import os
import json

# Mapping for renaming keys in the properties section
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
    """Update keys in each features.json and rename to all_features.json in subfolders."""
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower() == "features.json":
                full_path = os.path.join(root, file)
                new_path = os.path.join(root, "all_features.json")
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    updated_data = update_keys(data)

                    with open(new_path, "w", encoding="utf-8") as f:
                        json.dump(updated_data, f, ensure_ascii=False, indent=2)

                    os.remove(full_path)  # delete original features.json

                    print(f"Updated and renamed: {full_path} → {new_path}")
                except Exception as e:
                    print(f"Failed to process {full_path}: {e}")

if __name__ == "__main__":
    json_folder = os.path.join(os.path.dirname(__file__), "population_json_files")
    process_json_files(json_folder)
