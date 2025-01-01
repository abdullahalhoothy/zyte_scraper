import pandas as pd
import os
from pathlib import Path

column_name_mapping = {
    'LAT': 'latitude',
    'LON': 'longitude',
    '1-Population, 2021-Total Count': 'population_2021',
    '6-Population density per square kilometre-Total Count': 'population_density_per_sq_km',
    '39-Average age of the population-Total Count': 'average_age',
    '50-Total - Private households by household size - 100% data-Total Count': 'total_private_households_by_size',
    '318-  Median total income in 2020 ($)-Total Count': 'median_total_income_2020',
}

def process_csv_files():
    # Get the current directory where the script is located
    current_dir = Path(__file__).parent
    ignore_dir = current_dir / 'ignore'
    output_file = current_dir / 'canada_census.csv'

    # Get all CSV files from ignore directory
    csv_files = list(ignore_dir.glob('*.csv'))
    
    # List to store all dataframes
    all_dfs = []

    for csv_file in csv_files:
        print(f"Processing {csv_file.name}...")
        
        try:
            # Read CSV 
            df = pd.read_csv(csv_file, low_memory=False, encoding='latin-1')
            
            # First check if all required columns exist in the dataframe
            missing_columns = [col for col in column_name_mapping.keys() if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing columns: {missing_columns}")
            
            # rename columns and only keep the columns that are in the column_name_mapping
            df = df.rename(columns=column_name_mapping)
            df = df[column_name_mapping.values()]
            
            # Append the processed dataframe to all_dfs
            all_dfs.append(df)
            
            print(f"Successfully processed {csv_file.name}")
            
        except Exception as e:
            print(f"Error processing {csv_file.name}: {str(e)}")
    
    if all_dfs:
        # Combine all dataframes
        print("Combining all CSV files...")
        combined_df = pd.concat(all_dfs, ignore_index=True)
        
        # Write to single output file with UTF-8 encoding
        combined_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Successfully saved combined data to {output_file}")
    else:
        print("No CSV files were successfully processed")

if __name__ == "__main__":
    process_csv_files()
