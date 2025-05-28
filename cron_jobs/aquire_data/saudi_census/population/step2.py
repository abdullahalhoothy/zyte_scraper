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

                    # Calculate and add normalized density
                    density_values = []
                    for feature in updated_data.get("features", []):
                        properties = feature.get("properties", {})
                        current_density_km2_val = properties.get('Population_Density_KM2')
                        if current_density_km2_val is not None:
                            try:
                                density_values.append(float(current_density_km2_val))
                            except ValueError:
                                print(f"Warning: Could not convert Population_Density_KM2 '{current_density_km2_val}' to float in {file_path} for feature {properties.get('Grid_ID', 'N/A')}")

                    min_density = 0.0
                    max_density = 0.0
                    if density_values:
                        min_density = min(density_values)
                        max_density = max(density_values)

                    for feature in updated_data.get("features", []):
                        properties = feature.get("properties", {})
                        current_density_km2_val = properties.get('Population_Density_KM2')
                        normalized_density = 0.0
                        if current_density_km2_val is not None and density_values: # ensure density_values is not empty
                            try:
                                current_density_float = float(current_density_km2_val)
                                if max_density == min_density:
                                    normalized_density = 0.0
                                else:
                                    normalized_density = ((current_density_float - min_density) / (max_density - min_density)) * 100
                                properties["density"] = round(normalized_density, 4)
                            except ValueError:
                                # This case should ideally be caught in the first loop, but as a safeguard:
                                properties["density"] = 0.0
                            except ZeroDivisionError: # Should be caught by max_density == min_density
                                properties["density"] = 0.0
                        else:
                            properties["density"] = 0.0
                        feature["properties"] = properties
                    
                    # Write back to the SAME file
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(updated_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"Updated keys and density for: {file_path}")
                
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    json_folder = os.path.join(os.path.dirname(__file__), "population_json_files")
    process_json_files(json_folder)
