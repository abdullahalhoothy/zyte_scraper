from datetime import datetime
import sys
import os
from typing import List, Union, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from common_methods import GCPBucketManager
from cron_jobs.aquire_data.saudi_real_estate.load_config import load_config
import glob


def upload_csv_to_gcp(
    directories: List[Union[str, Dict]], gcp_manager: GCPBucketManager
) -> bool:
    """
    Upload CSV files to Google Cloud Storage bucket using provided GCPBucketManager instance
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

            elif isinstance(directory, dict):
                # Handle nested directories
                for main_dir, sub_dirs in directory.items():
                    for sub_dir in sub_dirs:
                        csv_files = glob.glob(
                            os.path.join(
                                "cron_jobs/aquire_data", main_dir, sub_dir, "*.csv"
                            )
                        )
                        for csv_file in csv_files:
                            file_name = os.path.basename(csv_file)
                            # Use the sub_dir (innermost folder) name in the GCS path
                            gcs_path = f"{base_path}/{sub_dir}/{date}/{file_name}"
                            gcp_manager.upload_csv(csv_file, gcs_path)

        return True

    except Exception as e:
        print(f"Error in GCP upload: {str(e)}")
        return False


config = load_config()
# Initialize GCP manager once
gcp_manager = GCPBucketManager(
    bucket_name="s-locator",
    credentials_path="cron_jobs/weighty-gasket-437422-h6-e1255469595a.json",
)

directories = [
    # "generate_economic_slocator_data",
    # "generate_housing_slocator_data",
    # "generate_household_slocator_data",
    # "saudi_real_estate",
    # "canada_census",
    # "canada_commercial_properties",
    "saudi_census",
    # {"saudi_census": [
        # "population",
        #   "housing", 
        #   "household"
        #   ]},
]

upload_success = upload_csv_to_gcp(directories, gcp_manager)
