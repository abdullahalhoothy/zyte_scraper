import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
from io import BytesIO
import pandas as pd
import os
import json
import sys
from io import StringIO
from geojsongcp2postgis import run_geojson_gcp_to_db
import logging
import argparse
import sys
parser = argparse.ArgumentParser()
parser.add_argument("--log-file", help="Path to shared log file", required=False)
args = parser.parse_args()

module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(module_dir)

if(args.log_file):
    from logging_utils import setup_logging
    setup_logging(args.log_file)

from common_methods import GCPBucketManager


def all_chunks(gcp, file_paths, chunk_size):
    """
    Generator yielding DataFrame chunks from all CSV files in file_paths.
    """
    for file_path in file_paths:
        logging.info(f"Reading chunks from CSV: {file_path}")
        blob = gcp.bucket.blob(file_path)
        data = blob.download_as_bytes()
        try:
            chunk_iter = pd.read_csv(
                BytesIO(data),
                encoding="utf-8-sig",
                low_memory=False,
                chunksize=chunk_size,
            )
        except UnicodeDecodeError:
            chunk_iter = pd.read_csv(
                BytesIO(data),
                encoding="ISO-8859-1",
                low_memory=False,
                chunksize=chunk_size,
            )
        for chunk_df in chunk_iter:
            yield chunk_df


def insert_all_chunks_to_temp_table(
    conn, chunk_iter, schema, temp_table_name, df_for_types
):
    """
    Create a temp table and insert all chunks into it (appending).
    df_for_types: DataFrame to infer column types (first chunk or sample)
    """
    logging.info(f"Creating temporary table {schema}.{temp_table_name} for bulk insert...")
    columns = []
    for col in df_for_types.columns:
        dtype = (
            "INTEGER"
            if df_for_types[col].dtype == "int64"
            else "REAL" if df_for_types[col].dtype == "float64" else "TEXT"
        )
        columns.append(sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(dtype)))
    create_temp = sql.SQL("CREATE TABLE IF NOT EXISTS {}.{} ({})").format(
        sql.Identifier(schema),
        sql.Identifier(temp_table_name),
        sql.SQL(", ").join(columns),
    )
    with conn.cursor() as cursor:
        cursor.execute(create_temp)
        for i, chunk_df in enumerate(chunk_iter):
            logging.info(f"Bulk inserting chunk {i+1} into {schema}.{temp_table_name}...")
            csv_text = chunk_df.to_csv(
                index=False, header=False, sep="\t", na_rep="\\N"
            )
            buffer = BytesIO(csv_text.encode("utf-8"))
            buffer.seek(0)
            columns_sql = sql.SQL(", ").join(
                sql.Identifier(col) for col in chunk_df.columns
            )
            copy_cmd = sql.SQL(
                "COPY {}.{} ({}) FROM STDIN WITH (FORMAT csv, DELIMITER E'\\t', NULL '\\N')"
            ).format(sql.Identifier(schema), sql.Identifier(temp_table_name), columns_sql)
            cursor.execute("SET client_encoding TO 'UTF8'")
            cursor.copy_expert(copy_cmd, buffer)
    logging.info(f"All chunks inserted into temporary table {schema}.{temp_table_name}.")


def replace_table_with_temp(conn, schema, table_name, temp_table_name):
    """
    Atomically swap temp table with original table, using same logic as insert_data_into_table.
    df_for_types: DataFrame to infer column types (first chunk or sample)
    """
    logging.info(
        f"Swapping tables: replacing {schema}.{table_name} with {schema}.{temp_table_name}..."
    )
    old_table = f"old_{table_name}"
    with conn.cursor() as cursor:
        # Drop old_table if exists
        cursor.execute(
            sql.SQL("DROP TABLE IF EXISTS {}.{}").format(
                sql.Identifier(schema), sql.Identifier(old_table)
            )
        )
        # Rename current table to old_table
        cursor.execute(
            sql.SQL("ALTER TABLE {}.{} RENAME TO {}").format(
                sql.Identifier(schema),
                sql.Identifier(table_name),
                sql.Identifier(old_table),
            )
        )
        # Rename temp table to main table
        cursor.execute(
            sql.SQL("ALTER TABLE {}.{} RENAME TO {}").format(
                sql.Identifier(schema),
                sql.Identifier(temp_table_name),
                sql.Identifier(table_name),
            )
        )
        # Drop old_table
        cursor.execute(
            sql.SQL("DROP TABLE {}.{}").format(
                sql.Identifier(schema), sql.Identifier(old_table)
            )
        )
    logging.info(
        f"Table {schema}.{table_name} replaced with data from {schema}.{temp_table_name}."
    )


def ensure_database_exists(config, db_name):
    """
    Ensures database exists, creates it if it doesn't, and returns a connection to it
    """
    try:
        # First try to connect directly to the target database
        return get_db_connection(config, db_name)
    except psycopg2.Error as e:
        if "database" in str(e) and "does not exist" in str(e):
            logging.info(f"Database {db_name} does not exist. Creating...")
            # Connect to postgres to create the database
            postgres_conn = get_db_connection(config, "postgres")
            postgres_conn.autocommit = True
            try:
                with postgres_conn.cursor() as cursor:
                    # Create the new database
                    cursor.execute(
                        sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                    )
                logging.info(f"Successfully created database {db_name}")
            finally:
                postgres_conn.close()

            # Now connect to the newly created database
            logging.info(f"Connecting to newly created database {db_name}")
            return get_db_connection(config, db_name)
        raise


def get_db_connection(db_config, db_name=None):
    """Create a database connection with optional database name override"""
    conn_params = db_config.copy()
    if db_name:
        conn_params["dbname"] = db_name
    logging.info(f"Attempting connection to database: {conn_params['dbname']}")
    # Add connection timeout (default 15 seconds)
    conn_params.setdefault("connect_timeout", 15)
    return psycopg2.connect(**conn_params)


def process_database_structure(gcp, config, bucket_name, objects_to_create):
    connections = {}
    try:
        # Process CSV files
        for (db_name, schema_name, table_name), file_paths in objects_to_create[
            "csv"
        ].items():
            if db_name not in connections:
                connections[db_name] = ensure_database_exists(config, db_name)

            conn = connections[db_name]
            # Use first CSV to infer types and create schema/table
            first_blob = gcp.bucket.blob(file_paths[0])
            first_data = first_blob.download_as_bytes()
            CHUNK_SIZE = 5000  # Adjust chunk size as needed
            try:
                first_chunk_iter = pd.read_csv(
                    BytesIO(first_data),
                    encoding="utf-8-sig",
                    low_memory=False,
                    chunksize=CHUNK_SIZE,
                )
            except UnicodeDecodeError:
                first_chunk_iter = pd.read_csv(
                    BytesIO(first_data),
                    encoding="ISO-8859-1",
                    low_memory=False,
                    chunksize=CHUNK_SIZE,
                )
            # Get first chunk for type inference
            first_chunk = next(first_chunk_iter)
            create_schema_and_table(conn, first_chunk, schema_name, table_name)

            # Bulk insert all chunks from all CSVs into temp table
            temp_table_name = f"temp_{table_name}"
            chunk_generator = all_chunks(gcp, file_paths, CHUNK_SIZE)
            insert_all_chunks_to_temp_table(
                conn, chunk_generator, schema_name, temp_table_name, first_chunk
            )
            conn.commit()
            replace_table_with_temp(
                conn, schema_name, table_name, temp_table_name
            )
            conn.commit()
            logging.info(f"All CSVs inserted into {db_name}.{schema_name}.{table_name}")

        # Process image files
        for (db_name, schema_name, table_name), image_data in objects_to_create[
            "images"
        ].items():
            if db_name not in connections:
                connections[db_name] = ensure_database_exists(config, db_name)

            conn = connections[db_name]
            insert_image_metadata(conn, schema_name, table_name, image_data)
            conn.commit()
            logging.info(f"Image metadata inserted into {db_name}.{schema_name}.{table_name}")

    except Exception as e:
        logging.info(f"Error occurred: {e}")
        for conn in connections.values():
            try:
                conn.rollback()
            except:
                pass
        raise
    finally:
        for conn in connections.values():
            try:
                conn.close()
            except:
                pass


def create_schema_and_table(conn, df, schema, table_name):
    """Creates schema and table if they don't exist."""
    conn.autocommit = True  # Temporarily enable autocommit
    try:
        with conn.cursor() as cursor:
            # Create schema
            cursor.execute(
                """
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name = %s
            """,
                (schema,),
            )

            if not cursor.fetchone():
                cursor.execute(
                    sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema))
                )
                logging.info(f"Schema '{schema}' created successfully.")

            # Create table
            columns = []
            for col in df.columns:
                dtype = (
                    "INTEGER"
                    if df[col].dtype == "int64"
                    else "REAL" if df[col].dtype == "float64" else "TEXT"
                )
                columns.append(
                    sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(dtype))
                )
            logging.info(f"Creating table '{schema}.{table_name}'...")

            # Build the CREATE TABLE command using SQL composition
            create_table_cmd = sql.SQL("CREATE TABLE {}.{} ({})").format(
                sql.Identifier(schema),
                sql.Identifier(table_name),
                sql.SQL(", ").join(columns),
            )

            # Check if table exists
            cursor.execute(
                """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = %s
            """,
                (schema, table_name),
            )

            if not cursor.fetchone():
                cursor.execute(create_table_cmd)
                logging.info(f"Table '{schema}.{table_name}' created successfully.")
            else:
                logging.info(f"Table '{schema}.{table_name}' already exists.")

    finally:
        conn.autocommit = False  # Restore autocommit to False


def insert_data_into_table(conn, df, table_name, schema):
    # add logging.infos to this function for debugging
    logging.info(f"Inserting data into {schema}.{table_name}...")
    # First, analyze DataFrame to determine which columns need BIGINT
    columns_to_alter = []
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            # Check if any value exceeds PostgreSQL integer limits
            max_val = df[col].max()
            min_val = df[col].min()
            if max_val > 2147483647 or min_val < -2147483648:
                columns_to_alter.append(col)

                # Convert float values to integers for BIGINT columns
                if df[col].dtype == "float64":
                    df[col] = df[col].fillna(0).astype("int64")

    # Write CSV to bytes buffer with UTF-8 encoding
    logging.info(f"Preparing data for COPY into {schema}.{table_name}...")
    csv_text = df.to_csv(index=False, header=False, sep="\t", na_rep="\\N")
    buffer = BytesIO(csv_text.encode("utf-8"))
    buffer.seek(0)

    with conn.cursor() as cursor:
        try:
            logging.info(f"Starting COPY to {schema}.{table_name}...")
            # Create a temporary table
            temp_table = f"temp_{table_name}"
            # Drop temp table if it exists
            drop_temp = sql.SQL("DROP TABLE IF EXISTS {}.{}").format(
                sql.Identifier(schema), sql.Identifier(temp_table)
            )
            cursor.execute(drop_temp)

            # CHANGED: Create temp table based on DataFrame structure instead of existing table
            columns = []
            for col in df.columns:
                dtype = (
                    "INTEGER"
                    if df[col].dtype == "int64"
                    else "REAL" if df[col].dtype == "float64" else "TEXT"
                )
                columns.append(
                    sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(dtype))
                )
            logging.info(f"Creating temporary table {schema}.{temp_table}...")
            create_temp = sql.SQL("CREATE TABLE {}.{} ({})").format(
                sql.Identifier(schema),
                sql.Identifier(temp_table),
                sql.SQL(", ").join(columns),
            )
            cursor.execute(create_temp)

            # Alter column types to BIGINT where needed
            for column in columns_to_alter:
                logging.info(f"Altering column {column} to BIGINT in temp table...")
                alter_column = sql.SQL(
                    """
                    ALTER TABLE {}.{} 
                    ALTER COLUMN {} TYPE BIGINT
                """
                ).format(
                    sql.Identifier(schema),
                    sql.Identifier(temp_table),
                    sql.Identifier(column),
                )
                cursor.execute(alter_column)

            # Insert into temp table
            logging.info(f"Inserting data into temporary table {schema}.{temp_table}...")
            qualified_temp_table = sql.SQL("{}.{}").format(
                sql.Identifier(schema), sql.Identifier(temp_table)
            )
            columns = sql.SQL(", ").join(sql.Identifier(col) for col in df.columns)
            copy_cmd = sql.SQL(
                "COPY {} ({}) FROM STDIN WITH (FORMAT csv, DELIMITER E'\\t', NULL '\\N')"
            ).format(qualified_temp_table, columns)
            cursor.execute("SET client_encoding TO 'UTF8'")  # Handle special characters
            cursor.copy_expert(copy_cmd, buffer)

            # Swap tables
            logging.info(f"Swapping tables to replace {schema}.{table_name}...")
            old_table = f"old_{table_name}"
            rename_commands = [
                sql.SQL("DROP TABLE IF EXISTS {}.{}").format(
                    sql.Identifier(schema), sql.Identifier(old_table)
                ),
                sql.SQL("ALTER TABLE {}.{} RENAME TO {}").format(
                    sql.Identifier(schema),
                    sql.Identifier(table_name),
                    sql.Identifier(old_table),
                ),
                sql.SQL("ALTER TABLE {}.{} RENAME TO {}").format(
                    sql.Identifier(schema),
                    sql.Identifier(temp_table),
                    sql.Identifier(table_name),
                ),
                sql.SQL("DROP TABLE {}.{}").format(
                    sql.Identifier(schema), sql.Identifier(old_table)
                ),
            ]
            for cmd in rename_commands:
                cursor.execute(cmd)
            logging.info(f"Table {schema}.{table_name} replaced with {len(df)} new rows")
            if columns_to_alter:
                logging.info(f"Columns converted to BIGINT: {', '.join(columns_to_alter)}")
        except Exception as e:
            logging.info(f"Error during copy to {schema}.{table_name}: {e}")
            logging.info("First row of DataFrame:")
            logging.info(df.iloc[0].to_dict() if not df.empty else "<DataFrame is empty>")
            logging.info("DataFrame dtypes:")
            logging.info(df.dtypes)
            logging.info("First 200 bytes of buffer:")
            buffer.seek(0)
            logging.info(buffer.read(200))
            # Save first 10 rows to CSV for debugging
            debug_csv_name = f"debug_first_rows_{schema}_{table_name}.csv"
            try:
                df.head(10).to_csv(debug_csv_name, index=False, encoding="utf-8-sig")
                logging.info(f"Saved first 10 rows to {debug_csv_name}")
            except Exception as save_err:
                logging.info(f"Failed to save debug CSV: {save_err}")
            raise


def insert_image_metadata(conn, schema, table_name, image_data):
    with conn.cursor() as cursor:
        cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{schema}"."{table_name}" (
                id SERIAL PRIMARY KEY,
                file_name TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE
            )
        """
        )
        insert_query = f'INSERT INTO "{schema}"."{table_name}" (file_name, url) VALUES %s ON CONFLICT DO NOTHING'
        execute_values(cursor, insert_query, image_data)


def list_csv_files_in_bucket(gcp, exclude_folders=[]):
    structure = {"csv": {}, "images": {}}
    blobs = list(gcp.bucket.list_blobs())
    for blob in blobs:
        parts = blob.name.split("/")

        # Skip unexpected files
        if len(parts) < 5 or not (
            blob.name.endswith(".csv")
            or blob.name.split(".")[-1].lower()
            in [
                "jpeg",
                "jpg",
                "png",
                "gif",
                "bmp",
                "tiff",
                "webp",
                "svg",
                "heic",
            ]
        ):
            logging.info(f"Skipping file with unexpected path structure: {blob.name}")
            continue

        db_name, schema_name, dir_name, dir_date = (
            parts[1],
            parts[2],
            parts[3],
            parts[4],
        )

        # skip excluded folders
        if exclude_folders:
            if schema_name in exclude_folders or dir_name in exclude_folders:
                logging.info(f"Skipping excluded folder: {blob.name}")
                continue

        if blob.name.endswith(".csv"):
            # remove .csv extension for table name
            table_name = parts[5].rsplit(".csv", 1)[0]
            structure["csv"].setdefault((db_name, schema_name, table_name), []).append(
                blob.name
            )
        if blob.name.endswith(".jpeg") or blob.name.endswith(".png"):
            structure["images"].setdefault((db_name, schema_name, dir_name), []).append(
                (dir_date, blob.public_url)
            )
    return structure


def process_all_pipelines(exclude_folders=[]):
    """Process all pipeline configurations"""
    with open("cron_jobs/secrets_database.json", "r") as f:
        config = json.load(f)

    for pipeline_name, pipeline_config in config.items():
        # Skip incomplete configurations
        if (
            not pipeline_config["bucket"]["credentials_path"]
            or not pipeline_config["db"]["host"]
        ):
            logging.info(f"Skipping {pipeline_name}: Incomplete configuration")
            continue

        try:
            logging.info(f"\nProcessing pipeline: {pipeline_name}")

            # Initialize GCP manager for this pipeline
            gcp_manager = GCPBucketManager(
                bucket_name=pipeline_name,
                credentials_path=pipeline_config["bucket"]["credentials_path"],
            )

            # Get the file structure
            structure = list_csv_files_in_bucket(gcp_manager, exclude_folders)

            # Skip if no files found
            if not structure["csv"] and not structure["images"]:
                run_geojson_gcp_to_db(gcp_manager,pipeline_config)
                logging.info(f"No files found in bucket {pipeline_name}")
                continue
            run_geojson_gcp_to_db(gcp_manager,pipeline_config)
            # Process the structure
            process_database_structure(
                gcp_manager, pipeline_config["db"], pipeline_name, structure
            )

            logging.info(f"Successfully processed pipeline: {pipeline_name}")

        except Exception as e:
            logging.info(f"Error processing pipeline {pipeline_name}: {e}")
            continue


process_all_pipelines(
    [
        "canada_census",
        "canada_commercial_properties",
        "household",
        "housing",
        "population",
        "interpolated_income",
    ]
)
run_geojson_gcp_to_db()
