import os
import json
import random
from collections import defaultdict


def update_keys(data, column_mapping):
    """Update keys in the data based on the provided column mapping."""
    for feature in data.get("features", []):
        if "properties" in feature:
            updated_props = {}
            for k, v in feature["properties"].items():
                # Use .upper() on the original key for case-insensitive matching with column_mapping
                updated_key = column_mapping.get(k.upper(), k)
                updated_props[updated_key] = v
            feature["properties"] = updated_props
    return data


def process_json_files(folder_path, column_mapping, primary_density_key, fallback_density_key=None):
    """
    Update keys in ALL JSON files and calculate normalized density based on available data.
    Normalization is done per zoom level (0-100 scale based on min/max within each level).
    
    Args:
        folder_path (str): Path to the folder containing JSON files
        column_mapping (dict): Dictionary mapping original keys to new keys (keys should be uppercase)
        primary_density_key (str): The primary key to use for density calculation (after mapping)
        fallback_density_key (str, optional): Fallback key if primary key has no valid values
    """
    if fallback_density_key is None:
        fallback_density_key = primary_density_key
    
    # First pass: collect all data and organize by zoom level
    files_data = {}
    zoom_level_values = defaultdict(list)  # zoom_level -> list of values
    
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith("json"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    updated_data = update_keys(data, column_mapping)
                    
                    # Determine which key to use for density calculation
                    key_for_density_calculation = primary_density_key
                    features_list = updated_data.get("features", [])
                    
                    if features_list:
                        # Sample to check if primary key has valid values
                        sample_size = min(50, len(features_list))
                        sampled_features = random.sample(features_list, k=sample_size)
                        has_primary_key = any(
                            feature.get("properties", {}).get(primary_density_key) is not None
                            for feature in sampled_features
                        )
                        
                        if not has_primary_key and fallback_density_key != primary_density_key:
                            key_for_density_calculation = fallback_density_key
                            print(f"Info: In '{file_path}', using fallback key '{fallback_density_key}'.")
                    
                    # Store file data for second pass
                    files_data[file_path] = {
                        'data': updated_data,
                        'density_key': key_for_density_calculation
                    }
                    
                    # Collect values by zoom level
                    for feature in features_list:
                        properties = feature.get("properties", {})
                        zoom_level = properties.get("Level")
                        density_value_str = properties.get(key_for_density_calculation)
                        
                        if zoom_level is not None and density_value_str is not None:
                            try:
                                density_value = float(density_value_str)
                                zoom_level_values[zoom_level].append(density_value)
                            except ValueError:
                                pass  # Skip invalid values
                    
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    # Calculate min/max for each zoom level
    zoom_level_ranges = {}
    for zoom_level, values in zoom_level_values.items():
        if values:
            zoom_level_ranges[zoom_level] = {
                'min': min(values),
                'max': max(values)
            }
            print(f"Zoom Level {zoom_level}: min={zoom_level_ranges[zoom_level]['min']}, max={zoom_level_ranges[zoom_level]['max']}, count={len(values)}")
    
    # Second pass: normalize and write files
    for file_path, file_info in files_data.items():
        try:
            updated_data = file_info['data']
            key_for_density_calculation = file_info['density_key']
            features_list = updated_data.get("features", [])
            
            if features_list:
                # Normalize density for each feature based on its zoom level
                for feature in features_list:
                    properties = feature.get("properties", {})
                    zoom_level = properties.get("Level")
                    current_value_str = properties.get(key_for_density_calculation)
                    normalized_density_value = 0.0
                    
                    if (zoom_level is not None and 
                        current_value_str is not None and 
                        zoom_level in zoom_level_ranges):
                        
                        try:
                            current_value_float = float(current_value_str)
                            min_val = zoom_level_ranges[zoom_level]['min']
                            max_val = zoom_level_ranges[zoom_level]['max']
                            
                            if max_val == min_val:
                                # All values at this zoom level are the same
                                normalized_density_value = 0.0  # Middle value
                            else:
                                # Normalize to 0-100 scale
                                normalized_density_value = (
                                    (current_value_float - min_val) / (max_val - min_val)
                                ) * 100
                            
                            properties["density"] = round(normalized_density_value, 4)
                        except ValueError:
                            properties["density"] = 0.0
                    else:
                        properties["density"] = 0.0
                    
                    feature["properties"] = properties
                
                print(f"Processed: {file_path}. Keys updated. Density normalized by zoom level using '{key_for_density_calculation}'.")
            else:
                print(f"Info: No features found in {file_path}. Only top-level keys updated.")
            
            # Write back to the SAME file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")