import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..",".."))
sys.path.append(grandparent_dir)

from cron_jobs.aquire_data.saudi_census.common_step2 import process_json_files, create_population_centers_geojson_urban

# Population column mapping
POPULATION_COLUMN_MAPPING = {
    "GLEVEL": "Level",
    "MAIN_ID": "Main_ID",
    "GID": "Grid_ID",
    "PCNT": "Population_Count",
    "PM_CNT": "Male_Population",
    "PF_CNT": "Female_Population",
    "PDEN_KM2": "Population_Density_KM2",
    "YMED_AGE": "Median_Age_Total",
    "YMED_AGE_M": "Median_Age_Male",
    "YMED_AGE_FM": "Median_Age_Female",
    "CENTROID_LAT": "Latitude",
    "CENTROID_LON": "Longitude",
}

def process_population_data(folder_path=None):
    """Process population JSON files."""
    if folder_path is None:
        folder_path = os.path.join(os.path.dirname(__file__), "population_json_files")

    # process_json_files(
    #     folder_path=folder_path,
    #     column_mapping=POPULATION_COLUMN_MAPPING,
    #     primary_density_key="Population_Density_KM2",
    #     fallback_density_key="Population_Count"
    # )
    print("\nStep 2: Creating population centers...")
    create_population_centers_geojson_urban(folder_path)
if __name__ == "__main__":
    process_population_data()