import pandas as pd
import os
from pathlib import Path

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
            
            # rename latitude/longitude columns
            column_mapping = {}
            for col in df.columns:
                if 'LAT' == col:
                    column_mapping[col] = 'latitude'
                elif 'LON' == col:
                    column_mapping[col] = 'longitude'
            
            df = df.rename(columns=column_mapping)
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
