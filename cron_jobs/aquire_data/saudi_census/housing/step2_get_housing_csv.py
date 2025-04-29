import json
import csv
import os

def convert_housing_json_to_csv(json_file_path, output_csv_path):
    """
    Convert a large housing JSON file to CSV format with specific field mapping.
    
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
        'Level', 'Main_ID', 'Grid_ID', 'Total_Dwelling', 'Residential_Dwelling',
        'Commercial_Dwelling', 'Owned_Residential_Dwelling', 'Rented_Residential_Dwelling',
        'Provided_Residential_Dwelling', 'Non_Residential_Dwelling', 'Public_Housing',
        'Work_Camps', 'Commercial_Dwelling_Units', 'Other_Dwelling', 'Latitude', 'Longitude'
    ]
    
    # Map JSON keys to CSV headers
    field_mapping = {
        'level': 'Level',
        'main_id': 'Main_ID',
        'gid': 'Grid_ID',
        'H_DWLG_CNT': 'Total_Dwelling',
        'H_DWLG_T_RID': 'Residential_Dwelling',
        'H_DWLG_T_COM': 'Commercial_Dwelling',
        'H_OWNED_RID_H_CNT': 'Owned_Residential_Dwelling',
        'H_RENTED_RID_H_CNT': 'Rented_Residential_Dwelling',
        'H_PROV_RID_H_CNT': 'Provided_Residential_Dwelling',
        'H_OTH_RID_H_CNT': 'Non_Residential_Dwelling',
        'H_DWLG_T_COM_PUB': 'Public_Housing',
        'H_DWLG_T_COM_WRK': 'Work_Camps',
        'H_DWLG_T_COM_COMM': 'Commercial_Dwelling_Units',
        'H_DWLG_OTH': 'Other_Dwelling',
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
    input_file = "all_features.json" # Update this to your actual input filename
    output_file = "housing.csv"
    
    # Convert JSON to CSV
    convert_housing_json_to_csv(input_file, output_file)