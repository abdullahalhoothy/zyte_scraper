import requests
import json
import csv
import os
import numpy as np
from datetime import datetime
import logging
import urllib3
from time import sleep

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(MODULE_DIR, "population.log")
logging.basicConfig(level=logging.INFO, filename=log_file_path, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COLUMN_MAPPING = {
    'level': 'Level',
    'main_id': 'Main_ID',
    'gid': 'Grid_ID',
    'pcnt': 'Population_Count',
    'pm_cnt': 'Male_Population',
    'pf_cnt': 'Female_Population',
    'pden_km2': 'Population_Density_KM2',
    'ymed_age': 'Median_Age_Total',
    'ymed_age_m': 'Median_Age_Male',
    'ymed_age_fm': 'Median_Age_Female',
    'centroid_lat': 'Latitude',
    'centroid_lon': 'Longitude'
}

def calculate_centroid(coordinates):
    """Calculate the centroid of a polygon using NumPy."""
    if not coordinates or not coordinates[0]:
        return None, None
    
    points = np.array(coordinates[0])
    longitude = np.mean(points[:, 0])
    latitude = np.mean(points[:, 1])
    
    return latitude, longitude

def fetch_with_pagination(url, params, max_retries=3):
    """Fetch data with pagination and retry logic."""
    all_features = []
    offset = 0
    result_limit = 1000  # Adjust this value based on server limitations
    
    while True:
        current_params = params.copy()
        current_params.update({
            'resultOffset': offset,
            'resultRecordCount': result_limit
        })
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=current_params, verify=False, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                features = data.get('features', [])
                all_features.extend(features)
                
                # Check if we've received all features
                if len(features) < result_limit:
                    return all_features
                
                offset += result_limit
                # Add a small delay between requests to avoid overwhelming the server
                sleep(0.5)
                break
                
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    logging.error(f"Failed after {max_retries} attempts: {str(e)}")
                    return all_features
                logging.warning(f"Attempt {attempt + 1} failed, retrying...")
                sleep(2 ** attempt)  # Exponential backoff
    
    return all_features

def process_census_data(level):
    """Fetch and process census data for a specific level."""
    base_url = f"https://maps.saudicensus.sa/arcgis/rest/services/results_grid_pop_v{level}/FeatureServer/0/query"
    params = {
        'where': '1=1',
        'outFields': '*',
        'returnGeometry': 'true',
        'f': 'geojson'
    }
    
    try:
        logging.info(f"Fetching data for level {level}...")
        features = fetch_with_pagination(base_url, params)
        
        if not features:
            logging.warning(f"No features found for level {level}")
            return []        
        
        # Process features
        processed_features = []
        
        for feature in features:
            centroid_lat, centroid_lon = calculate_centroid(feature['geometry']['coordinates'])
            
            processed_feature = {
                'level': level,
                'main_id': feature['properties'].get('MAIN_ID'),
                'gid': feature['properties'].get('GID'),
                'pcnt': feature['properties'].get('PCNT'),
                'pm_cnt': feature['properties'].get('PM_CNT'),
                'pf_cnt': feature['properties'].get('PF_CNT'),
                'pden_km2': feature['properties'].get('PDEN_KM2'),
                'ymed_age': feature['properties'].get('YMED_AGE'),
                'ymed_age_m': feature['properties'].get('YMED_AGE_M'),
                'ymed_age_fm': feature['properties'].get('YMED_AGE_FM'),
                'centroid_lat': centroid_lat,
                'centroid_lon': centroid_lon
            }
            
            processed_features.append(processed_feature)
        
        logging.info(f"Successfully processed {len(processed_features)} features for level {level}")
        return processed_features
    
    except Exception as e:
        logging.error(f"Error processing level {level}: {str(e)}")
        return []

# The save_to_csv and main functions remain the same as in your original code

def save_to_csv(features, filename, fieldnames):
    """Save features to CSV with mapped column names"""
    
    filename = os.path.join(MODULE_DIR, filename)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[COLUMN_MAPPING[field] for field in fieldnames])
        
        # Write header
        writer.writeheader()
        
        # Write rows with mapped field names
        for feature in features:
            mapped_feature = {COLUMN_MAPPING[k]: v for k, v in feature.items() if k in fieldnames}
            writer.writerow(mapped_feature)

def main():
    # Process levels 8 through 14
    logging.info("Processing levels 8 through 14...")
    # END: abpxx6d04wxr

    all_features = []
    for level in range(8, 17):
        logging.info(f"Processing level {level}...")
        features = process_census_data(level)
        all_features.extend(features)

    # Convert to numpy array for faster processing
    if all_features:
        # Save all data to CSV
        csv_fields = [
            'level', 'main_id', 'gid', 'pcnt', 'pm_cnt', 
            'pf_cnt', 'pden_km2', 'ymed_age', 'ymed_age_m', 'ymed_age_fm',
            'centroid_lat', 'centroid_lon'
        ]

        # Create separate CSV files for each level
        features_by_level = {}
        for feature in all_features:
            level = feature['level']
            if level not in features_by_level:
                features_by_level[level] = []
            features_by_level[level].append(feature)

        # Save level-specific CSV files with mapped column names
        # for level, features in features_by_level.items():
        #     save_to_csv(features, f'census_data_level_{level}.csv', csv_fields)
        
        # Save combined CSV with mapped column names
        save_to_csv(all_features, 'population.csv', csv_fields)

        logging.info(f"Processing complete. Processed {len(all_features)} features.")
        logging.info("Files saved:")
        logging.info("- Level-specific CSV files: census_data_level_{8-14}.csv")
        logging.info("- Combined data in 'population.csv'")

        # Print summary statistics using numpy
        features_array = np.array([(f['level'], f['level'], f['pcnt'])
                                   for f in all_features if f['pcnt'] is not None])
        if len(features_array) > 0:
            logging.info("\nSummary Statistics:")
            for level in range(8, 17):
                level_data = features_array[features_array[:, 1] == level]
                if len(level_data) > 0:
                    logging.info(f"\nLevel {level}:")
                    logging.info(f"  Count: {len(level_data)}")
                    logging.info(f"  Mean population: {np.mean(level_data[:, 2]):.2f}")
                    logging.info(f"  Min population: {np.min(level_data[:, 2]):.2f}")
                    logging.info(f"  Max population: {np.max(level_data[:, 2]):.2f}")
    else:
        logging.info("No data was processed successfully.")


if __name__ == "__main__":
    main()


