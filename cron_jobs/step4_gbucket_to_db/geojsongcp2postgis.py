#!/usr/bin/env python3
import os
import json
import re
import io
import tempfile
from google.cloud import storage
import geopandas as gpd
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


# ----------------------------
# HELPERS
# ----------------------------
def download_blob_large(blob, timeout=300, stream_to_disk=False):
    """Download blob with optional disk streaming for very large files."""
    if stream_to_disk:
        tmp_file = tempfile.NamedTemporaryFile(suffix=".geojson", delete=False)
        blob.download_to_file(tmp_file, timeout=timeout)
        tmp_file_path = tmp_file.name
        tmp_file.close()
        return tmp_file_path
    else:
        buf = io.BytesIO()
        blob.download_to_file(buf, timeout=timeout)
        buf.seek(0)
        return buf


def get_latest_dir(bucket, base_path):
    """Return the latest date directory under the given GCS base path."""
    blobs = bucket.list_blobs(prefix=base_path)
    date_pattern = re.compile(rf"^{re.escape(base_path)}(\d{{8}})/")
    dates_found = set()

    for blob in blobs:
        match = date_pattern.match(blob.name)
        if match:
            dates_found.add(match.group(1))

    if not dates_found:
        raise ValueError(f"No date directories found under {base_path}")

    latest_date = max(dates_found)
    return f"{base_path}{latest_date}/"


def table_name_from_blob(blob_name):
    """Extract table name from blob."""
    parts = blob_name.split("/")
    filename = os.path.splitext(parts[-1])[0]
    version = parts[-2]
    return f"{filename}_{version}"


def import_geojson_to_postgis(bucket, gcs_path, table_prefix, engine, schema="schema_marketplace"):
    """Download latest GeoJSON files from GCS and load into PostGIS with large-file handling."""
    dataset_type = table_prefix
    latest_prefix = get_latest_dir(bucket, gcs_path)
    if not latest_prefix:
        print(f"No data found for {table_prefix}")
        return

    latest_prefix = latest_prefix + table_prefix
    print(f"Latest path: {latest_prefix}")

    blobs = bucket.list_blobs(prefix=latest_prefix)
    for blob in blobs:
        if blob.name.endswith(".geojson") or blob.name.endswith(".json"):
            file_size_mb = blob.size / (1024 * 1024)
            print(f"Processing: {blob.name} ({file_size_mb:.2f} MB)")

            # Timeout adjustment
            timeout = 600 if file_size_mb > 50 else 300
            stream_to_disk = file_size_mb > 200

            if stream_to_disk:
                print("Large file detected → streaming to disk...")
                tmp_file_path = download_blob_large(blob, timeout=timeout, stream_to_disk=True)
                gdf = gpd.read_file(tmp_file_path)
                os.remove(tmp_file_path)
            else:
                geo_data = download_blob_large(blob, timeout=timeout, stream_to_disk=False)
                gdf = gpd.read_file(geo_data)

            table_name = table_name_from_blob(blob.name)

            if "population" in dataset_type and "population" not in table_name:
                table_name = "population_" + table_name
            elif "area" in dataset_type:
                table_name = "area_income_" + table_name
            elif "household" in dataset_type:
                table_name = "household_" + table_name
            elif "housing" in dataset_type:
                table_name = "housing_" + table_name

            # Write in batches to prevent connection drop
            try:
                gdf.to_postgis(table_name, engine, if_exists="replace", chunksize=1000, schema=schema)
                print(f"Loaded {blob.name} --> {schema}.{table_name}")
            except OperationalError as e:
                print(f"Connection lost while writing {table_name}. Reconnecting...")
                engine.dispose()
                engine.connect()
                gdf.to_postgis(table_name, engine, if_exists="replace", chunksize=500, schema=schema)

    print(f"Completed import for {dataset_type}")


def run_geojson_gcp_to_db():
    """Run the complete import process."""
    GCP_BUCKET = "dev-s-locator"
    POPULATION_PATH = "postgreSQL/dbo_operational/raw_schema_marketplace/population/"
    AREA_INCOME_PATH = "postgreSQL/dbo_operational/raw_schema_marketplace/interpolated_riyadh/"
    HOUSEHOLD_PATH = "postgreSQL/dbo_operational/raw_schema_marketplace/household/"
    HOUSING_PATH = "postgreSQL/dbo_operational/raw_schema_marketplace/housing/"

    # Load secrets
    with open("cron_jobs/secrets_database.json", "r") as f:
        conf = json.load(f)
    gcp_credentials_file = conf['dev-s-locator']['bucket']['credentials_path']
    db_conf = conf['dev-s-locator']['db']

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_credentials_file

    # Connect to GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCP_BUCKET)

    # Create SQLAlchemy engine with keepalive
    db_url = (
        f"postgresql+psycopg2://{db_conf['user']}:{db_conf['password']}"
        f"@{db_conf['host']}:{db_conf['port']}/{db_conf['dbname']}"
    )
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_recycle=1200  # Reconnect every 30  mins to avoid stale connections
    )

    # Import datasets
    import_geojson_to_postgis(bucket, POPULATION_PATH, "population_json_files/", engine)
    import_geojson_to_postgis(bucket, AREA_INCOME_PATH, "area_income_geojson/", engine)
    import_geojson_to_postgis(bucket, HOUSING_PATH, "housing_json_files/", engine)
    import_geojson_to_postgis(bucket, HOUSEHOLD_PATH, "household_json_files/", engine)

    print("All imports completed successfully!")


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    run_geojson_gcp_to_db()
