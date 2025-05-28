import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..",".."))
sys.path.append(grandparent_dir)

from cron_jobs.aquire_data.saudi_census.common_step2 import process_json_files

# Household column mapping
HOUSEHOLD_COLUMN_MAPPING = {
    "GLEVEL": "Level",
    "MAIN_ID": "Main_ID",
    "GID": "Grid_ID",
    "HHAVG": "Household_Average_Size",
    "HHMED": "Household_Median_Size",
    "CENTROID_LAT": "Latitude",
    "CENTROID_LON": "Longitude",
}

def process_household_data(folder_path=None):
    """Process household JSON files."""
    if folder_path is None:
        folder_path = os.path.join(os.path.dirname(__file__), "household_json_files")
    
    process_json_files(
        folder_path=folder_path,
        column_mapping=HOUSEHOLD_COLUMN_MAPPING,
        primary_density_key="Household_Average_Size",
        fallback_density_key="Household_Median_Size"
    )

if __name__ == "__main__":
    process_household_data()