from datetime import datetime
import sys
import os
from typing import List
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import json
from common_methods import GCPBucketManager
from cron_jobs.aquire_data.aqar_zyte.load_config import CONF, load_config
import glob

def download_csv_from_gcp(directories: List[str], gcp_manager: GCPBucketManager, date: str = None) -> bool:
    """
    Download CSV files from Google Cloud Storage bucket if they don't exist locally.
    
    Args:
        directories: List of directories to check
        gcp_manager: GCP bucket manager instance
        date: Specific date to download from. If None, uses latest date
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        base_path = "postgreSQL/dbo_operational/raw_schema_marketplace/real_estate"
        
        # If date not specified, get the latest date from GCP
        if not date:
            all_paths = gcp_manager.list_files(base_path)
            if not all_paths:
                raise Exception("No files found in GCP bucket")
            dates = set()
            for path in all_paths:
                parts = path.split('/')
                if len(parts) >= 6:  # Ensure path has enough parts
                    dates.add(parts[5])  # Date should be the 5th element
            if not dates:
                raise Exception("No valid dates found in paths")
            date = max(dates)  # Get most recent date
        
        for directory in directories:
            # Create local directory if it doesn't exist
            local_dir = os.path.join(os.path.dirname(__file__), directory)
            os.makedirs(local_dir, exist_ok=True)
            
            # List all CSV files in GCP for this directory
            gcp_prefix = f"{base_path}/{directory}/{date}"
            gcp_files = gcp_manager.list_files(gcp_prefix)
            
            for gcp_file in gcp_files:
                if not gcp_file.endswith('.csv'):
                    continue
                    
                file_name = os.path.basename(gcp_file)
                local_file_path = os.path.join(local_dir, file_name)
                
                # Check if file exists locally
                if not os.path.exists(local_file_path):
                    try:
                        # Use the GCPBucketManager's download_csv method
                        gcp_manager.download_csv(gcp_file, local_file_path)
                    except Exception as download_error:
                        print(f"Error downloading file {gcp_file}: {str(download_error)}")
                        continue
                else:
                    print(f"File already exists locally: {local_file_path}")
        
        return True
        
    except Exception as e:
        print(f"Error in GCP download: {str(e)}")
        return False

config = load_config()

# Initialize GCP manager once
gcp_manager = GCPBucketManager(
    bucket_name=config["bucket_name"], credentials_path=config["cred_path"]
)
directories = list(CONF.base_url_info.keys())
download_success = download_csv_from_gcp(directories, gcp_manager)