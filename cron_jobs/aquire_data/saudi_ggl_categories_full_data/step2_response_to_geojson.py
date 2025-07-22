import json
import os
import csv
from pathlib import Path

def convert_geojson_to_csv(geojson, output_csv_path):
    """
    Converts a GeoJSON object to CSV format and saves it.
    
    Args:
        geojson (dict): The GeoJSON object to convert
        output_csv_path (str or Path): The path to save the CSV file
        
    Returns:
        str: Path to the output CSV file
    """
    features = geojson["features"]
    
    # Determine all possible property keys across all features
    all_keys = set()
    for feature in features:
        if "properties" in feature:
            all_keys.update(feature["properties"].keys())
    
    # Add geometry and id fields
    csv_fields = ["id", "geometry_type", "longitude", "latitude"]
    csv_fields.extend(sorted(all_keys))
    
    # Convert to Path object if needed
    if not isinstance(output_csv_path, Path):
        output_csv_path = Path(output_csv_path)
    
    # Write to CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
        writer.writeheader()
        
        for feature in features:
            row = {}
            
            # Handle ID
            if "id" in feature:
                row["id"] = feature["id"]
            
            # Handle geometry
            if "geometry" in feature and feature["geometry"] is not None:
                geometry = feature["geometry"]
                row["geometry_type"] = geometry.get("type", "")
                
                # Extract coordinates - assuming Point geometry, adjust as needed
                if geometry.get("type") == "Point" and "coordinates" in geometry:
                    coordinates = geometry["coordinates"]
                    if len(coordinates) >= 2:
                        row["longitude"] = coordinates[0]
                        row["latitude"] = coordinates[1]
            
            # Handle properties
            if "properties" in feature and feature["properties"] is not None:
                for key, value in feature["properties"].items():
                    # Convert complex objects to string representation
                    if isinstance(value, (dict, list)):
                        row[key] = json.dumps(value)
                    else:
                        row[key] = value
            
            writer.writerow(row)
            
    return str(output_csv_path)

def to_geojson_save_csv(input_file_path, data=None):
    """
    Converts API response JSON to GeoJSON format and CSV.
   
    This function:
    1. Loads a JSON file containing API responses
    2. Extracts all GeoJSON features
    3. Creates a proper GeoJSON FeatureCollection
    4. Removes duplicate features based on their "id" property
    5. Saves it with "geojson_" prefix and .geojson extension
    6. Converts the GeoJSON to CSV and saves with "csv_" prefix
   
    Args:
        input_file_path (str): Path to the input JSON file
       
    Returns:
        tuple: Paths to the output GeoJSON and CSV files
    """
    # Get the directory, filename, and extension
    input_path = Path(input_file_path)
   
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file_path}")
   
    directory = input_path.parent
    filename = input_path.stem
   
    # Create the output filenames
    geojson_filename = f"geojson_{filename}.geojson"
    csv_filename = f"csv_{filename}.csv"
    geojson_path = directory / geojson_filename
    csv_path = directory / csv_filename
   
    # Load the input JSON file
    if not data:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
   
    # Combine features from all responses
    all_features = []
   
    # Handle different possible JSON structures
    if isinstance(data, list):
        # Multiple responses in a list
        for response in data:
            if isinstance(response, dict) and "data" in response and "features" in response["data"]:
                all_features.extend(response["data"]["features"])
    elif isinstance(data, dict) and "data" in data and "features" in data["data"]:
        # Single response
        all_features.extend(data["data"]["features"])
   
    if not all_features:
        raise KeyError("No GeoJSON features found in the input file")
 
    # Create a proper GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": all_features
    }
        
    # Drop duplicate features based on "id" in properties (keeping the first occurrence)
    unique_features = {}
    for feature in geojson["features"]:
        if "properties" in feature and "id" in feature["properties"]:
            feature_id = feature["properties"]["id"]
            # Only add if we haven't seen this ID before
            if feature_id not in unique_features:
                unique_features[feature_id] = feature
        else:
            # If feature doesn't have properties or id, keep it
            # We use a generated key to ensure it's kept
            unique_features[f"no_id_{id(feature)}"] = feature
    
    # Replace features with deduplicated list
    geojson["features"] = list(unique_features.values())
    # Save the GeoJSON file
    with open(geojson_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
    
    # Convert GeoJSON to CSV by calling the separate function
    csv_output_path = convert_geojson_to_csv(geojson, csv_path)
   
    return str(geojson_path), csv_output_path

if __name__ == "__main__":
    geojson_path, csv_path = to_geojson_save_csv(r"cron_jobs\aquire_data\saudi_ggl_categories_full_data\saudi_plumber_20250514_231515.json")
    print(f"Converted GeoJSON file saved to: {geojson_path}")
    print(f"Converted CSV file saved to: {csv_path}")

