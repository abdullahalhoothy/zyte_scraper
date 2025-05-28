import os
import json
import random # For sampling features

COLUMN_MAPPING = {
    "GLEVEL": "Level",
    "MAIN_ID": "Main_ID",
    "GID": "Grid_ID",
    "PCNT": "Population_Count",
    "PM_CNT": "Male_Population",
    "PF_CNT": "Female_Population",
    "PDEN_KM2": "Population_Density_KM2",
    "YMED_AGE": "Median_Age_Total",
    "YMED_AGE_M": "Median_Age_Male",
    "YMED_AGE_FM": "Median_Age_Female",
    "CENTROID_LAT": "Latitude",
    "CENTROID_LON": "Longitude",
}


def update_keys(data):
    for feature in data.get("features", []):
        if "properties" in feature:
            updated_props = {}
            for k, v in feature["properties"].items():
                # Use .upper() on the original key for case-insensitive matching with COLUMN_MAPPING
                updated_key = COLUMN_MAPPING.get(k.upper(), k)
                updated_props[updated_key] = v
            feature["properties"] = updated_props
    return data


def process_json_files(folder_path):
    """Update keys in ALL JSON files and calculate normalized density based on available data."""
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith("json"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    updated_data = update_keys(data)  # Keys are updated first

                    key_for_density_calculation = (
                        "Population_Density_KM2"  # Default
                    )
                    source_key_name_for_print = (
                        "Population_Density_KM2"  # For logging
                    )

                    features_list = updated_data.get("features", [])
                    final_processing_message = ""

                    if features_list:
                        # Determine if 'Population_Density_KM2' is "present" with a non-null value in a sample
                        has_population_density_key_with_value_in_sample = False
                        sample_size = min(
                            50, len(features_list)
                        )  # Ensure sample size is not more than available features

                        sampled_features = random.sample(
                            features_list, k=sample_size
                        )
                        for feature_in_sample in sampled_features:
                            properties_in_sample = feature_in_sample.get(
                                "properties", {}
                            )
                            # Check the mapped key 'Population_Density_KM2' for a non-null value
                            if (
                                properties_in_sample.get(
                                    "Population_Density_KM2"
                                )
                                is not None
                            ):
                                has_population_density_key_with_value_in_sample = (
                                    True
                                )
                                break

                        if not has_population_density_key_with_value_in_sample:
                            key_for_density_calculation = (
                                "Population_Count"  # Fallback key
                            )
                            source_key_name_for_print = (
                                "Population_Count (fallback)"
                            )
                            print(
                                f"Info: In '{file_path}', all 'Population_Density_KM2' are null values in sample. Using '{key_for_density_calculation}'."
                            )
                        else:
                            source_key_name_for_print = (
                                "Population_Density_KM2 (found in sample)"
                            )
                            print(
                                f"Info: In '{file_path}', 'Population_Density_KM2' found with valid values in sample. Using '{key_for_density_calculation}'."
                            )

                        # Collect values for normalization from the chosen key across ALL features
                        values_for_normalization = []
                        for feature in features_list:
                            properties = feature.get("properties", {})
                            current_value_str = properties.get(
                                key_for_density_calculation
                            )
                            if current_value_str is not None:
                                try:
                                    values_for_normalization.append(
                                        float(current_value_str)
                                    )
                                except ValueError:
                                    grid_id_info = properties.get(
                                        "Grid_ID", "N/A"
                                    )
                                    print(
                                        f"Warning: Could not convert {key_for_density_calculation} '{current_value_str}' to float in '{file_path}' for feature GID '{grid_id_info}'. Skipping this value for normalization."
                                    )

                        min_val = 0.0
                        max_val = 0.0
                        if values_for_normalization:
                            min_val = min(values_for_normalization)
                            max_val = max(values_for_normalization)
                        # If values_for_normalization is empty (e.g., all chosen key values were None or non-numeric)
                        # min_val and max_val will remain 0.0.
                        elif (
                            features_list
                        ):  # This means features exist, but no valid numeric data found for the chosen key
                            print(
                                f"Warning: No valid numeric values found for '{key_for_density_calculation}' in '{file_path}'. All 'density' values will be 0.0."
                            )

                        # Calculate and add normalized "density" property to each feature
                        for feature in features_list:
                            properties = feature.get("properties", {})
                            current_value_str = properties.get(
                                key_for_density_calculation
                            )
                            normalized_density_value = (
                                0.0  # Default for "density"
                            )

                            if (
                                current_value_str is not None
                                and values_for_normalization
                            ):  # Check if there are values to normalize against
                                try:
                                    current_value_float = float(
                                        current_value_str
                                    )
                                    if max_val == min_val:
                                        # If all valid numbers are the same, or only one number, resulting in min_val == max_val.
                                        # Normalized to 0.0 to represent no variation relative to the range.
                                        normalized_density_value = 0.0
                                    else:
                                        normalized_density_value = (
                                            (current_value_float - min_val)
                                            / (max_val - min_val)
                                        ) * 100
                                    properties["density"] = round(
                                        normalized_density_value, 4
                                    )
                                except ValueError:
                                    # Value for this specific feature was not numeric, already warned. Set density to 0.
                                    properties["density"] = 0.0
                            else:
                                # current_value_str is None, or no valid values for normalization were found in the entire file (values_for_normalization is empty).
                                properties["density"] = 0.0

                            feature["properties"] = properties

                        final_processing_message = f"Processed: {file_path}. Keys updated. Density calculated from '{source_key_name_for_print}'."

                    else:  # No features in features_list
                        print(
                            f"Info: No features found in {file_path}. Only top-level keys (if any) updated via mapping."
                        )
                        final_processing_message = f"Processed: {file_path}. Keys updated (no features for density calculation)."

                    # Write back to the SAME file
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(updated_data, f, ensure_ascii=False, indent=2)

                    print(final_processing_message)

                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    # import traceback # Uncomment for detailed debugging
                    # traceback.print_exc()


if __name__ == "__main__":
    json_folder = os.path.join(
        os.path.dirname(__file__), "population_json_files"
    )
    process_json_files(json_folder)
