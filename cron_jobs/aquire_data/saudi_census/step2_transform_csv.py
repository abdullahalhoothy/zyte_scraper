import pandas as pd
import numpy as np
import os
import logging


def split_degree(degree_str):
    """Split degree string into longitude and latitude."""
    logging.info("Splitting Degree column for %s", degree_str)
    if pd.isna(degree_str) or 'Degrees' not in str(degree_str):
        return pd.Series({'longitude': np.nan, 'latitude': np.nan})
    
    # Remove 'Degrees' and split
    coords = degree_str.replace(' Degrees', '').strip().split()
    return pd.Series({'longitude': float(coords[0]), 'latitude': float(coords[1])})

def process_csv_files(housing_path, household_path, population_path):
    """Process and merge CSV files."""
    logging.info("Reading CSV files")
    housing_df = pd.read_csv(housing_path)
    household_df = pd.read_csv(household_path)
    population_df = pd.read_csv(population_path)
    
    logging.info("Splitting Degree column")
    # Process each dataframe to split Degree column
    for df in [housing_df, household_df, population_df]:
        # Split Degree column into longitude and latitude
        degree_split = df['Degree'].apply(split_degree)
        df['longitude'] = degree_split['longitude']
        df['latitude'] = degree_split['latitude']
        logging.info(f"longitude: {df['longitude']} , latitude: {df['latitude']}")
    
    # Merge dataframes based on Degree and ZoomLevel
    # First merge housing and household
    logging.info("Merging dataframes")
    merged_df = pd.merge(
        housing_df,
        household_df,
        on=['longitude', 'latitude', 'ZoomLevel'],
        how='outer',
        suffixes=('_housing', '_household')
    )
    
    # Then merge with population
    final_df = pd.merge(
        merged_df,
        population_df,
        on=['longitude', 'latitude', 'ZoomLevel'],
        how='outer',
        suffixes=('', '_population')
    )
    
    # Clean up duplicate columns
    # Get list of columns to keep (avoiding duplicates)
    columns_to_keep = []
    seen_base_columns = set()
    logging.info("Cleaning up duplicate columns")
    for col in final_df.columns:
        base_col = col.split('_')[0] if '_' in col else col
        if base_col not in seen_base_columns:
            columns_to_keep.append(col)
            seen_base_columns.add(base_col)
    
    final_df = final_df[columns_to_keep]
    
    return final_df

# Example usage
if __name__ == "__main__":
    MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
    housing = os.path.join(MODULE_DIR, "housing/housing.csv")
    household = os.path.join(MODULE_DIR, "household/household.csv")
    population = os.path.join(MODULE_DIR, "population/population.csv")
    log_file_path = os.path.join(MODULE_DIR, "step2_transform_csv.log")
    
    logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    encoding="utf-8",
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s")
    
    logging.info("Module directory: %s", MODULE_DIR)
    logging.info("Housing file: %s", housing)
    logging.info("Household file: %s", household)
    logging.info("Population file: %s", population)
    
    logging.info("Starting data processing")
    result_df = process_csv_files(housing, household, population)
    result_df.to_csv('merged_data.csv', index=False)
    logging.info("Data processing complete")