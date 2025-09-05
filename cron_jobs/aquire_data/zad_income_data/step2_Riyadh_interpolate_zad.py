import sys
import os
import logging
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up to the grandparent directory (cron_jobs)
grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
# Add the grandparent directory to the system path
sys.path.append(grandparent_dir)

import numpy as np
import pandas as pd
import geopandas as gpd
from glob import glob
from cron_jobs.aquire_data.predict_saudi_income.pipeline import idw_interpolation
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
    handlers=[
        logging.FileHandler('income_interpolation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def interpolate_income(population_dir_path, zad_income_file_path, output_dir_path):
    logger.info(f"Starting income interpolation process")
    logger.info(f"Population directory: {population_dir_path}")
    logger.info(f"Income data file: {zad_income_file_path}")
    logger.info(f"Output directory: {output_dir_path}")
    
    # Load income data FIRST to get the bounds
    logger.info(f"Loading income data from {zad_income_file_path}")
    income_data = gpd.GeoDataFrame.from_features(
        pd.read_json(zad_income_file_path).features
    )
    logger.info(f"Loaded {len(income_data)} income records")
    
    # Get income bounds early for filtering
    income_bounds = income_data.union_all().convex_hull
    logger.info(f"Income data bounds calculated")
    
    # Convert income geometries to centroids for interpolation
    logger.info("Converting income geometries to centroids")
    income_centroids = income_data.geometry.centroid
    income_data = income_data.assign(geometry=income_centroids)
    
    # Only look for all_features.geojson files in each version directory
    population_data_files = glob(os.path.join(population_dir_path, "*", "all_features.geojson"))
    logger.info(f"Found {len(population_data_files)} population data files")
    
    for population_file_path in population_data_files:
        logger.info(f"Processing population file: {population_file_path}")
        
        input_path_parts = population_file_path.split(os.path.sep)
        output_file_path = Path(output_dir_path) / input_path_parts[-2] / input_path_parts[-1]
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove existing file if it exists
        if output_file_path.exists():
            logger.info(f"Removing existing output file: {output_file_path}")
            output_file_path.unlink()
        
        # skip v8
        if "v8" in population_file_path:
            logger.info("Skipping v8 file because it's too big")
            continue

        logger.info(f"Loading population data from {population_file_path}")
        population_data = gpd.GeoDataFrame.from_features(
            pd.read_json(population_file_path).features
        )
        logger.info(f"Loaded {len(population_data)} population records")

        # Rename columns if needed
        if "PCNT" in population_data.columns:
            logger.info("Renaming columns to standardized format")
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
        logger.info("Filtering population data by income bounds")
        pop_within_income_bounds = population_data[population_data.geometry.intersects(income_bounds)]
        logger.info(f"Filtered to {len(pop_within_income_bounds)} population records within income bounds")
        
        # If no population data overlaps with income data, skip this file
        if len(pop_within_income_bounds) == 0:
            logger.info("No population data within income bounds, skipping this file")
            continue
        
        # Filter out population polygons with missing population count
        mask = ~pop_within_income_bounds["Population_Count"].isna()
        pop_within_income_bounds = pop_within_income_bounds.loc[mask]
        logger.info(f"Final population data contains {len(pop_within_income_bounds)} records after filtering missing data")

        # Prepare data for interpolation - use population polygon centroids as targets
        logger.info("Preparing data for IDW interpolation")
        xy_points = np.array([(point.x, point.y) for point in income_data.geometry])
        values = income_data["Average Male Income"].values
        xy_targets = np.array(
            [(poly.centroid.x, poly.centroid.y) for poly in pop_within_income_bounds.geometry]
        )
        logger.info(f"Interpolating from {len(xy_points)} income points to {len(xy_targets)} population polygon centroids")
        
        # Perform interpolation
        interpolated_values = idw_interpolation(xy_points, values, xy_targets, k=6, power=2)
        pop_within_income_bounds = pop_within_income_bounds.copy()  # Avoid SettingWithCopyWarning
        pop_within_income_bounds["income"] = interpolated_values
        logger.info(f"Interpolation completed. Income range: {interpolated_values.min():.2f} - {interpolated_values.max():.2f}")

        # Set CRS and save - keeping original population polygons with added income values
        pop_within_income_bounds = pop_within_income_bounds.set_crs(epsg=4326).to_crs(epsg=4326)
        logger.info(f"Saving interpolated data to {output_file_path}")
        pop_within_income_bounds.to_file(output_file_path, driver="GeoJSON")
        logger.info(f"Successfully saved {len(pop_within_income_bounds)} records to {output_file_path}")

    logger.info("Income interpolation process completed")



interpolate_income(r"F:\git\zyte_scraper\cron_jobs\aquire_data\saudi_census\population\population_json_files",
                   r"F:\git\zyte_scraper\cron_jobs\aquire_data\zad_income_data\zad_output_geo_json_files\Output_data_20250520_201024.geojson",
                   r"F:\git\zyte_scraper\cron_jobs\aquire_data\zad_income_data\area_income_geojson")