from datetime import datetime
import sys
import os
from typing import List
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
import json
from common_methods import GCPBucketManager
from cron_jobs.aquire_data.aqar_zyte_gbucket_db.load_config import CONF, load_config
import glob


def upload_json_to_gcp(directories: List[str], gcp_manager: GCPBucketManager) -> bool:
    """
    Upload JSON files to Google Cloud Storage bucket using provided GCPBucketManager instance
    """
    try:
        # Get current timestamp for folder organization
        base_path = "postgreSQL/dbo_operational/raw_schema-marketplace/real_estate"
        date = datetime.now().strftime("%Y%m%d")

        for directory in directories:
            # Get all JSON files in the directory
            json_files = glob.glob(os.path.join(os.path.dirname(__file__) +"\\"+ directory, "*.json"))

            for json_file in json_files:
                try:
                    # Read JSON file
                    with open(json_file, "r", encoding="utf-8") as f:
                        json_data = json.load(f)

                    file_name = os.path.basename(json_file)
                    gcs_path = f"{base_path}/{directory}/{date}/{file_name}"

                    # Upload file to GCS using our manager
                    gcp_manager.upload_json(json_data, gcs_path)

                    print(f"Successfully uploaded {json_file} to {gcs_path}")

                except Exception as file_error:
                    print(f"Error uploading file {json_file}: {str(file_error)}")
                    continue

        return True

    except Exception as e:
        print(f"Error in GCP upload: {str(e)}")
        return False


def upload_csv_to_gcp(directories: List[str], gcp_manager: GCPBucketManager) -> bool:
    """
    Upload CSV files to Google Cloud Storage bucket using provided GCPBucketManager instance
    """
    try:
        base_path = "postgreSQL/dbo_operational/raw_schema-marketplace/real_estate"
        date = datetime.now().strftime("%Y%m%d")
        
        for directory in directories:
            csv_files = glob.glob(os.path.join(os.path.dirname(__file__) + "\\" + directory, "*.csv"))
            
            for csv_file in csv_files:

                file_name = os.path.basename(csv_file)
                gcs_path = f"{base_path}/{directory}/{date}/{file_name}"
                
                # Direct file upload without DataFrame conversion
                gcp_manager.upload_csv(csv_file, gcs_path)
                    
                    
        return True
        
    except Exception as e:
        print(f"Error in GCP upload: {str(e)}")
        return False

config = load_config()

# Initialize GCP manager once
gcp_manager = GCPBucketManager(
    bucket_name=config["bucket_name"], credentials_path=config["cred_path"]
)

directories = list(CONF.base_url_info.keys())
upload_success = upload_csv_to_gcp(directories, gcp_manager)

