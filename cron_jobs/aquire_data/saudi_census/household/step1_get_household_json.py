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
    "HHAVG": "Household_Average",
    "HHMED": "Household_Median",
    'centroid_lat': 'Latitude',
    'centroid_lon': 'Longitude'
}

ENTITY_TYPE = "household"
BASE_URL_TEMPLATE_PART = "hh" # As per results_grid_hh_v{level}

def specific_fields_extractor_household(properties):
    """
    Extracts household-specific fields from the properties dictionary of a feature.
    """
    return {
        'HHAVG': properties.get('HHAVG'),
        'HHMED': properties.get('HHMED'),
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
        specific_fields_extractor=specific_fields_extractor_household
    )
    print(f"Script finished for {ENTITY_TYPE}.")
