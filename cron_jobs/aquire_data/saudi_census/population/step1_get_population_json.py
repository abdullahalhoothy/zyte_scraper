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
    'pcnt': 'Population_Count',
    'pm_cnt': 'Male_Population',
    'pf_cnt': 'Female_Population',
    'pden_km2': 'Population_Density_KM2',
    'ymed_age': 'Median_Age_Total',
    'ymed_age_m': 'Median_Age_Male',
    'ymed_age_fm': 'Median_Age_Female',
    'centroid_lat': 'Latitude',
    'centroid_lon': 'Longitude'
}

ENTITY_TYPE = "population"
BASE_URL_TEMPLATE_PART = "pop" # Used to construct the API URL, e.g. "pop" for population, "hh" for household

def specific_fields_extractor_population(properties):
    """
    Extracts population-specific fields from the properties dictionary of a feature.
    Uses the global COLUMN_MAPPING for population.
    """
    return {
        'pcnt': properties.get('PCNT'),
        'pm_cnt': properties.get('PM_CNT'),
        'pf_cnt': properties.get('PF_CNT'),
        'pden_km2': properties.get('PDEN_KM2'),
        'ymed_age': properties.get('YMED_AGE'),
        'ymed_age_m': properties.get('YMED_AGE_M'),
        'ymed_age_fm': properties.get('YMED_AGE_FM'),
    }

if __name__ == "__main__":
    print(f"Script Starting for {ENTITY_TYPE}...")
    
    # MODULE_DIR is used by common.setup_logging and common.main_step1_runner
    # It refers to the directory of the current script (step1_get_population_json.py)
    module_dir = os.path.dirname(os.path.abspath(__file__)) 

    # Setup logging for this specific script run
    # common.setup_logging(module_dir, ENTITY_TYPE) # This will create e.g. population.log
    # Logging for step1 is now done within main_step1_runner
    
    # The column_mapping is passed here as it's used by the specific_fields_extractor,
    # which in turn is used by the common.process_census_data_generic function.
    # The keys in specific_fields_extractor_population are already the desired keys for the final JSON.
    # COLUMN_MAPPING itself is more for renaming headers if saving to CSV or for mapping raw API responses.
    # The common.process_census_data_generic will handle the 'MAIN_ID', 'GID', 'level', 'centroid_lat', 'centroid_lon'.
    # The specific_fields_extractor only needs to provide the entity-specific data.
    common.main_step1_runner(
        module_dir=module_dir,
        entity_type=ENTITY_TYPE,
        base_url_template_part=BASE_URL_TEMPLATE_PART,
        column_mapping=COLUMN_MAPPING, 
        specific_fields_extractor=specific_fields_extractor_population
    )
    print(f"Script finished for {ENTITY_TYPE}.")
