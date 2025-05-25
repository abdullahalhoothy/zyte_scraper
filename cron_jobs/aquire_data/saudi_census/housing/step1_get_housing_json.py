import json
import os
import sys

# Add parent directory (saudi_census) to path to import saudi_census_common
current_script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_script_dir, ".."))
sys.path.append(parent_dir)
import saudi_census_common as common

# Entity-Specific Configuration
COLUMN_MAPPING = {
    'level': 'Level',
    'main_id': 'Main_ID',
    'gid': 'Grid_ID',
    "H_DWLG_CNT": "Total_Dwelling", 
    "H_DWLG_T_RID": "Residential_Dwelling",
    "H_DWLG_T_COM": "Other_Residential_Dwelling", # This was "Commercial_Dwelling" in file, "Other_Residential_Dwelling" in instructions. Sticking to instruction.
    "H_OWNED_RID_H_CNT": "Owned_Residential_Dwelling",
    "H_RENTED_RID_H_CNT": "Rented_Residential_Dwelling",
    "H_PROV_RID_H_CNT": "Provided_Residential_Dwelling",
    "H_OTH_RID_H_CNT": "Non_Residential_Dwelling", # This was "Other_Residential_Dwelling" in file, "Non_Residential_Dwelling" in instructions. Sticking to instruction.
    "H_DWLG_T_COM_PUB": "Public_Housing",
    "H_DWLG_T_COM_WRK": "Work_Camps",
    "H_DWLG_T_COM_COMM": "Commercial_Dwelling", # This was "Collective_Dwelling" in file, "Commercial_Dwelling" in instructions. Sticking to instruction.
    "H_DWLG_OTH": "Other_Dwelling",
    'centroid_lat': 'Latitude',
    'centroid_lon': 'Longitude'
}

ENTITY_TYPE = "housing"
BASE_URL_TEMPLATE_PART = "hous" # As per results_grid_hous_v{level}

def specific_fields_extractor_housing(properties):
    """
    Extracts housing-specific fields from the properties dictionary of a feature.
    Uses the global COLUMN_MAPPING for housing.
    """
    return {
        "H_DWLG_CNT": properties.get('H_DWLG_CNT'),
        "H_DWLG_T_RID": properties.get('H_DWLG_T_RID'),
        "H_DWLG_T_COM": properties.get('H_DWLG_T_COM'),
        "H_OWNED_RID_H_CNT": properties.get('H_OWNED_RID_H_CNT'),
        "H_RENTED_RID_H_CNT": properties.get('H_RENTED_RID_H_CNT'),
        "H_PROV_RID_H_CNT": properties.get('H_PROV_RID_H_CNT'),
        "H_OTH_RID_H_CNT": properties.get('H_OTH_RID_H_CNT'),
        "H_DWLG_T_COM_PUB": properties.get('H_DWLG_T_COM_PUB'),
        "H_DWLG_T_COM_WRK": properties.get('H_DWLG_T_COM_WRK'),
        "H_DWLG_T_COM_COMM": properties.get('H_DWLG_T_COM_COMM'),
        "H_DWLG_OTH": properties.get('H_DWLG_OTH'),
    }

if __name__ == "__main__":
    print(f"Script Starting for {ENTITY_TYPE}...")
    
    module_dir = os.path.dirname(os.path.abspath(__file__))

    common.setup_logging(module_dir, ENTITY_TYPE)
    
    common.main_step1_runner(
        module_dir=module_dir,
        entity_type=ENTITY_TYPE,
        base_url_template_part=BASE_URL_TEMPLATE_PART,
        column_mapping=COLUMN_MAPPING,
        specific_fields_extractor=specific_fields_extractor_housing
    )
    print(f"Script finished for {ENTITY_TYPE}.")
