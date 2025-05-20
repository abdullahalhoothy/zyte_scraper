import os
import numpy as np
import pandas as pd
import geopandas as gpd
from glob import glob
from shapely.geometry import box
from pipeline import idw_interpolation
from pathlib import Path

def interpolate_income(population_dir_path, zad_income_file_path, output_dir_path):
    population_data_files = glob(os.path.join(population_dir_path, "**", "*.json"), recursive=True)
    for population_data_file in population_data_files:
        print(f"starting {population_data_file} ...")
        population_data = gpd.GeoDataFrame.from_features(
            pd.read_json(population_data_file).features
        )

        if "PCNT" in population_data.columns:
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

        grid_size = np.round((population_data.geometry.area.max()) ** 0.5, 5) * 2.5

        minx, miny, maxx, maxy = population_data.total_bounds
        grid_cells = [
            box(x, y, x + grid_size, y + grid_size)
            for x in np.arange(minx, maxx, grid_size)
            for y in np.arange(miny, maxy, grid_size)
        ]

        grid = gpd.GeoDataFrame(geometry=grid_cells, crs=population_data.crs)

        joined_population = gpd.sjoin(
            population_data, grid, how="inner", predicate="within"
        )

        grid = pd.concat(
            [
                grid,
                joined_population.groupby("index_right")["Population_Count"].sum(),
                joined_population.groupby("index_right")["Male_Population"].sum(),
                joined_population.groupby("index_right")["Female_Population"].sum(),
                joined_population.groupby("index_right")["Population_Density_KM2"].mean(),
                joined_population.groupby("index_right")["Median_Age_Total"].mean(),
                joined_population.groupby("index_right")["Median_Age_Male"].mean(),
                joined_population.groupby("index_right")["Median_Age_Female"].mean(),
            ],
            axis=1
        )

        mask = ~grid["Population_Count"].isna()
        grid = grid.loc[mask]

        income_data = gpd.GeoDataFrame.from_features(
            pd.read_json(zad_income_file_path).features
        )

        bounds = grid[["geometry", "Population_Count"]].dropna().union_all().convex_hull
        mask = income_data[["geometry", "Average Male Income"]].within(bounds)
        income_data = income_data.loc[mask][["geometry", "Average Male Income"]]

        bounds = income_data.union_all().convex_hull
        mask = grid.within(bounds)
        grid = grid.loc[mask]

        income_data = income_data[["geometry", "Average Male Income"]].assign(
            geometry=lambda x: x.geometry.centroid
        )
        mask = ~grid[["geometry", "Population_Count"]].isna().any(axis=1)
        grid = grid.loc[mask]

        xy_points = np.array([(point.x, point.y) for point in income_data.geometry])
        values = income_data["Average Male Income"].values
        xy_targets = np.array(
            [(poly.centroid.x, poly.centroid.y) for poly in grid.geometry]
        )
        interpolated_values = idw_interpolation(xy_points, values, xy_targets, k=6, power=2) 
        grid["income"] = interpolated_values
        grid = grid.set_crs(epsg=4326).to_crs(epsg=4326)
        input_path_parts = population_data_file.split(os.path.sep)
        # Build the output path
        output_file_path = Path(output_dir_path) / input_path_parts[-2] / input_path_parts[-1]
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        grid.to_file(output_file_path, driver="geojson")


interpolate_income(r"F:\git\zyte_scraper\cron_jobs\aquire_data\saudi_census\population\population_json_files",
                   r"F:\git\zyte_scraper\cron_jobs\aquire_data\saudi_income_data\output_geo_json_files\ignore_Output_data_20250509_101734.json",
                   r"F:\git\zyte_scraper\cron_jobs\aquire_data\saudi_income_data\interpolated_zad")

