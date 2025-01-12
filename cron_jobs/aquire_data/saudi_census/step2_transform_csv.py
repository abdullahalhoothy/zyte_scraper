import pandas as pd
import numpy as np
import os
import logging


def clean_numeric_column(column):
    """Clean numeric column by removing quotes and commas."""
    return pd.to_numeric(column.str.replace(',', '').str.replace('"', ''), errors='coerce')

def process_numeric_columns(df):
    """Process all numeric columns in the dataframe."""
    numeric_columns = [
        'MalePopulation', 'FemalePopulation', 'MedianAgeMale', 'MedianAgeFemale',
        'TotalPopulation', 'PopulationDensity', 'ZoomLevel', 'TotalDwellings',
        'ResidentialDwellings', 'OwnedDwellings', 'RentedDwellings', 'ProvidedDwellings',
        'OtherResidentialDwellings', 'Non-ResidentialDwellings', 'PublicHousing',
        'WorkCamps', 'CommercialDwellings', 'OtherDwellings', 'HouseholdAverageSize',
        'HouseholdMedianSize'
    ]
    
    for column in numeric_columns:
        if column in df.columns:
            df[column] = clean_numeric_column(df[column].astype(str))
    
    return df

def split_degree(degree_str):
    """Split degree string into longitude and latitude."""
    logging.info("Splitting Degree column for %s", degree_str)
    if pd.isna(degree_str) or 'Degrees' not in str(degree_str):
        return pd.Series({'longitude': np.nan, 'latitude': np.nan})
    
    # Remove 'Degrees' and split
    coords = degree_str.replace(' Degrees', '').strip().split()
    return pd.Series({'longitude': float(coords[0]), 'latitude': float(coords[1])})

def combine_similar_coordinates(df, tolerance=0.003):
    """
    Combine records with similar coordinates by averaging their values.
    Takes into account ZoomLevel when grouping coordinates.
    """
    # Sort by ZoomLevel, latitude, and longitude
    df_sorted = df.sort_values(['ZoomLevel', 'latitude', 'longitude']).reset_index(drop=True)
    
    # Calculate differences between consecutive rows
    lat_diff = df_sorted['latitude'].diff()
    lon_diff = df_sorted['longitude'].diff()
    zoom_diff = df_sorted['ZoomLevel'].diff()
    
    # Create groups where coordinates are within tolerance and ZoomLevel is same
    current_group = 0
    groups = []
    
    for i in range(len(df_sorted)):
        if i == 0:
            groups.append(current_group)
            continue
            
        # If ZoomLevel changes, start new group
        if zoom_diff.iloc[i] != 0:
            current_group += 1
            groups.append(current_group)
            continue
            
        # Check if coordinates are within tolerance
        if abs(lat_diff.iloc[i]) <= tolerance and abs(lon_diff.iloc[i]) <= tolerance:
            groups.append(current_group)
        else:
            current_group += 1
            groups.append(current_group)
    
    # Add group column
    df_sorted['coord_group'] = groups
    
    # Create aggregation dictionary for all columns
    agg_dict = {}
    for column in df_sorted.columns:
        if pd.api.types.is_numeric_dtype(df_sorted[column]):
            agg_dict[column] = 'mean'
    
    # For each group, average all numeric values
    df_grouped = df_sorted.groupby('coord_group').agg(agg_dict)
    
    # Round all numeric columns to 3 decimal places
    numeric_cols = df_grouped.select_dtypes(include=['float64', 'int64']).columns
    df_grouped[numeric_cols] = df_grouped[numeric_cols].round(3)
    
    # Merge back to get averaged and rounded values
    df_result = df_sorted.merge(
        df_grouped,
        left_on='coord_group',
        right_index=True,
        suffixes=('_orig', '')
    )
    
    # Drop temporary columns
    cols_to_drop = ['coord_group'] + [col for col in df_result.columns if col.endswith('_orig')]
    df_result = df_result.drop(cols_to_drop, axis=1)
    
    return df_result


def process_csv_files(household_path, population_path):
    """Process and merge household and population CSV files."""
    logging.info("Reading CSV files")
    
    # Read CSVs and immediately drop unnecessary columns
    columns_to_drop = ['Location', 'Selector', 'TopLeftDegree', 
                      'BottomRightDegree', 'ID', 'Parent']
    
    household_df = pd.read_csv(household_path).drop(columns=columns_to_drop, errors='ignore')
    population_df = pd.read_csv(population_path).drop(columns=columns_to_drop, errors='ignore')
    
    # Clean numeric columns
    logging.info("Cleaning numeric columns")
    household_df = process_numeric_columns(household_df)
    population_df = process_numeric_columns(population_df)
    
    # Process degree columns
    logging.info("Processing coordinates")
    for df in [household_df, population_df]:
        degree_split = df['Degree'].apply(split_degree)
        df['longitude'] = degree_split['longitude']
        df['latitude'] = degree_split['latitude']
    
    # Merge dataframes
    logging.info("Merging dataframes")
    merged_df = pd.merge(
        household_df,
        population_df,
        on=['longitude', 'latitude', 'ZoomLevel'],
        how='outer'
    )
    
    # Now combine similar coordinates
    logging.info("Combining similar coordinates")
    final_df = combine_similar_coordinates(merged_df)
    
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
    result_df = process_csv_files(household, population)
    output_csv_path = os.path.join(MODULE_DIR, "merged_data.csv")
    df_sorted = result_df.sort_values(by=['longitude', 'latitude'])
    result_df.to_csv(output_csv_path, index=False)
    logging.info("Data processing complete")