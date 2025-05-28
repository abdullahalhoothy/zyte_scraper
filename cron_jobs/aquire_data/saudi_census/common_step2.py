import os
import json
import random


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
    
    Args:
        folder_path (str): Path to the folder containing JSON files
        column_mapping (dict): Dictionary mapping original keys to new keys (keys should be uppercase)
        primary_density_key (str): The primary key to use for density calculation (after mapping)
        fallback_density_key (str, optional): Fallback key if primary key has no valid values
    """
    if fallback_density_key is None:
        fallback_density_key = primary_density_key
    
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith("json"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    updated_data = update_keys(data, column_mapping)  # Keys are updated first

                    key_for_density_calculation = primary_density_key
                    source_key_name_for_print = primary_density_key

                    features_list = updated_data.get("features", [])
                    final_processing_message = ""

                    if features_list:
                        # Determine if primary density key is "present" with a non-null value in a sample
                        has_primary_key_with_value_in_sample = False
                        sample_size = min(50, len(features_list))

                        sampled_features = random.sample(features_list, k=sample_size)
                        for feature_in_sample in sampled_features:
                            properties_in_sample = feature_in_sample.get("properties", {})
                            if properties_in_sample.get(primary_density_key) is not None:
                                has_primary_key_with_value_in_sample = True
                                break

                        if not has_primary_key_with_value_in_sample and fallback_density_key != primary_density_key:
                            key_for_density_calculation = fallback_density_key
                            source_key_name_for_print = f"{fallback_density_key} (fallback)"
                            print(
                                f"Info: In '{file_path}', all '{primary_density_key}' are null values in sample. Using '{key_for_density_calculation}'."
                            )
                        else:
                            source_key_name_for_print = f"{primary_density_key} (found in sample)"
                            print(
                                f"Info: In '{file_path}', '{primary_density_key}' found with valid values in sample. Using '{key_for_density_calculation}'."
                            )

                        # Collect values for normalization from the chosen key across ALL features
                        values_for_normalization = []
                        for feature in features_list:
                            properties = feature.get("properties", {})
                            current_value_str = properties.get(key_for_density_calculation)
                            if current_value_str is not None:
                                try:
                                    values_for_normalization.append(float(current_value_str))
                                except ValueError:
                                    grid_id_info = properties.get("Grid_ID", "N/A")
                                    print(
                                        f"Warning: Could not convert {key_for_density_calculation} '{current_value_str}' to float in '{file_path}' for feature GID '{grid_id_info}'. Skipping this value for normalization."
                                    )

                        min_val = 0.0
                        max_val = 0.0
                        if values_for_normalization:
                            min_val = min(values_for_normalization)
                            max_val = max(values_for_normalization)
                        elif features_list:
                            print(
                                f"Warning: No valid numeric values found for '{key_for_density_calculation}' in '{file_path}'. All 'density' values will be 0.0."
                            )

                        # Calculate and add normalized "density" property to each feature
                        for feature in features_list:
                            properties = feature.get("properties", {})
                            current_value_str = properties.get(key_for_density_calculation)
                            normalized_density_value = 0.0

                            if current_value_str is not None and values_for_normalization:
                                try:
                                    current_value_float = float(current_value_str)
                                    if max_val == min_val:
                                        normalized_density_value = 0.0
                                    else:
                                        normalized_density_value = (
                                            (current_value_float - min_val) / (max_val - min_val)
                                        ) * 100
                                    properties["density"] = round(normalized_density_value, 4)
                                except ValueError:
                                    properties["density"] = 0.0
                            else:
                                properties["density"] = 0.0

                            feature["properties"] = properties

                        final_processing_message = f"Processed: {file_path}. Keys updated. Density calculated from '{source_key_name_for_print}'."

                    else:
                        print(f"Info: No features found in {file_path}. Only top-level keys (if any) updated via mapping.")
                        final_processing_message = f"Processed: {file_path}. Keys updated (no features for density calculation)."

                    # Write back to the SAME file
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(updated_data, f, ensure_ascii=False, indent=2)

                    print(final_processing_message)

                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")