from datetime import datetime
from google.cloud import storage
from google.oauth2 import service_account
import json
from typing import Optional, Dict, Any, List
import os
import glob

class GCPBucketManager:
    def __init__(self, bucket_name: str, credentials_path: str):
        """
        Initialize GCP Bucket connection
        
        Args:
            bucket_name (str): Name of the GCP bucket
            credentials_path (str): Path to service account JSON credentials file
        """
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.storage_client = storage.Client(credentials=self.credentials)
        self.bucket = self.storage_client.bucket(bucket_name)

    def list_files(self, prefix: Optional[str] = None) -> List[str]:
        """
        List all files in bucket, optionally filtered by prefix
        
        Args:
            prefix (str, optional): Filter files by prefix/folder path
            
        Returns:
            List[str]: List of file names in the bucket
        """
        blobs = self.bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]

    def read_json(self, file_path: str) -> Dict[str, Any]:
        """
        Read JSON file from bucket
        
        Args:
            file_path (str): Path to file in bucket
            
        Returns:
            dict: Parsed JSON data
        """
        try:
            blob = self.bucket.blob(file_path)
            content = blob.download_as_text()
            return json.loads(content)
        except Exception as e:
            raise Exception(f"Error reading JSON from {file_path}: {str(e)}")


    def save_json(self, data: dict, file_path: str) -> None:
        try:
            blob = self.bucket.blob(file_path)
            blob.upload_from_string(
                json.dumps(data, indent=2),
                content_type='application/json'
            )
            print(f"Successfully saved JSON to {file_path}")
        except Exception as e:
            raise Exception(f"Error saving JSON to {file_path}: {str(e)}")

    def read_file_as_bytes(self, file_path: str) -> bytes:
        """
        Read any file as bytes from bucket
        
        Args:
            file_path (str): Path to file in bucket
            
        Returns:
            bytes: File content as bytes
        """
        try:
            blob = self.bucket.blob(file_path)
            return blob.download_as_bytes()
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {str(e)}")


def upload_json_to_gcp(directories: List[str], gcp_manager: GCPBucketManager) -> bool:
    """
    Upload JSON files to Google Cloud Storage bucket using provided GCPBucketManager instance
    """
    try:
        # Get current timestamp for folder organization
        date = datetime.now().strftime("%Y%m%d")

        for directory in directories:
            # Get all JSON files in the directory
            json_files = glob.glob(os.path.join(directory, "*.json"))

            for json_file in json_files:
                try:
                    # Read JSON file
                    with open(json_file, "r", encoding="utf-8") as f:
                        json_data = json.load(f)

                    # Create GCS path: bucket/timestamp/database/schema/table/file.json
                    file_name = os.path.basename(json_file)
                    gcs_path = f"{directory}/{date}/raw_data/{file_name}"

                    # Upload file to GCS using our manager
                    gcp_manager.save_json(json_data, gcs_path)

                    print(f"Successfully uploaded {json_file} to {gcs_path}")

                except Exception as file_error:
                    print(f"Error uploading file {json_file}: {str(file_error)}")
                    continue

        return True

    except Exception as e:
        print(f"Error in GCP upload: {str(e)}")
        return False