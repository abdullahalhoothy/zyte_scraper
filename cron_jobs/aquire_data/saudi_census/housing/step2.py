import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..",".."))
sys.path.append(grandparent_dir)

from cron_jobs.aquire_data.saudi_census.common_step2 import process_json_files

# Housing/housing column mapping
housing_COLUMN_MAPPING = {
    "GLEVEL": "Level",
    "MAIN_ID": "Main_ID",
    "GID": "Grid_ID",
    "H_DWLG_CNT": "Total_housings",
    "H_DWLG_T_RID": "Residential_housings",
    "H_DWLG_T_COM": "Non_Residential_housings",
    "H_OWNED_RID_H_CNT": "Owned_housings",
    "H_RENTED_RID_H_CNT": "Rented_housings",
    "H_PROV_RID_H_CNT": "Provided_housings",
    "H_OTH_RID_H_CNT": "Other_Residential_housings",
    "H_DWLG_T_COM_PUB": "Public_Housing",
    "H_DWLG_T_COM_WRK": "Work_Camps",
    "H_DWLG_T_COM_COMM": "Commercial_housings",
    "H_DWLG_OTH": "Other_housings",
    "CENTROID_LAT": "Latitude",
    "CENTROID_LON": "Longitude",
}

def process_housing_data(folder_path=None):
    """Process housing JSON files."""
    if folder_path is None:
        folder_path = os.path.join(os.path.dirname(__file__), "housing_json_files")
    
    process_json_files(
        folder_path=folder_path,
        column_mapping=housing_COLUMN_MAPPING,
        primary_density_key="Total_housings",
        fallback_density_key="Residential_housings"
    )

if __name__ == "__main__":
    process_housing_data()