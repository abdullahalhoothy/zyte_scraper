import os
import json

COLUMN_MAPPING = {
    'GLEVEL': 'Level',
    'MAIN_ID': 'Main_ID',
    'GID': 'Grid_ID',
    'PCNT': 'Population_Count',
    'PM_CNT': 'Male_Population',
    'PF_CNT': 'Female_Population',
    'PDEN_KM2': 'Population_Density_KM2',
    'YMED_AGE': 'Median_Age_Total',
    'YMED_AGE_M': 'Median_Age_Male',
    'YMED_AGE_FM': 'Median_Age_Female',
    'CENTROID_LAT': 'Latitude',
    'CENTROID_LON': 'Longitude'
}

def update_keys(data):
    for feature in data.get("features", []):
        if "properties" in feature:
            updated_props = {}
            for k, v in feature["properties"].items():
                updated_key = COLUMN_MAPPING.get(k.upper(), k)
                updated_props[updated_key] = v
            feature["properties"] = updated_props
    return data

def process_json_files(folder_path):
    """Update keys in ALL JSON files (keep original filenames)."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('json'):  # Process ALL JSON files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    updated_data = update_keys(data)
                    
                    # Write back to the SAME file
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(updated_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"Updated keys for: {file_path}")
                
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    json_folder = os.path.join(os.path.dirname(__file__), "population_json_files")
    process_json_files(json_folder)
