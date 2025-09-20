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

module_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(module_dir)
from common_methods import GCPBucketManager


def ensure_database_exists(config, db_name):
    """
    Ensures database exists, creates it if it doesn't, and returns a connection to it
    """
    try:
        # First try to connect directly to the target database
        return get_db_connection(config, db_name)
    except psycopg2.Error as e:
        if "database" in str(e) and "does not exist" in str(e):
            print(f"Database {db_name} does not exist. Creating...")
            # Connect to postgres to create the database
            postgres_conn = get_db_connection(config, "postgres")
            postgres_conn.autocommit = True
            try:
                with postgres_conn.cursor() as cursor:
                    # Create the new database
                    cursor.execute(
                        sql.SQL("CREATE DATABASE {}").format(
                            sql.Identifier(db_name)
                        )
                    )
                print(f"Successfully created database {db_name}")
            finally:
                postgres_conn.close()

            # Now connect to the newly created database
            print(f"Connecting to newly created database {db_name}")
            return get_db_connection(config, db_name)
        raise


def get_db_connection(db_config, db_name=None):
    """Create a database connection with optional database name override"""
    conn_params = db_config.copy()
    if db_name:
        conn_params["dbname"] = db_name
    print(f"Attempting connection to database: {conn_params['dbname']}")
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
                # This will create the database if it doesn't exist and return a connection to it
                connections[db_name] = ensure_database_exists(config, db_name)

            conn = connections[db_name]
            merged_df = read_and_merge_csv_files(gcp, file_paths)

            # Create schema and table with autocommit
            create_schema_and_table(conn, merged_df, schema_name, table_name)

            # Now insert data in a new transaction
            insert_data_into_table(conn, merged_df, table_name, schema_name)
            conn.commit()
            print(f"Data inserted into {db_name}.{schema_name}.{table_name}")

        # Process image files
        for (db_name, schema_name, table_name), image_data in objects_to_create[
            "images"
        ].items():
            if db_name not in connections:
                connections[db_name] = ensure_database_exists(config, db_name)

            conn = connections[db_name]
            insert_image_metadata(conn, schema_name, table_name, image_data)
            conn.commit()
            print(
                f"Image metadata inserted into {db_name}.{schema_name}.{table_name}"
            )

    except Exception as e:
        print(f"Error occurred: {e}")
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
                print(f"Schema '{schema}' created successfully.")

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
                print(f"Table '{schema}.{table_name}' created successfully.")
            else:
                print(f"Table '{schema}.{table_name}' already exists.")

            # Verify table exists
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
                raise Exception(
                    f"Table {schema}.{table_name} was not created successfully"
                )

    finally:
        conn.autocommit = False  # Restore autocommit to False


def create_database_structure(conn, df, db_name, schema, table_name):
    """
    Creates database, schema, and table if they don't exist.
    Returns True if operations were successful.
    """
    # First create database with autocommit
    conn.autocommit = True
    try:
        with conn.cursor() as cursor:
            # Check and create database
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s", (db_name,)
            )
            if not cursor.fetchone():
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(db_name)
                    )
                )
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")

            # Check if schema exists
            cursor.execute(
                """
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name = %s
            """,
                (schema,),
            )

            if not cursor.fetchone():
                cursor.execute(f'CREATE SCHEMA "{schema}"')
                print(f"Schema '{schema}' created successfully.")
            else:
                print(f"Schema '{schema}' already exists.")

            # Create table
            columns = []
            for col in df.columns:
                dtype = (
                    "INTEGER"
                    if df[col].dtype == "int64"
                    else "REAL" if df[col].dtype == "float64" else "TEXT"
                )
                columns.append(f'"{col}" {dtype}')
            columns_str = ", ".join(columns)

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
                create_table_sql = (
                    f'CREATE TABLE "{schema}"."{table_name}" ({columns_str})'
                )
                cursor.execute(create_table_sql)
                print(f"Table '{schema}.{table_name}' created successfully.")
            else:
                print(f"Table '{schema}.{table_name}' already exists.")

    except Exception as e:
        print(f"Error in database structure creation: {e}")
        raise
    finally:
        conn.autocommit = False


def insert_data_into_table(conn, df, table_name, schema):
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
    csv_text = df.to_csv(index=False, header=False, sep="\t", na_rep="\\N")
    buffer = BytesIO(csv_text.encode("utf-8"))
    buffer.seek(0)

    with conn.cursor() as cursor:
        try:
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

            create_temp = sql.SQL("CREATE TABLE {}.{} ({})").format(
                sql.Identifier(schema),
                sql.Identifier(temp_table),
                sql.SQL(", ").join(columns),
            )
            cursor.execute(create_temp)

            # Alter column types to BIGINT where needed
            for column in columns_to_alter:
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
            qualified_temp_table = sql.SQL("{}.{}").format(
                sql.Identifier(schema), sql.Identifier(temp_table)
            )
            columns = sql.SQL(", ").join(
                sql.Identifier(col) for col in df.columns
            )
            copy_cmd = sql.SQL(
                "COPY {} ({}) FROM STDIN WITH (FORMAT csv, DELIMITER E'\\t', NULL '\\N')"
            ).format(qualified_temp_table, columns)
            cursor.execute(
                "SET client_encoding TO 'UTF8'"
            )  # Handle special characters
            cursor.copy_expert(copy_cmd, buffer)

            # Swap tables
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
            print(
                f"Table {schema}.{table_name} replaced with {len(df)} new rows"
            )
            if columns_to_alter:
                print(
                    f"Columns converted to BIGINT: {', '.join(columns_to_alter)}"
                )
        except Exception as e:
            print(f"Error during copy to {schema}.{table_name}: {e}")
            print("First row of DataFrame:")
            print(
                df.iloc[0].to_dict() if not df.empty else "<DataFrame is empty>"
            )
            print("DataFrame dtypes:")
            print(df.dtypes)
            print("First 200 bytes of buffer:")
            buffer.seek(0)
            print(buffer.read(200))
            # Save first 10 rows to CSV for debugging
            debug_csv_name = f"debug_first_rows_{schema}_{table_name}.csv"
            try:
                df.head(10).to_csv(
                    debug_csv_name, index=False, encoding="utf-8-sig"
                )
                print(f"Saved first 10 rows to {debug_csv_name}")
            except Exception as save_err:
                print(f"Failed to save debug CSV: {save_err}")
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
            print(f"Skipping file with unexpected path structure: {blob.name}")
            continue

        db_name, schema_name, table_name, file_name = (
            parts[1],
            parts[2],
            parts[3],
            parts[4],
        )

        # skip excluded folders
        if exclude_folders:
            if schema_name in exclude_folders or table_name in exclude_folders:
                print(f"Skipping excluded folder: {blob.name}")
                continue

        if blob.name.endswith(".csv"):
            structure["csv"].setdefault(
                (db_name, schema_name, table_name), []
            ).append(blob.name)
        else:
            structure["images"].setdefault(
                (db_name, schema_name, table_name), []
            ).append((file_name, blob.public_url))
    return structure


def read_and_merge_csv_files(slocator_gcp, file_paths):
    dataframes = []
    for file_path in file_paths:
        blob = slocator_gcp.bucket.blob(file_path)
        data = blob.download_as_bytes()
        try:
            df = pd.read_csv(
                BytesIO(data), encoding="utf-8-sig", low_memory=False
            )  # handles both utf-8 and utf-8-sig
        except UnicodeDecodeError:
            df = pd.read_csv(
                BytesIO(data), encoding="ISO-8859-1", low_memory=False
            )
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)


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
            print(f"Skipping {pipeline_name}: Incomplete configuration")
            continue

        try:
            print(f"\nProcessing pipeline: {pipeline_name}")

            # Initialize GCP manager for this pipeline
            gcp_manager = GCPBucketManager(
                bucket_name=pipeline_name,
                credentials_path=pipeline_config["bucket"]["credentials_path"],
            )

            # Get the file structure
            structure = list_csv_files_in_bucket(gcp_manager, exclude_folders)

            # Skip if no files found
            if not structure["csv"] and not structure["images"]:
                print(f"No files found in bucket {pipeline_name}")
                continue

            # Process the structure
            process_database_structure(
                gcp_manager, pipeline_config["db"], pipeline_name, structure
            )

            print(f"Successfully processed pipeline: {pipeline_name}")

        except Exception as e:
            print(f"Error processing pipeline {pipeline_name}: {e}")
            continue


process_all_pipelines(
    [
        "canada_census",
        "canada_commercial_properties",
        "household",
        "housing",
        "population",
        "interpolated_income",
        "ignore",
    ]
)
run_geojson_gcp_to_db()
