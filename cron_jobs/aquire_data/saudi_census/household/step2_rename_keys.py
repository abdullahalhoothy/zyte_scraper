import os
import json

# COLUMN_MAPPING specific to household - MUST BE POPULATED CORRECTLY
# This should match the keys used in household_all_features.json (output of step1)
# and the raw keys in household_json_files/v{level}/features.json (properties)
COLUMN_MAPPING_HOUSEHOLD = {
    # Raw keys from the API (usually uppercase) mapped to desired final keys
    # Example: 'MAIN_ID': 'Main_ID', 'GID': 'Grid_ID', (these are common)
    # From household step1:
    'HHAVG': 'Household_Average',
    'HHMED': 'Household_Median',
    # Need to include mappings for 'level', 'main_id', 'gid', 'centroid_lat', 'centroid_lon'
    # if they are present in the *_all_features.json with different casing/names
    # than what's desired, or if they appear in the raw features.json properties.
    # For properties in features.json (raw data from API):
    'MAIN_ID': 'Main_ID', # Assuming these are standard from API
    'GID': 'Grid_ID',     # Assuming these are standard from API
    # For keys in household_all_features.json (processed by step1 extractor):
    'level': 'Level',
    'main_id': 'Main_ID', # Already desired form from step1 extractor
    'gid': 'Grid_ID',     # Already desired form from step1 extractor
    'HHAVG': 'Household_Average', # Already desired form from step1 extractor
    'HHMED': 'Household_Median', # Already desired form from step1 extractor
    'centroid_lat': 'Latitude',
    'centroid_lon': 'Longitude'
}

def update_keys(data, column_mapping):
    if isinstance(data, dict) and "features" in data: # For raw v{level}/features.json
        for feature in data.get("features", []):
            if "properties" in feature:
                updated_props = {}
                for k, v in feature["properties"].items():
                    updated_key = column_mapping.get(k.upper(), k) # API keys are often uppercase
                    updated_props[updated_key] = v
                feature["properties"] = updated_props
    elif isinstance(data, list): # For household_all_features.json
        for i, item in enumerate(data):
            if isinstance(item, dict):
                updated_item = {}
                for k, v in item.items():
                    # Keys in *_all_features.json are as defined by step1's processed_feature
                    updated_key = column_mapping.get(k, k) 
                    updated_item[updated_key] = v
                data[i] = updated_item
    return data

def process_json_files(folder_path, all_features_file_path, column_mapping):
    # Process files in subdirectories (like v{level}/features.json)
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('json'):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        jsonData = json.load(f)
                    updated_data = update_keys(jsonData, column_mapping)
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(updated_data, f, ensure_ascii=False, indent=2)
                    print(f"Updated keys for: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    # Process the all_features.json file directly
    if os.path.exists(all_features_file_path):
        try:
            with open(all_features_file_path, "r", encoding="utf-8") as f:
                jsonData = json.load(f)
            updated_data = update_keys(jsonData, column_mapping)
            with open(all_features_file_path, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)
            print(f"Updated keys for: {all_features_file_path}")
        except Exception as e:
            print(f"Error processing {all_features_file_path}: {e}")
    else:
        print(f"File not found: {all_features_file_path}, skipping.")

if __name__ == "__main__":
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    json_folder = os.path.join(current_script_dir, "household_json_files")
    all_features_file = os.path.join(current_script_dir, "household_all_features.json")
    
    print(f"Starting key renaming for household data...")
    process_json_files(json_folder, all_features_file, COLUMN_MAPPING_HOUSEHOLD)
    print("Household key renaming process completed.")
