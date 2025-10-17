import sys
import os
import logging
import argparse
import sys
parser = argparse.ArgumentParser()
parser.add_argument("--log-file", help="Path to shared log file", required=False)
args = parser.parse_args()

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to the grandparent directory (cron_jobs)
grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
# Add the grandparent directory to the system path
sys.path.append(grandparent_dir)

if(args.log_file):
    from logging_utils import setup_logging
    setup_logging(args.log_file)

import numpy as np
import pandas as pd
import geopandas as gpd
from glob import glob
from cron_jobs.aquire_data.predict_saudi_income.pipeline import idw_interpolation
from pathlib import Path

def interpolate_income(population_dir_path, zad_income_file_path, output_dir_path):
    logging.info(f"Starting income interpolation process")
    logging.info(f"Population directory: {population_dir_path}")
    logging.info(f"Income data file: {zad_income_file_path}")
    logging.info(f"Output directory: {output_dir_path}")
    
    # Load income data FIRST to get the bounds
    logging.info(f"Loading income data from {zad_income_file_path}")
    income_data = gpd.GeoDataFrame.from_features(
        pd.read_json(zad_income_file_path).features
    )
    logging.info(f"Loaded {len(income_data)} income records")
    
    # Get income bounds early for filtering
    income_bounds = income_data.union_all().convex_hull
    logging.info(f"Income data bounds calculated")
    
    # Convert income geometries to centroids for interpolation
    logging.info("Converting income geometries to centroids")
    income_centroids = income_data.geometry.centroid
    income_data = income_data.assign(geometry=income_centroids)
    
    # Only look for all_features.geojson files in each version directory
    population_data_files = glob(os.path.join(population_dir_path, "*", "all_features.geojson"))
    logging.info(f"Found {len(population_data_files)} population data files")
    
    for population_file_path in population_data_files:
        logging.info(f"Processing population file: {population_file_path}")
        
        input_path_parts = population_file_path.split(os.path.sep)
        output_file_path = Path(output_dir_path) / input_path_parts[-2] / input_path_parts[-1]
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove existing file if it exists
        if output_file_path.exists():
            logging.info(f"Removing existing output file: {output_file_path}")
            output_file_path.unlink()
        
        # skip v8
        if "v8" in population_file_path:
            logging.info("Skipping v8 file because it's too big")
            continue

        logging.info(f"Loading population data from {population_file_path}")
        population_data = gpd.GeoDataFrame.from_features(
            pd.read_json(population_file_path).features
        )
        logging.info(f"Loaded {len(population_data)} population records")

        # Rename columns if needed
        if "PCNT" in population_data.columns:
            logging.info("Renaming columns to standardized format")
            population_data = population_data.rename(
                columns={
                    "MAIN_ID": "Main_ID",
                    "GID": "Grid_ID",
                    "GLEVEL": "Level",
                    "PCNT": "Population_Count",
                    "PM_CNT": "Male_Population",
                    "PF_CNT": "Female_Population",
                    "PDEN_KM2": "Population_Density_KM2",
                    "YMED_AGE": "Median_Age_Total",
                    "YMED_AGE_M": "Median_Age_Male",
                    "YMED_AGE_FM": "Median_Age_Female",
                }
            )

        # Filter population data to only include polygons that intersect with income bounds
        logging.info("Filtering population data by income bounds")
        pop_within_income_bounds = population_data[population_data.geometry.intersects(income_bounds)]
        logging.info(f"Filtered to {len(pop_within_income_bounds)} population records within income bounds")
        
        # If no population data overlaps with income data, skip this file
        if len(pop_within_income_bounds) == 0:
            logging.info("No population data within income bounds, skipping this file")
            continue
        
        # Filter out population polygons with missing population count
        mask = ~pop_within_income_bounds["Population_Count"].isna()
        pop_within_income_bounds = pop_within_income_bounds.loc[mask]
        logging.info(f"Final population data contains {len(pop_within_income_bounds)} records after filtering missing data")

        # Prepare data for interpolation - use population polygon centroids as targets
        logging.info("Preparing data for IDW interpolation")
        xy_points = np.array([(point.x, point.y) for point in income_data.geometry])
        values = income_data["Average Male Income"].values
        xy_targets = np.array(
            [(poly.centroid.x, poly.centroid.y) for poly in pop_within_income_bounds.geometry]
        )
        logging.info(f"Interpolating from {len(xy_points)} income points to {len(xy_targets)} population polygon centroids")
        
        # Perform interpolation
        interpolated_values = idw_interpolation(xy_points, values, xy_targets, k=6, power=2)
        pop_within_income_bounds = pop_within_income_bounds.copy()  # Avoid SettingWithCopyWarning
        pop_within_income_bounds["income"] = interpolated_values
        logging.info(f"Interpolation completed. Income range: {interpolated_values.min():.2f} - {interpolated_values.max():.2f}")

        # Set CRS and save - keeping original population polygons with added income values
        pop_within_income_bounds = pop_within_income_bounds.set_crs(epsg=4326).to_crs(epsg=4326)
        logging.info(f"Saving interpolated data to {output_file_path}")
        pop_within_income_bounds.to_file(output_file_path, driver="GeoJSON")
        logging.info(f"Successfully saved {len(pop_within_income_bounds)} records to {output_file_path}")

    logging.info("Income interpolation process completed")



census_population_path=os.path.join(current_dir,"..","saudi_census","population','population_json_files")
zad_geojson_path=os.path.join(current_dir,"zad_output_geo_json_files","Output_data.geojson")
output_interpolated_income_path=os.path.join(current_dir,"interpolated_income","area_income_geojson")

interpolate_income(census_population_path,
                   zad_geojson_path,
                   output_interpolated_income_path)