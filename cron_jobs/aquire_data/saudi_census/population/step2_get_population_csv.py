import json
import csv
import os

def convert_population_json_to_csv(json_file_path, output_csv_path):
    """
    Convert a JSON file with population data to CSV format with specific field mapping.
    
    Args:
        json_file_path (str): Path to the input JSON file
        output_csv_path (str): Path to the output CSV file
    """
    # Check if input file exists
    if not os.path.exists(json_file_path):
        print(f"Error: Input file '{json_file_path}' not found")
        return False
    
    # Define CSV field names with proper mapping
    field_names = [
        'Level', 'Main_ID', 'Grid_ID', 'Population_Count', 'Male_Population',
        'Female_Population', 'Population_Density_KM2', 'Median_Age_Total',
        'Median_Age_Male', 'Median_Age_Female', 'Latitude', 'Longitude'
    ]
    
    # Map JSON keys to CSV headers
    field_mapping = {
        'level': 'Level',
        'main_id': 'Main_ID',
        'gid': 'Grid_ID',
        'pcnt': 'Population_Count',
        'pm_cnt': 'Male_Population',
        'pf_cnt': 'Female_Population',
        'pden_km2': 'Population_Density_KM2',
        'ymed_age': 'Median_Age_Total',
        'ymed_age_m': 'Median_Age_Male',
        'ymed_age_fm': 'Median_Age_Female',
        'centroid_lat': 'Latitude',
        'centroid_lon': 'Longitude'
    }
    
    try:
        # Open the JSON file and CSV file
        with open(json_file_path, 'r') as json_file, open(output_csv_path, 'w', newline='') as csv_file:
            # Create CSV writer
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            
            # Load and parse the JSON file
            print(f"Loading JSON file: {json_file_path}")
            data = json.load(json_file)
            
            # Process each record
            print(f"Processing {len(data)} records...")
            count = 0
            for row in data:
                # Create a new row with mapped field names
                mapped_row = {}
                for json_key, csv_key in field_mapping.items():
                    if json_key in row:
                        mapped_row[csv_key] = row[json_key]
                
                writer.writerow(mapped_row)
                
                # Display progress
                count += 1
                if count % 10000 == 0:
                    print(f"Processed {count} records")
        
        print(f"Successfully converted JSON to CSV: {output_csv_path}")
        print(f"Total records processed: {count}")
        return True
    
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return False
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

if __name__ == "__main__":
    # Input and output file paths
    input_file = "all_features.json"  # Update this to your actual input filename
    output_file = "population.csv"
    
    # Convert JSON to CSV
    convert_population_json_to_csv(input_file, output_file)