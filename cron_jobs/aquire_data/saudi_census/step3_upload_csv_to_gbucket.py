from datetime import datetime
import sys
import os
from typing import List
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from common_methods import GCPBucketManager
from cron_jobs.aquire_data.aqar_zyte_gbucket_db.load_config import load_config
import glob



def upload_csv_to_gcp(directories: List[str], gcp_manager: GCPBucketManager) -> bool:
    """
    Upload CSV files to Google Cloud Storage bucket using provided GCPBucketManager instance
    """
    try:
        base_path = "postgreSQL/dbo_operational/raw_schema_marketplace"
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

directories = ["household", "housing", "population"]
upload_success = upload_csv_to_gcp(directories, gcp_manager)

