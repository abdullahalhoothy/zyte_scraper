import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import os
import logging


def clean_numeric_column(column):
    """Clean numeric column by removing quotes and commas."""
    return pd.to_numeric(
        column.str.replace(",", "").str.replace('"', ""), errors="coerce"
    )


def process_numeric_columns(df):
    """Process all numeric columns in the dataframe."""
    numeric_columns = [
        "MalePopulation",
        "FemalePopulation",
        "MedianAgeMale",
        "MedianAgeFemale",
        "TotalPopulation",
        "PopulationDensity",
        "ZoomLevel",
        "TotalDwellings",
        "ResidentialDwellings",
        "OwnedDwellings",
        "RentedDwellings",
        "ProvidedDwellings",
        "OtherResidentialDwellings",
        "Non-ResidentialDwellings",
        "PublicHousing",
        "WorkCamps",
        "CommercialDwellings",
        "OtherDwellings",
        "HouseholdAverageSize",
        "HouseholdMedianSize",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = clean_numeric_column(df[column].astype(str))

    return df


def split_degree(degree_str):
    """Split degree string into longitude and latitude."""
    logging.info("Splitting Degree column for %s", degree_str)
    if pd.isna(degree_str) or "Degrees" not in str(degree_str):
        return pd.Series({"longitude": np.nan, "latitude": np.nan})

    # Remove 'Degrees' and split
    coords = degree_str.replace(" Degrees", "").strip().split()
    return pd.Series({"longitude": float(coords[0]), "latitude": float(coords[1])})


def merge_similar_coordinates(df, tolerance=0.003):
    """
    Combine records with similar coordinates by averaging their values.
    Takes into account ZoomLevel when grouping coordinates.
    """
    # Sort by ZoomLevel, latitude, and longitude
    df_sorted = df.sort_values(["ZoomLevel", "latitude", "longitude"]).reset_index(
        drop=True
    )

    # Calculate differences between consecutive rows
    lat_diff = df_sorted["latitude"].diff()
    lon_diff = df_sorted["longitude"].diff()
    zoom_diff = df_sorted["ZoomLevel"].diff()

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
    df_sorted["coord_group"] = groups

    # Create aggregation dictionary for all columns
    agg_dict = {}
    for column in df_sorted.columns:
        if pd.api.types.is_numeric_dtype(df_sorted[column]):
            agg_dict[column] = "mean"

    # For each group, average all numeric values
    df_grouped = df_sorted.groupby("coord_group").agg(agg_dict)

    # Round all numeric columns to 3 decimal places
    numeric_cols = df_grouped.select_dtypes(include=["float64", "int64"]).columns
    df_grouped[numeric_cols] = df_grouped[numeric_cols].round(3)

    # Merge back to get averaged and rounded values
    df_result = df_sorted.merge(
        df_grouped, left_on="coord_group", right_index=True, suffixes=("_orig", "")
    )

    # Drop temporary columns
    cols_to_drop = ["coord_group"] + [
        col for col in df_result.columns if col.endswith("_orig")
    ]
    df_result = df_result.drop(cols_to_drop, axis=1)

    return df_result


def avg_duplicate_coordinates(df):
    # Create separate dataframe for degrees and other columns (except lat/long)
    base_columns = [
        "Degree_x",
        "Degree_y",
        "HouseholdAverageSize",
        "HouseholdMedianSize",
        "ZoomLevel",
        "MalePopulation",
        "FemalePopulation",
        "MedianAgeMale",
        "MedianAgeFemale",
        "TotalPopulation",
        "PopulationDensity",
    ]
    df = df.fillna(-999)
    base_df = df[base_columns].copy()
    group_df = df.copy()

    group_columns = base_columns[2:]
    group_df = group_df.drop(columns=["Degree_x", "Degree_y"])

    # Calculate average coordinates
    coord_df = group_df.groupby(group_columns).mean()

    # Merge the averaged coordinates back with the original data
    final_result = base_df.merge(coord_df, on=group_columns, how="left")
    final_result = final_result.replace(-999, pd.NA)

    return final_result


def standardize_point_spacing(df):
    result_dfs = []
    tolerance = 0.01
    
    for zoom in range(4, 10):
        filtered_df = df[df['ZoomLevel'] == zoom].copy()
        if filtered_df.empty:
            continue
            
        # Use KMeans for initial city clustering
        coords = filtered_df[['latitude', 'longitude']].values
        clustering = KMeans(n_clusters=3, random_state=42).fit(coords)
        filtered_df['cluster'] = clustering.labels_
        
        # Process each city cluster
        for cluster_id in range(3):
            city_df = filtered_df[filtered_df['cluster'] == cluster_id].copy()
            
            # Reset index once at city_df level
            city_df = city_df.reset_index()

            # Identify columns (sort by longitude)
            lon_df = city_df.sort_values('longitude')
            lon_diff = lon_df['longitude'].diff()
            new_col = (abs(lon_diff) > tolerance) | lon_diff.isna()
            lon_df['col_id'] = new_col.cumsum()

            # Identify rows (sort by latitude)
            lat_df = city_df.sort_values('latitude')
            lat_diff = lat_df['latitude'].diff()
            new_row = (abs(lat_diff) > tolerance) | lat_diff.isna()
            lat_df['row_id'] = new_row.cumsum()

            # Merge back to city_df using the index
            city_df = city_df.merge(lon_df[['index', 'col_id']], on='index')
            city_df = city_df.merge(lat_df[['index', 'row_id']], on='index')
            
            city_df = city_df.drop(columns=['index'])
            # Calculate average column (longitude) separations
            col_groups = city_df.groupby('col_id')
            avg_lon_seps = []
            for _, col in col_groups:
                lon_diffs = np.diff(sorted(col['longitude'].unique()))
                if len(lon_diffs) > 0:
                    avg_lon_seps.extend([np.mean(lon_diffs)] * len(col))
                else:
                    avg_lon_seps.extend([0] * len(col))
            
            # Calculate average row (latitude) separations
            row_groups = city_df.groupby('row_id')
            avg_lat_seps = []
            for _, row in row_groups:
                lat_diffs = np.diff(sorted(row['latitude'].unique()))
                if len(lat_diffs) > 0:
                    avg_lat_seps.extend([np.mean(lat_diffs)] * len(row))
                else:
                    avg_lat_seps.extend([0] * len(row))
            
            city_df['avg_lon_sep'] = avg_lon_seps
            city_df['avg_lat_sep'] = avg_lat_seps
            
            # Adjust coordinates
            min_lat = city_df.groupby('row_id')['latitude'].transform('min')
            min_lon = city_df.groupby('col_id')['longitude'].transform('min')
            
            city_df['latitude'] = min_lat + (city_df['row_id'] * city_df['avg_lat_sep'])
            city_df['longitude'] = min_lon + (city_df['col_id'] * city_df['avg_lon_sep'])
            
            # Drop temporary columns
            city_df = city_df.drop(['row_id', 'col_id', 'cluster', 'avg_lon_sep', 'avg_lat_sep'], axis=1)
            result_dfs.append(city_df)
    
    # Combine all results
    if result_dfs:
        return pd.concat(result_dfs, ignore_index=True)
    return df

def process_csv_files(household_path, population_path):
    """Process and merge household and population CSV files."""
    logging.info("Reading CSV files")

    # Read CSVs and immediately drop unnecessary columns
    columns_to_drop = [
        "Location",
        "Selector",
        "TopLeftDegree",
        "BottomRightDegree",
        "ID",
        "Parent",
    ]

    household_df = pd.read_csv(household_path).drop(
        columns=columns_to_drop, errors="ignore"
    )
    population_df = pd.read_csv(population_path).drop(
        columns=columns_to_drop, errors="ignore"
    )

    # Clean numeric columns
    logging.info("Cleaning numeric columns")
    household_df = process_numeric_columns(household_df)
    population_df = process_numeric_columns(population_df)

    # Process degree columns
    logging.info("Processing coordinates")
    for df in [household_df, population_df]:
        degree_split = df["Degree"].apply(split_degree)
        df["longitude"] = degree_split["longitude"]
        df["latitude"] = degree_split["latitude"]

    # Merge dataframes
    logging.info("Merging dataframes")
    merged_df = pd.merge(
        household_df,
        population_df,
        on=["longitude", "latitude", "ZoomLevel"],
        how="outer",
    )

    # Now combine similar coordinates
    logging.info("Combining similar coordinates")
    final_df = merge_similar_coordinates(merged_df)
    # average lat and long for duplicate coordinates
    no_dup_df = avg_duplicate_coordinates(final_df)
    basecopy = no_dup_df[["Degree_x", "Degree_y", "longitude", "latitude"]].copy()
    no_dup_df = no_dup_df.drop(columns=["Degree_x", "Degree_y"]).drop_duplicates()
    # standardize spacing between points
    std_df = standardize_point_spacing(no_dup_df)

    return no_dup_df


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
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    logging.info("Module directory: %s", MODULE_DIR)
    logging.info("Housing file: %s", housing)
    logging.info("Household file: %s", household)
    logging.info("Population file: %s", population)

    logging.info("Starting data processing")
    result_df = process_csv_files(household, population)
    output_csv_path = os.path.join(MODULE_DIR, "merged_data.csv")
    df_sorted = result_df.sort_values(by=["longitude", "latitude"])
    result_df.to_csv(output_csv_path, index=False)
    logging.info("Data processing complete")
