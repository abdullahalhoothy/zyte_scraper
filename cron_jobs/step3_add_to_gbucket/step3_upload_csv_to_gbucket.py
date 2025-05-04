from datetime import datetime
import sys
import os
from typing import List, Union, Dict
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from common_methods import GCPBucketManager
from cron_jobs.aquire_data.saudi_real_estate.load_config import load_config
import glob


def upload_directory_to_gcp(
    source_paths: Union[str, List[Union[str, Dict[str, List[str]]]]],
    gcp_manager: GCPBucketManager,
    base_gcp_path: str = "postgreSQL/dbo_operational/raw_schema_marketplace",
    include_date: bool = True
) -> bool:
    """
    Upload entire directories to GCP bucket, maintaining directory structure.
    Only uploads CSV and JSON files.
   
    Args:
        source_paths: Can be:
            - A string (single directory path)
            - A list of strings (multiple directory paths)
            - A list containing dictionaries with main_dir as key and list of sub_dirs as value
        gcp_manager: GCP Bucket Manager instance
        base_gcp_path: Base path in GCP bucket
        include_date: Whether to include date in the destination path
       
    Returns:
        bool: True if all uploads were successful, False otherwise
    """
    try:
        # Get the current date for directory structure
        date = datetime.now().strftime("%Y%m%d") if include_date else ""
        
        # Handle single path case
        if isinstance(source_paths, str):
            paths_to_process = [(source_paths, None)]  # (main_dir, sub_dir)
        else:
            # Initialize list to store (main_dir, sub_dir) tuples
            paths_to_process = []
            
            # Process each item in the list
            for item in source_paths:
                if isinstance(item, str):
                    # Simple directory path
                    paths_to_process.append((item, None))
                elif isinstance(item, dict):
                    # Nested directory structure {main_dir: [sub_dir1, sub_dir2, ...]}
                    for main_dir, sub_dirs in item.items():
                        for sub_dir in sub_dirs:
                            paths_to_process.append((main_dir, sub_dir))
        
        all_success = True
        
        # Process each directory path
        for main_dir, sub_dir in paths_to_process:
            # Construct the full path
            if sub_dir:
                full_path = os.path.join("cron_jobs/aquire_data", main_dir, sub_dir)
            else:
                full_path = os.path.join("cron_jobs/aquire_data", main_dir)
            
            print(f"Processing directory: {full_path}")
            
            # Get the absolute path
            abs_source_path = os.path.abspath(full_path)
            
            if not os.path.exists(abs_source_path):
                print(f"Warning: Path does not exist: {abs_source_path}")
                all_success = False
                continue
                
            # Walk through the directory and all subdirectories
            for root, _, files in os.walk(abs_source_path):
                # Get the relative path from the source directory
                rel_path = os.path.relpath(root, os.path.dirname(abs_source_path))
                
                # For subdirectories, use the sub_dir name in the GCS path
                # This preserves the logical structure rather than the physical one
                if sub_dir:
                    gcs_rel_path = sub_dir if rel_path == sub_dir else f"{sub_dir}/{date}/{os.path.relpath(root, abs_source_path)}"
                else:
                    gcs_rel_path = f"{rel_path}/{date}"
               
                # Process files in the current directory
                for file in files:
                    # Only process CSV and JSON files
                    if file.lower().endswith(('.csv', '.json')):
                        local_file_path = os.path.join(root, file)
                    
                        # Construct the destination path in GCP
                        if include_date:
                            gcp_path = f"{base_gcp_path}/{gcs_rel_path}/{file}"
                        else:
                            gcp_path = f"{base_gcp_path}/{gcs_rel_path}/{file}"
                    
                        # Upload file based on its extension
                        try:
                            if file.lower().endswith('.csv'):
                                gcp_manager.upload_file_directly(local_file_path, gcp_path, "text/csv")
                            elif file.lower().endswith('.json'):
                                gcp_manager.upload_file_directly(local_file_path, gcp_path, "application/json")
                        
                            print(f"Uploaded {local_file_path} to {gcp_path}")
                        except Exception as e:
                            print(f"Failed to upload {local_file_path}: {str(e)}")
                            all_success = False
       
        return all_success
   
    except Exception as e:
        print(f"Error in GCP directory upload: {str(e)}")
        return False


config = load_config()
# Initialize GCP manager once
gcp_manager = GCPBucketManager(
    bucket_name="s-locator",
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
    # {"saudi_census": [
    #     # "population",
    #       "housing", 
    #       "household"
    #       ]},
    {"temp_test_dir": [
        "sub1",
        "sub2",
        # "sub3"
    ]},
    "temp_test_dir_2"
    ]

upload_success = upload_directory_to_gcp(directories, gcp_manager)
