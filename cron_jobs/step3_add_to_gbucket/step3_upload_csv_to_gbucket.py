from datetime import datetime
import sys
import os
from typing import List, Union, Dict
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from common_methods import GCPBucketManager
from cron_jobs.aquire_data.saudi_real_estate.load_config import load_config
import glob


def upload_files_to_gcp(
    directories: List[Union[str, Dict]], gcp_manager: GCPBucketManager
) -> bool:
    """
    Upload CSV and JSON files to Google Cloud Storage bucket using provided GCPBucketManager instance
    """
    try:
        base_path = "postgreSQL/dbo_operational/raw_schema_marketplace"
        date = datetime.now().strftime("%Y%m%d")

        for directory in directories:
            if isinstance(directory, str):
                # Handle simple directory paths
                csv_files = glob.glob(
                    os.path.join("cron_jobs/aquire_data", directory, "*.csv")
                )
                for csv_file in csv_files:
                    file_name = os.path.basename(csv_file)
                    gcs_path = f"{base_path}/{directory}/{date}/{file_name}"
                    gcp_manager.upload_csv(csv_file, gcs_path)
                json_files = glob.glob(
                    os.path.join("cron_jobs/aquire_data", directory, "*.json")
                )
                for json_file in json_files:
                    file_name = os.path.basename(json_file)
                    gcs_path = f"{base_path}/{directory}/{date}/{file_name}"
                    gcp_manager.upload_csv(csv_file, gcs_path)
    

            elif isinstance(directory, dict):
                for main_dir, sub_dirs in directory.items():
                    for sub_dir in sub_dirs:
                        base_path_local = os.path.join("cron_jobs/aquire_data", main_dir, sub_dir)

                        csv_files = glob.glob(os.path.join("cron_jobs/aquire_data", main_dir, sub_dir, "*.csv"))
                        for csv_file in csv_files:
                            file_name = os.path.basename(csv_file)
                            gcs_path = f"{base_path}/{sub_dir}/{date}/{file_name}"
                            gcp_manager.upload_csv(csv_file, gcs_path)

                        direct_json_files = glob.glob(os.path.join(base_path_local, "*.json"))
                        for json_file in direct_json_files:
                            file_name = os.path.basename(json_file)
                            gcs_path = f"{base_path}/{sub_dir}/{date}/{file_name}"
                            print("Direct JSON file path:", json_file)
                            print("GCS path:", gcs_path)
                            gcp_manager.upload_csv(json_file, gcs_path)

                        # Upload nested JSON files
                        nested_json_files = glob.glob(
                            os.path.join(base_path_local, "**", "*.json"), recursive=True
                        )

                        for json_file in nested_json_files:
                            # Skip direct files
                            if os.path.dirname(json_file) == base_path_local:
                                continue

                            rel_path = os.path.relpath(json_file, base_path_local)
                            path_parts = rel_path.split(os.sep)

                            # Upload folder should be the version folder, e.g., "v15"
                            version_folder = path_parts[-2]  # e.g., "v15"
                            file_name = os.path.basename(json_file)
                            gcs_path = f"{base_path}/{sub_dir}/{date}/{version_folder}/{file_name}"
                            print("Nested JSON file path:", json_file)
                            print("GCS path:", gcs_path)
                            gcp_manager.upload_csv(json_file, gcs_path)

        return True

    except Exception as e:
        print(f"Error in GCP upload: {str(e)}")
        return False


config = load_config()
# Initialize GCP manager once

with open("cron_jobs/secrets_database.json", "r") as f:
    secrets = json.load(f)

gcp_manager = GCPBucketManager(
    bucket_name="s-locator",
    credentials_path=secrets["s-locator"]["bucket"]["credentials_path"],
)
gcp_manager_dev = GCPBucketManager(
    bucket_name="dev-s-locator",
    credentials_path=secrets["dev-s-locator"]["bucket"]["credentials_path"],
)
directories = [
    # "generate_economic_slocator_data",
    # "generate_housing_slocator_data",
    # "generate_household_slocator_data",
    # "saudi_real_estate",
    # "canada_census",
    # "canada_commercial_properties",
    # "saudi_census",
    # "saudi_ggl_categories_full_data"
    {"saudi_census": [
        "population",
        "housing", 
        "household"
    ]},
]

upload_success = upload_files_to_gcp(directories, gcp_manager)
upload_success_dev = upload_files_to_gcp(directories, gcp_manager_dev)
