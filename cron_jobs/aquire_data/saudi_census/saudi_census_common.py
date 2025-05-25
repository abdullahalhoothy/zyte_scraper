import requests
import json
import csv
import os
import numpy as np
from datetime import datetime
import logging
import urllib3
from time import sleep

def setup_logging(module_dir, entity_type):
    """Configures logging and disables urllib3 warnings."""
    log_file_path = os.path.join(module_dir, f"{entity_type}.log")
    logging.basicConfig(level=logging.INFO, filename=log_file_path, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def calculate_centroid(coordinates):
    """Calculate the centroid of a polygon using NumPy."""
    if not coordinates or not isinstance(coordinates, list) or not coordinates[0]:
        return None, None
    
    # Ensure coordinates[0] is a list of points
    if not isinstance(coordinates[0], list) or len(coordinates[0]) == 0:
        return None, None
        
    points = np.array(coordinates[0])
    # Ensure points is a 2D array with at least one point and two dimensions
    if points.ndim != 2 or points.shape[1] != 2:
        # Attempt to handle cases where coordinates might be wrapped deeper
        if len(coordinates) == 1 and isinstance(coordinates[0], list) and len(coordinates[0]) > 0 and isinstance(coordinates[0][0], list):
             points = np.array(coordinates[0][0])
             if points.ndim != 2 or points.shape[1] != 2:
                logging.warning(f"Unexpected coordinate structure for centroid calculation: {coordinates}")
                return None, None
        else:
            logging.warning(f"Unexpected coordinate structure for centroid calculation: {coordinates}")
            return None, None

    longitude = np.mean(points[:, 0])
    latitude = np.mean(points[:, 1])
    
    return latitude, longitude

def fetch_with_pagination(url, params, max_retries=3):
    """Fetch data with pagination and retry logic."""
    all_features = []
    offset = 0
    result_limit = 10000  # Adjust this value based on server limitations
    
    while True:
        current_params = params.copy()
        current_params.update({
            'resultOffset': offset,
            'resultRecordCount': result_limit
        })
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=current_params, verify=False, timeout=60) # Increased timeout
                response.raise_for_status()
                data = response.json()
                
                features = data.get('features', [])
                all_features.extend(features)
                
                # Check if we've received all features
                if not features or len(features) < result_limit: # also check if features is empty
                    return all_features
                
                offset += result_limit # Correctly increment offset
                # Add a small delay between requests to avoid overwhelming the server
                sleep(0.5)
                break # Break from retry loop on success
                
            except requests.exceptions.RequestException as e:
                logging.warning(f"Attempt {attempt + 1} for URL {url} with offset {current_params.get('resultOffset')} failed: {str(e)}")
                if attempt == max_retries - 1:
                    logging.error(f"Failed after {max_retries} attempts for URL {url} with offset {current_params.get('resultOffset')}: {str(e)}")
                    return all_features # Return what has been collected so far
                sleep(2 ** attempt)  # Exponential backoff
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error for URL {url} with offset {current_params.get('resultOffset')}: {str(e)}. Response text: {response.text[:200]}")
                if attempt == max_retries -1:
                    return all_features # Return what has been collected so far
                sleep(2 ** attempt)


def process_census_data_generic(level, module_dir, entity_type, base_url_template_part, specific_fields_extractor):
    """Fetch and process census data for a specific level generically."""
    base_url = f"https://maps.saudicensus.sa/arcgis/rest/services/results_grid_{base_url_template_part}_v{level}/FeatureServer/0/query"
    params = {
        'where': '1=1',
        'outFields': '*',
        'returnGeometry': 'true',
        'f': 'geojson'
    }
    
    logging.info(f"Fetching data for {entity_type} level {level} from {base_url}")
    features = fetch_with_pagination(base_url, params)
    
    if not features:
        logging.warning(f"No features found for {entity_type} level {level}")
        return []
    
    # Create directory for JSON files
    json_files_path = os.path.join(module_dir, f"{entity_type}_json_files")
    level_json_path = os.path.join(json_files_path, f'v{level}')
    os.makedirs(level_json_path, exist_ok=True)
    
    processed_features = []
    
    for feature_idx, feature in enumerate(features):
        try:
            geometry = feature.get('geometry')
            coordinates = geometry.get('coordinates') if geometry else None
            centroid_lat, centroid_lon = calculate_centroid(coordinates)
            
            properties = feature.get('properties', {})
            extracted_props = specific_fields_extractor(properties)
            
            processed_feature = {
                'level': level,
                'main_id': properties.get('MAIN_ID'),
                'gid': properties.get('GID'),
                'centroid_lat': centroid_lat,
                'centroid_lon': centroid_lon,
                **extracted_props # Unpack extracted properties
            }
            
            processed_features.append(processed_feature)
        except Exception as e:
            logging.error(f"Error processing feature {feature_idx} in level {level} for {entity_type}: {e}. Feature data: {feature}")
            # Optionally, append a record with error info or skip
            continue

    # Save original fetched features for this level
    raw_features_output_path = os.path.join(level_json_path, 'features.json')
    try:
        output_json_raw = {
            'type': 'FeatureCollection',
            'features': features # Save the original, unmodified features
        }
        with open(raw_features_output_path, 'w') as f:
            json.dump(output_json_raw, f, indent=2)
        logging.info(f"Saved raw features for {entity_type} level {level} to {raw_features_output_path}")
    except Exception as e:
        logging.error(f"Error saving raw features for {entity_type} level {level} to {raw_features_output_path}: {e}")

    logging.info(f"Successfully processed {len(processed_features)} features for {entity_type} level {level}")
    return processed_features

def main_step1_runner(module_dir, entity_type, base_url_template_part, column_mapping, specific_fields_extractor):
    """Main runner for step 1 of data acquisition."""
    setup_logging(module_dir, f"{entity_type}_step1") # Setup logging for step1
    logging.info(f"Starting step 1 for {entity_type}: Data Fetching and Processing.")

    all_features = []
    for level in range(8, 17): # As per typical range observed
        logging.info(f"Processing {entity_type} data for level {level}...")
        features_for_level = process_census_data_generic(
            level, 
            module_dir, 
            entity_type, 
            base_url_template_part, 
            specific_fields_extractor
        )
        all_features.extend(features_for_level)

    if all_features:
        output_filename = f"{entity_type}_all_features.json"
        output_path = os.path.join(module_dir, output_filename)
        try:
            with open(output_path, 'w') as f:
                json.dump(all_features, f, indent=2)
            logging.info(f"All processed {entity_type} features saved to {output_path}")
        except Exception as e:
            logging.error(f"Error saving all_features for {entity_type} to {output_path}: {e}")
    else:
        logging.info(f"No data was processed for {entity_type}.")
    logging.info(f"Step 1 for {entity_type} completed.")

# Example of a specific_fields_extractor function that would be defined in the calling script:
# def household_specific_fields_extractor(properties):
# return {
# 'HHAVG': properties.get('HHAVG'),
# 'HHMED': properties.get('HHMED'),
#     }

# Example of COLUMN_MAPPING that would be defined in the calling script:
# HOUSEHOLD_COLUMN_MAPPING = {
#     'LEVEL': 'Level',
#     'MAIN_ID': 'Main_ID',
#     'GID': 'Grid_ID',
#     "HHAVG": "Household_Average",
#     "HHMED": "Household_Median",
#     # Add other specific mappings here
#     'CENTROID_LAT': 'Latitude', # Example, though lat/lon are handled separately
#     'CENTROID_LON': 'Longitude' # Example
# }
