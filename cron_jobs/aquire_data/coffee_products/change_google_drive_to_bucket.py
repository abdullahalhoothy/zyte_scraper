import pandas as pd
from google.cloud import storage
from google.oauth2 import service_account
import requests
import os
from urllib.parse import urlparse, parse_qs
import logging
from tqdm import tqdm
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_url_update.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_google_cloud():
    """Setup Google Cloud Storage client"""
    logger.info("Setting up Google Cloud Storage connection...")
    try:
        credentials = service_account.Credentials.from_service_account_file(
            'cron_jobs/secret_weighty-gasket-437422-h6-c961161f5668.json'
        )
        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.bucket('vivi_app')
        logger.info("Successfully connected to Google Cloud Storage")
        return bucket
    except Exception as e:
        logger.error(f"Failed to setup Google Cloud Storage: {str(e)}")
        raise

def get_file_id_from_drive_link(url):
    """Extract file ID from Google Drive link"""
    try:
        parsed = urlparse(url)
        if parsed.hostname in ['drive.google.com', 'www.drive.google.com']:
            if 'id=' in parsed.query:
                return parse_qs(parsed.query)['id'][0]
            else:
                return parsed.path.split('/')[-2]
    except Exception as e:
        logger.error(f"Error extracting file ID from URL {url}: {str(e)}")
    return None

def list_all_gcs_images(bucket):
    """Get a list of all images in the GCS bucket"""
    base_gcs_path = 'postgreSQL/dbo-coffee/raw_schema_marketplace/product_images'
    prefix = f"{base_gcs_path}/"
    
    image_list = []
    try:
        blobs = list(bucket.list_blobs(prefix=prefix))
        blobs.sort(key=lambda x: x.name)  # Sort blobs by name
        
        for blob in blobs:
            if blob.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                gcs_url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"
                image_list.append(gcs_url)
                
        logger.info(f"Found {len(image_list)} images in GCS bucket")
        return image_list
    except Exception as e:
        logger.error(f"Error listing images in GCS bucket: {str(e)}")
        return []

def process_csv():
    logger.info("Starting CSV processing")
    
    # Initialize Google Cloud Storage
    bucket = setup_google_cloud()
    
    # Get list of all GCS images
    gcs_images = list_all_gcs_images(bucket)
    if not gcs_images:
        logger.error("No images found in GCS bucket")
        return
    
    # Track current image index
    current_image_index = 0
    total_gcs_images = len(gcs_images)
    
    # Try different encodings
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    df = None
    
    # Read CSV file
    logger.info("Attempting to read CSV file...")
    for encoding in encodings:
        try:
            df = pd.read_csv('cron_jobs/aquire_data/coffee_products/productssmal.csv', encoding=encoding)
            logger.info(f"Successfully read CSV with {encoding} encoding")
            break
        except UnicodeDecodeError:
            logger.warning(f"Failed to read CSV with {encoding} encoding")
            continue
    
    if df is None:
        logger.error("Could not read CSV file with any of the attempted encodings")
        raise Exception("Could not read CSV file with any of the attempted encodings")

    # Get total number of rows for progress tracking
    total_rows = len(df)
    logger.info(f"Processing {total_rows} rows in CSV file")
    
    # Initialize counters for statistics
    updated_urls = 0
    failed_urls = 0
    
    # Process Image 1 Link and Image 2 Link columns
    for idx, row in tqdm(df.iterrows(), total=total_rows, desc="Processing rows"):
        for col in ['Image 1 Link', 'Image 2 Link']:
            if pd.notna(row[col]) and current_image_index < total_gcs_images:
                drive_url = row[col]
                logger.debug(f"Processing {col} for row {idx + 1}/{total_rows}")
                
                # Update with next GCS image URL
                df.at[idx, col] = gcs_images[current_image_index]
                logger.info(f"Updated {col} in row {idx + 1} with image {current_image_index + 1}/{total_gcs_images}")
                current_image_index += 1
                updated_urls += 1
            else:
                failed_urls += 1
                logger.warning(f"No more GCS images available for row {idx + 1}, {col}")

        # Log progress every 10 rows
        if (idx + 1) % 10 == 0:
            progress = (idx + 1) / total_rows * 100
            logger.info(f"Progress: {progress:.2f}% ({idx + 1}/{total_rows} rows processed)")

    # Save the updated CSV
    logger.info("Saving updated CSV file...")
    try:
        df.to_csv('cron_jobs/aquire_data/coffee_products/updated_products.csv', index=False, encoding=encoding)
        logger.info("Successfully saved updated CSV file")
    except Exception as e:
        logger.error(f"Failed to save updated CSV: {str(e)}")
        raise

    # Log final statistics
    logger.info(f"""
    Processing completed:
    - Total rows processed: {total_rows}
    - URLs successfully updated: {updated_urls}
    - Failed URL updates: {failed_urls}
    - Success rate: {(updated_urls/(updated_urls + failed_urls) * 100):.2f}%
    """)

if __name__ == "__main__":
    start_time = time.time()
    try:
        process_csv()
        execution_time = time.time() - start_time
        logger.info(f"Script completed successfully in {execution_time:.2f} seconds")
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Script failed after {execution_time:.2f} seconds: {str(e)}")
        raise