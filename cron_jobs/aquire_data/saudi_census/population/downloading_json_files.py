from google.cloud import storage
import os
import logging

def download_json_files_recursive(bucket_name: str, source_prefix: str, destination_folder: str = ""):
    """Downloads all JSON files recursively from a specific path in a GCS bucket.

    Args:
        bucket_name: The name of the Google Cloud Storage bucket.
        source_prefix: The prefix (path) within the bucket to look for JSON files.
                       Ensure this ends with a '/'.
        destination_folder: The local folder where the files will be downloaded.
    """
    try:
        client = storage.Client.create_anonymous_client()
        bucket = client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=source_prefix)  
        destination_folder = os.path.join(os.path.dirname(__file__), "population_json_files")
        os.makedirs(destination_folder, exist_ok=True)

        for blob in blobs:
            # Only consider JSON files
            if blob.name.endswith("json"):
                relative_path = os.path.relpath(blob.name, source_prefix)
                destination_path = os.path.join(destination_folder, relative_path)
                if os.path.exists(destination_path):
                    print("skipped")
                    continue  # Skip downloading this file that already exist
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                
                try:
                    blob.download_to_filename(destination_path)
                    print(f"Downloaded: {blob.name} to {destination_path}")
                except Exception as e:
                    if os.path.exists(destination_path):
                        os.remove(destination_path)
    except Exception as e:
        logging.error(f"Error happens when fetching data : {str(e)}")

if __name__ == "__main__":
    bucket_name = "s-locator"  
    source_prefix = "misc/population_json_files/"  
    download_json_files_recursive(bucket_name, source_prefix)
