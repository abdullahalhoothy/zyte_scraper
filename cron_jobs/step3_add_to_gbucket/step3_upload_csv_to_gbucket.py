from datetime import datetime
import sys
import os
from typing import List, Union, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from common_methods import GCPBucketManager
from cron_jobs.aquire_data.saudi_real_estate.load_config import load_config
import glob


def upload_json_to_gcp(
    directories: List[Union[str, Dict]], gcp_manager: GCPBucketManager
) -> bool:
    """
    Upload JSON files to Google Cloud Storage bucket using provided GCPBucketManager instance
    """
    try:
        base_path = "postgreSQL/dbo_operational/raw_schema_marketplace"
        date = datetime.now().strftime("%Y%m%d")

        for directory in directories:
            if isinstance(directory, str):
                # Handle simple directory paths
                json_files = glob.glob(
                    os.path.join("cron_jobs/aquire_data", directory, "*.json")
                )
                for json_file in json_files:
                    file_name = os.path.basename(json_file)
                    gcs_path = f"{base_path}/{directory}/{date}/{file_name}"
                    gcp_manager.upload_json(json_file, gcs_path)

            elif isinstance(directory, dict):
                # Handle nested directories
                for main_dir, sub_dirs in directory.items():
                    for sub_dir in sub_dirs:
                        json_files = glob.glob(
                            os.path.join(
                                "cron_jobs/aquire_data", main_dir, sub_dir, "*.json"
                            )
                        )
                        for json_file in json_files:
                            file_name = os.path.basename(json_file)
                            # Use the sub_dir (innermost folder) name in the GCS path
                            gcs_path = f"{base_path}/{sub_dir}/{date}/{file_name}"
                            gcp_manager.upload_json(json_file, gcs_path)

        return True

    except Exception as e:
        print(f"Error in GCP upload: {str(e)}")
        return False


config = load_config()
# Initialize GCP manager once
gcp_manager_s_locator = GCPBucketManager(
    bucket_name="s-locator",
    credentials_path="cron_jobs/ggl_bucket_sa.json",
)
gcp_manager_dev_s_locator = GCPBucketManager(
    bucket_name="dev-s-locator",
    credentials_path="cron_jobs/ggl_bucket_sa.json",
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

upload_success_s_locator = upload_json_to_gcp(directories, gcp_manager_s_locator)

upload_success_dev_locator = upload_json_to_gcp(directories, gcp_manager_dev_s_locator)
