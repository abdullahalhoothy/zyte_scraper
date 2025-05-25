import os
import json

# COLUMN_MAPPING specific to housing - MUST BE POPULATED CORRECTLY
COLUMN_MAPPING_HOUSING = {
    # Raw keys from API
    'MAIN_ID': 'Main_ID',
    'GID': 'Grid_ID',
    'H_DWLG_CNT': "Total_Dwelling", 
    'H_DWLG_T_RID': "Residential_Dwelling",
    'H_DWLG_T_COM': "Other_Residential_Dwelling", 
    'H_OWNED_RID_H_CNT': "Owned_Residential_Dwelling",
    'H_RENTED_RID_H_CNT': "Rented_Residential_Dwelling",
    'H_PROV_RID_H_CNT': "Provided_Residential_Dwelling", 
    'H_OTH_RID_H_CNT': "Non_Residential_Dwelling", 
    'H_DWLG_T_COM_PUB': "Public_Housing",
    'H_DWLG_T_COM_WRK': "Work_Camps",
    'H_DWLG_T_COM_COMM': "Commercial_Dwelling",
    'H_DWLG_OTH': "Other_Dwelling",
    # Keys from *_all_features.json (output of step1)
    'level': 'Level',
    # main_id, gid are already desired form from step1 extractor
    'main_id': 'Main_ID', 
    'gid': 'Grid_ID',
    # Other specific fields from step1 extractor if their keys need mapping
    # These are redundant if the key in all_features.json is already the target value,
    # but harmless due to .get(k,k)
    'H_DWLG_CNT': 'Total_Dwelling',
    'H_DWLG_T_RID': 'Residential_Dwelling',
    'H_DWLG_T_COM': 'Other_Residential_Dwelling',
    'H_OWNED_RID_H_CNT': 'Owned_Residential_Dwelling',
    'H_RENTED_RID_H_CNT': 'Rented_Residential_Dwelling',
    'H_PROV_RID_H_CNT': 'Provided_Residential_Dwelling',
    'H_OTH_RID_H_CNT': 'Non_Residential_Dwelling',
    'H_DWLG_T_COM_PUB': 'Public_Housing',
    'H_DWLG_T_COM_WRK': 'Work_Camps',
    'H_DWLG_T_COM_COMM': 'Commercial_Dwelling',
    'H_DWLG_OTH': 'Other_Dwelling',
    'centroid_lat': 'Latitude',
    'centroid_lon': 'Longitude'
}

def update_keys(data, column_mapping):
    # Identical to household's update_keys function
    if isinstance(data, dict) and "features" in data: 
        for feature in data.get("features", []):
            if "properties" in feature:
                updated_props = {}
                for k, v in feature["properties"].items():
                    updated_key = column_mapping.get(k.upper(), k) 
                    updated_props[updated_key] = v
                feature["properties"] = updated_props
    elif isinstance(data, list): 
        for i, item in enumerate(data):
            if isinstance(item, dict):
                updated_item = {}
                for k, v in item.items():
                    updated_key = column_mapping.get(k, k) 
                    updated_item[updated_key] = v
                data[i] = updated_item
    return data

def process_json_files(folder_path, all_features_file_path, column_mapping):
    # Identical to household's process_json_files function
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
    json_folder = os.path.join(current_script_dir, "housing_json_files")
    all_features_file = os.path.join(current_script_dir, "housing_all_features.json")

    print(f"Starting key renaming for housing data...")
    process_json_files(json_folder, all_features_file, COLUMN_MAPPING_HOUSING)
    print("Housing key renaming process completed.")
