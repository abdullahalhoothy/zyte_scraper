from datetime import datetime
import os
from time import sleep
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from step2_traffic_analysis import GoogleMapsTrafficAnalyzer, logger
from step2_scrapy_transform_to_csv import process_real_estate_data
from step2_add_demographics import fetch_demographics
from step2_add_demographics import login_and_get_user
from step2_add_demographics import fetch_household_from_db
from step2_extract_listing_id import add_listing_ids_to_csv

# --- Centralized column definitions ---
INPUT_COLUMNS = [
    "listing_id",
    "url",
    "latitude",
    "longitude",
    "city",
    "direction_id",
    "category",
]
TRAFFIC_COLUMNS = [
    "traffic_score",
    "traffic_storefront_score",
    "traffic_area_score",
    "traffic_screenshot_filename",
    "traffic_analysis_date",
]
DEMOGRAPHIC_COLUMNS = [
    "total_population",
    "avg_density",
    "avg_median_age",
    "avg_income",
    "percentage_age_above_20",
    "percentage_age_above_25",
    "percentage_age_above_30",
    "percentage_age_above_35",
    "percentage_age_above_40",
    "percentage_age_above_45",
    "percentage_age_above_50",
    "demographics_analysis_date",
]
HOUSEHOLD_COLUMNS = [
    "total_households",
    "avg_household_size",
    "median_household_size",
    "density_sum",
    "features_count",
    "household_analysis_date",
]
OBJECT_COLUMNS = [
    "demographics_analysis_date",
    "traffic_details",
    "traffic_analysis_date",
]
DATE_COLUMNS = ["demographics_analysis_date", "traffic_analysis_date"]
CITY_FILTER = "الرياض"
CATEGORY_FILTER = "shop_for_rent"
CHUNK_SIZE = 5000


def ensure_city_csv(
    csv_path,
    city=CITY_FILTER,
    category=CATEGORY_FILTER,
    columns=INPUT_COLUMNS,
    chunk_size=CHUNK_SIZE,
):
    """
    Ensure a city-specific CSV exists and is up-to-date (created if missing or older than 1 day).
    Filters records by city and saves to a new CSV file with selected columns if needed.
    Returns the path to the city CSV.
    """
    base_path = csv_path.rsplit(".csv", 1)[0]
    city_csv_path = f"{base_path}_{city}.csv"
    need_create = True
    if os.path.exists(city_csv_path):
        last_modified = datetime.fromtimestamp(os.path.getmtime(city_csv_path))
        now = datetime.now()
        if (now - last_modified).days < 1:
            need_create = False
    if need_create:
        print(f"Creating {city} CSV: {city_csv_path}")
        first_chunk = True
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            city_chunk = chunk[chunk["city"] == city].copy()
            # Filter for category
            city_chunk = city_chunk[city_chunk["category"] == category]
            city_chunk = city_chunk[columns]
            if first_chunk:
                city_chunk.to_csv(city_csv_path, index=False, mode="w")
                first_chunk = False
            else:
                city_chunk.to_csv(
                    city_csv_path, index=False, mode="a", header=False
                )
        logger.info(f"{city} records saved to: {city_csv_path}")
    else:
        print(f"{city} CSV is up-to-date: {city_csv_path}")
    return city_csv_path


def ensure_columns_in_csv(csv_path, columns, temp_path, chunk_size=CHUNK_SIZE):
    """
    Ensure columns exist in CSV and save to temp file.
    """
    all_columns = INPUT_COLUMNS + columns
    first_chunk = True
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        chunk = chunk[INPUT_COLUMNS]
        for col in columns:
            if col not in chunk.columns:
                chunk[col] = None
        chunk = chunk[all_columns]
        if first_chunk:
            chunk.to_csv(temp_path, index=False, mode="w")
            first_chunk = False
        else:
            chunk.to_csv(temp_path, index=False, mode="a", header=False)


def get_locations_needing_processing(
    temp_path, key_column, city=CITY_FILTER, chunk_size=CHUNK_SIZE
):
    """
    Get locations for a city where key_column is NaN.
    """
    locations = []
    for chunk in pd.read_csv(temp_path, chunksize=chunk_size):
        city_chunk = chunk[chunk["city"] == city].copy()
        if len(city_chunk) > 0:
            unprocessed = city_chunk[city_chunk[key_column].isna()]
            for _, row in unprocessed.iterrows():
                locations.append(
                    {
                        "lat": row["latitude"],
                        "lng": row["longitude"],
                        "index": row.name if hasattr(row, "name") else None,
                    }
                )
    return locations


def update_csv_with_results(
    temp_path,
    results,
    columns,
    object_columns=OBJECT_COLUMNS,
    date_columns=DATE_COLUMNS,
    city_filter=CITY_FILTER,
    chunk_size=CHUNK_SIZE,
):
    """
    Update temp CSV file with results for locations in a city.
    """
    temp_updated_path = f"{temp_path}_updating"
    first_chunk_update = True
    all_columns = INPUT_COLUMNS + columns
    for chunk in pd.read_csv(temp_path, chunksize=chunk_size):
        for col in object_columns:
            if col in chunk.columns:
                chunk[col] = chunk[col].astype("object")
        city_mask = chunk["city"] == city_filter
        for idx in chunk[city_mask].index:
            chunk_lat = chunk.loc[idx, "latitude"]
            chunk_lng = chunk.loc[idx, "longitude"]
            coord_key = f"{chunk_lat}_{chunk_lng}"
            if coord_key in results:
                for col in columns:
                    value = results[coord_key].get(col, None)
                    # Ensure only pure values are written, not dicts
                    if isinstance(value, dict):
                        # If the value is a dict, set to None (should not happen)
                        value = None
                    if col in date_columns and value is not None:
                        value = str(value)
                    chunk.loc[idx, col] = value
        chunk = chunk[all_columns]
        if first_chunk_update:
            chunk.to_csv(temp_updated_path, index=False, mode="w")
            first_chunk_update = False
        else:
            chunk.to_csv(temp_updated_path, index=False, mode="a", header=False)
    try:
        sleep(2)
        os.replace(temp_updated_path, temp_path)
    except Exception as e:
        # warning log
        logger.warning(
            f"Failed to replace {temp_path} with updated file {temp_updated_path}: {e}"
        )

def process_city_traffic(csv_path: str, batch_size: int, city=CITY_FILTER):
    """
    Process records for traffic analysis and save to a dedicated CSV for a city.
    """
    base_path = csv_path.rsplit(".csv", 1)[0]
    city_csv_path = f"{base_path}_{city}.csv"
    output_path = f"{base_path}_{city}_enriched_with_traffic.csv"
    temp_path = f"{base_path}_{city}_traffic_temp_processing.csv"

    logger.info(f"Starting traffic analysis for {city} locations")
    logger.info(f"Input CSV: {city_csv_path}")
    logger.info(f"Enriched Output CSV: {output_path}")

    ensure_columns_in_csv(city_csv_path, TRAFFIC_COLUMNS, temp_path)
    locations = get_locations_needing_processing(
        temp_path, "traffic_score", city
    )
    logger.info(
        f"Found {len(locations)} {city} locations needing traffic analysis"
    )
    if len(locations) == 0:
        logger.info(f"All {city} locations already have traffic data")
        os.rename(temp_path, output_path)
        logger.info(f"All data saved to: {output_path}")
        return output_path

    processed_count = 0
    traffic_results = {}
    total_locations = len(locations)

    for batch_start in range(0, total_locations, batch_size):
        batch = locations[batch_start : batch_start + batch_size]
        logger.info(
            f"Processing traffic for batch {batch_start+1}-{min(batch_start+batch_size, total_locations)} of {total_locations}"
        )
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_loc = {
                executor.submit(
                    lambda loc: GoogleMapsTrafficAnalyzer(
                        cleanup_driver=True
                    ).analyze_location_traffic(
                        lat=loc["lat"],
                        lng=loc["lng"],
                        day_of_week="Monday",
                        target_time="6:00PM",
                    ),
                    loc,
                ): loc
                for loc in batch
            }
            for future in as_completed(future_to_loc):
                loc = future_to_loc[future]
                lat, lng = loc["lat"], loc["lng"]
                try:
                    traffic_result = future.result()
                except Exception as e:
                    logger.error(
                        f"Traffic analysis failed for {lat}, {lng}: {e}"
                    )
                    traffic_result = {"score": 0, "error": str(e)}
                
                traffic_score = traffic_result.get("score", 0)
                traffic_storefront_score = traffic_result.get("storefront_score", 0)
                traffic_area_score = traffic_result.get("area_score", 0)
                traffic_screenshot_path = traffic_result.get("screenshot_path", "")
                # f:\git\zyte_scraper\cron_jobs\aquire_data\saudi_real_estate\step2\traffic_screenshots\traffic_24.677122_46.693966_Monday_6-00PM_pinned_frontscore=0_areascore=51.png
                # i don't need the entire path just the file name
                traffic_screenshot_filename = os.path.basename(traffic_screenshot_path)
                coord_key = f"{lat}_{lng}"
                traffic_results[coord_key] = {
                    "traffic_score": traffic_score,
                    "traffic_storefront_score": traffic_storefront_score,
                    "traffic_area_score": traffic_area_score,
                    "traffic_screenshot_filename": traffic_screenshot_filename,
                    "traffic_analysis_date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                processed_count += 1
        logger.info(
            f"Progress checkpoint: {processed_count}/{total_locations} locations processed"
        )
        update_csv_with_results(temp_path, traffic_results, TRAFFIC_COLUMNS)
        logger.info(
            f"Batch progress saved: {processed_count} records updated in CSV"
        )
        traffic_results = {}  # Clear for next batch
    logger.info("Finalizing enriched output file...")
    os.rename(temp_path, output_path)
    logger.info(
        f"Traffic analysis completed: {processed_count} locations processed"
    )
    logger.info(f"Enriched CSV with all data saved to: {output_path}")
    return output_path


def process_city_demographics(csv_path: str, batch_size: int, city=CITY_FILTER):
    """
    Process records for demographic analysis and save to a dedicated CSV for a city.
    """
    base_path = csv_path.rsplit(".csv", 1)[0]
    city_csv_path = f"{base_path}_{city}.csv"
    output_path = f"{base_path}_{city}_enriched_with_demographics.csv"
    temp_path = f"{base_path}_{city}_temp_demographics.csv"

    logger.info(f"Starting demographic analysis for {city} locations")
    logger.info(f"Input CSV: {city_csv_path}")
    logger.info(f"Enriched Output CSV: {output_path}")

    ensure_columns_in_csv(city_csv_path, DEMOGRAPHIC_COLUMNS, temp_path)
    locations = get_locations_needing_processing(
        temp_path, "total_population", city
    )
    logger.info(
        f"Found {len(locations)} {city} locations needing demographic analysis"
    )
    if len(locations) == 0:
        logger.info(f"All {city} locations already have demographic data")
        os.rename(temp_path, output_path)
        logger.info(f"All data saved to: {output_path}")
        return output_path

    processed_count = 0
    demo_results = {}
    total_locations = len(locations)

    for batch_start in range(0, total_locations, batch_size):
        batch = locations[batch_start : batch_start + batch_size]
        logger.info(
            f"Processing demographics for batch {batch_start+1}-{min(batch_start+batch_size, total_locations)} of {total_locations}"
        )
        user_id, id_token = login_and_get_user()
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_loc = {
                executor.submit(
                    fetch_demographics,
                    loc["lat"],
                    loc["lng"],
                    user_id,
                    id_token,
                ): loc
                for loc in batch
            }
            for future in as_completed(future_to_loc):
                loc = future_to_loc[future]
                lat, lng = loc["lat"], loc["lng"]
                demo_result = future.result()
                demo_results[f"{lat}_{lng}"] = {
                    **demo_result,
                    "demographics_analysis_date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                processed_count += 1
        logger.info(
            f"Progress checkpoint: {processed_count}/{total_locations} locations processed"
        )
        update_csv_with_results(temp_path, demo_results, DEMOGRAPHIC_COLUMNS)
        logger.info(
            f"Batch progress saved: {processed_count} records updated in CSV"
        )
        demo_results = {}  # Clear for next batch
    logger.info("Finalizing enriched output file...")
    os.rename(temp_path, output_path)
    logger.info(
        f"Demographic analysis completed: {processed_count} locations processed"
    )
    logger.info(f"Enriched CSV with all data saved to: {output_path}")
    return output_path


def process_city_household(csv_path: str, batch_size: int, city=CITY_FILTER):
    """
    Process records for household analysis and save to a dedicated CSV for a city.
    Uses database queries instead of remote API calls.
    """
    base_path = csv_path.rsplit(".csv", 1)[0]
    city_csv_path = f"{base_path}_{city}.csv"
    output_path = f"{base_path}_{city}_enriched_with_household.csv"
    temp_path = f"{base_path}_{city}_temp_household.csv"

    logger.info(f"Starting household analysis for {city} locations")
    logger.info(f"Input CSV: {city_csv_path}")
    logger.info(f"Enriched Output CSV: {output_path}")

    ensure_columns_in_csv(city_csv_path, HOUSEHOLD_COLUMNS, temp_path)
    locations = get_locations_needing_processing(
        temp_path, "total_households", city
    )
    logger.info(
        f"Found {len(locations)} {city} locations needing household analysis"
    )
    if len(locations) == 0:
        logger.info(f"All {city} locations already have household data")
        os.rename(temp_path, output_path)
        logger.info(f"All data saved to: {output_path}")
        return output_path

    processed_count = 0
    hh_results = {}
    total_locations = len(locations)

    for batch_start in range(0, total_locations, batch_size):
        batch = locations[batch_start : batch_start + batch_size]
        logger.info(
            f"Processing household for batch {batch_start+1}-{min(batch_start+batch_size, total_locations)} of {total_locations}"
        )
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_loc = {
                executor.submit(
                    fetch_household_from_db,
                    loc["lat"],
                    loc["lng"],
                    1,
                ): loc
                for loc in batch
            }
            for future in as_completed(future_to_loc):
                loc = future_to_loc[future]
                lat, lng = loc["lat"], loc["lng"]
                try:
                    hh_result = future.result()
                except Exception as e:
                    logger.error(f"Household DB query failed for {lat}, {lng}: {e}")
                    hh_result = {
                        "total_households": 0,
                        "avg_household_size": 0.0,
                        "median_household_size": 0.0,
                        "density_sum": 0.0,
                        "features_count": 0,
                    }

                coord_key = f"{lat}_{lng}"
                hh_results[coord_key] = {
                    **hh_result,
                    "household_analysis_date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                processed_count += 1
        logger.info(
            f"Progress checkpoint: {processed_count}/{total_locations} locations processed"
        )
        update_csv_with_results(temp_path, hh_results, HOUSEHOLD_COLUMNS)
        logger.info(
            f"Batch progress saved: {processed_count} records updated in CSV"
        )
        hh_results = {}  # Clear for next batch
    logger.info("Finalizing enriched output file...")
    os.rename(temp_path, output_path)
    logger.info(
        f"Household analysis completed: {processed_count} locations processed"
    )
    logger.info(f"Enriched CSV with all data saved to: {output_path}")
    return output_path


# process_real_estate_data()
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "..", "saudi_real_estate.csv")
# add_listing_ids_to_csv(csv_path)
# ensure_city_csv(csv_path)
# process_city_demographics(csv_path, 10)
# process_city_traffic(csv_path, 1)
process_city_household(csv_path, batch_size=10, city=CITY_FILTER)
