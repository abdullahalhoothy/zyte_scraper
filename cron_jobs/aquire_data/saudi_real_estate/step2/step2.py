import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from time import sleep

import pandas as pd
import requests
from step2_add_demographics import (
    fetch_demographics,
    fetch_household_from_db,
    fetch_housing_from_db,
    login_and_get_user,
)
from step2_extract_listing_id import add_listing_ids_to_csv
from step2_scrapy_transform_to_csv import process_real_estate_data

# from step2_traffic_analysis import GoogleMapsTrafficAnalyzer, logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


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
    "household_analysis_date",
]
HOUSING_COLUMNS = [
    "total_housings",
    "residential_housings",
    "non_residential_housings",
    "owned_housings",
    "rented_housings",
    "provided_housings",
    "other_residential_housings",
    "public_housing",
    "work_camps",
    "commercial_housings",
    "other_housings",
    "density_sum",
    "housing_analysis_date",
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
                city_chunk.to_csv(city_csv_path, index=False, mode="a", header=False)
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
    Process records for traffic analysis using the API endpoint and save to a dedicated CSV for a city.
    """
    base_path = csv_path.rsplit(".csv", 1)[0]
    city_csv_path = f"{base_path}_{city}.csv"
    output_path = f"{base_path}_{city}_enriched_with_traffic.csv"
    temp_path = f"{base_path}_{city}_traffic_temp_processing.csv"

    logger.info(f"Starting traffic analysis for {city} locations using API")
    logger.info(f"Input CSV: {city_csv_path}")
    logger.info(f"Enriched Output CSV: {output_path}")

    ensure_columns_in_csv(city_csv_path, TRAFFIC_COLUMNS, temp_path)
    locations = get_locations_needing_processing(temp_path, "traffic_score", city)
    logger.info(f"Found {len(locations)} {city} locations needing traffic analysis")
    if len(locations) == 0:
        logger.info(f"All {city} locations already have traffic data")
        os.rename(temp_path, output_path)
        logger.info(f"All data saved to: {output_path}")
        return output_path

    processed_count = 0
    traffic_results = {}
    total_locations = len(locations)

    # API configuration
    API_BASE_URL = "http://localhost:8000"  # Adjust if needed
    LOGIN_ENDPOINT = f"{API_BASE_URL}/login"
    ANALYZE_ENDPOINT = f"{API_BASE_URL}/analyze-traffic"
    JOB_STATUS_ENDPOINT = f"{API_BASE_URL}/job"

    # Login to get token (you might want to move this outside the function)
    def get_auth_token() -> str:
        """Get authentication token from the API"""
        try:
            login_data = {
                "username": os.getenv(
                    "ADMIN_USERNAME", "admin"
                ),  # Replace with your username
                "password": os.getenv(
                    "ADMIN_PASSWORD", "password123"
                ),  # Replace with your password
            }
            response = requests.post(LOGIN_ENDPOINT, data=login_data, timeout=30)
            response.raise_for_status()
            token_data = response.json()
            return token_data["access_token"]
        except Exception as e:
            logger.error(f"Failed to get auth token: {e}")
            raise

    def submit_traffic_job(locations_batch, token) -> str | None:
        """Submit a batch of locations for traffic analysis"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            payload = {
                "locations": [
                    {
                        "lat": loc["lat"],
                        "lng": loc["lng"],
                        "storefront_direction": "north",  # Default direction
                        "day": "Monday",  # Default day
                        "time": "6PM",  # Default time (6:00 PM)
                    }
                    for loc in locations_batch
                ]
            }
            response = requests.post(
                ANALYZE_ENDPOINT, json=payload, headers=headers, timeout=30
            )
            response.raise_for_status()
            return response.json()["job_id"]
        except Exception as e:
            logger.error(f"Failed to submit traffic job: {e}")
            raise

    def poll_job_status(job_id, token) -> dict | None:
        """Poll job status until completion"""
        headers = {"Authorization": f"Bearer {token}"}
        max_attempts = 60  # 5 minutes with 5-second intervals
        attempt = 0

        while attempt < max_attempts:
            try:
                response = requests.get(
                    f"{JOB_STATUS_ENDPOINT}/{job_id}", headers=headers, timeout=30
                )
                response.raise_for_status()
                job_data = response.json()

                status = job_data.get("status")

                if status == "done":
                    return job_data
                elif status in ("failed", "canceled"):
                    error_msg = job_data.get("error", "Unknown error")
                    raise Exception(f"Job {status}: {error_msg}")
                elif status in ("pending", "running"):
                    remaining = job_data.get("remaining", 0)
                    logger.info(
                        f"Job {job_id} status: {status}, remaining: {remaining}"
                    )
                    sleep(5)  # Wait 5 seconds before polling again
                    attempt += 1
                else:
                    logger.warning(f"Unknown job status: {status}")
                    sleep(5)
                    attempt += 1

            except Exception as e:
                logger.error(f"Error polling job status: {e}")
                if attempt >= max_attempts - 1:
                    raise
                sleep(5)
                attempt += 1

        raise Exception(f"Job {job_id} timed out after {max_attempts} attempts")

    def process_traffic_batch(locations_batch, token):
        """Process a batch of locations through the API"""
        try:
            # Submit job
            job_id = submit_traffic_job(locations_batch, token)
            logger.info(f"Submitted job {job_id} for {len(locations_batch)} locations")

            # Poll for results
            job_result = poll_job_status(job_id, token)

            # Extract and format results
            batch_results = {}
            results_data = job_result.get("result", {}).get("results", [])

            for loc, result in zip(locations_batch, results_data):
                lat, lng = loc["lat"], loc["lng"]
                coord_key = f"{lat}_{lng}"

                if result.get("error"):
                    logger.error(
                        f"Traffic analysis failed for {lat}, {lng}: {result['error']}"
                    )
                    traffic_score = 0
                    traffic_storefront_score = 0
                    traffic_area_score = 0
                    screenshot_filename = ""
                else:
                    traffic_score = result.get("score", 0)
                    traffic_storefront_score = result.get("storefront_score", 0)
                    traffic_area_score = result.get("area_score", 0)
                    screenshot_url = result.get("screenshot_url", "")
                    screenshot_filename = (
                        os.path.basename(screenshot_url) if screenshot_url else ""
                    )

                batch_results[coord_key] = {
                    "traffic_score": traffic_score,
                    "traffic_storefront_score": traffic_storefront_score,
                    "traffic_area_score": traffic_area_score,
                    "traffic_screenshot_filename": screenshot_filename,
                    "traffic_analysis_date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }

            return batch_results

        except Exception as e:
            logger.error(f"Failed to process traffic batch: {e}")
            # Return empty results for all locations in batch
            batch_results = {}
            for loc in locations_batch:
                lat, lng = loc["lat"], loc["lng"]
                coord_key = f"{lat}_{lng}"
                batch_results[coord_key] = {
                    "traffic_score": 0,
                    "traffic_storefront_score": 0,
                    "traffic_area_score": 0,
                    "traffic_screenshot_filename": "",
                    "traffic_analysis_date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            return batch_results

    # Get authentication token once
    try:
        auth_token = get_auth_token()
        logger.info("Successfully authenticated with API")
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        return output_path

    # Process locations in batches
    for batch_start in range(0, total_locations, batch_size):
        batch = locations[batch_start : batch_start + batch_size]
        logger.info(
            f"Processing traffic for batch {batch_start+1}-{min(batch_start+batch_size, total_locations)} of {total_locations}"
        )

        try:
            # Process batch through API
            batch_results = process_traffic_batch(batch, auth_token)
            traffic_results.update(batch_results)
            processed_count += len(batch)

        except Exception as e:
            logger.error(f"Failed to process batch {batch_start}: {e}")
            # Mark all locations in failed batch as errored
            for loc in batch:
                lat, lng = loc["lat"], loc["lng"]
                coord_key = f"{lat}_{lng}"
                traffic_results[coord_key] = {
                    "traffic_score": 0,
                    "traffic_storefront_score": 0,
                    "traffic_area_score": 0,
                    "traffic_screenshot_filename": "",
                    "traffic_analysis_date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            processed_count += len(batch)

        logger.info(
            f"Progress checkpoint: {processed_count}/{total_locations} locations processed"
        )
        update_csv_with_results(temp_path, traffic_results, TRAFFIC_COLUMNS)
        logger.info(f"Batch progress saved: {processed_count} records updated in CSV")
        traffic_results = {}  # Clear for next batch

    logger.info("Finalizing enriched output file...")
    os.rename(temp_path, output_path)
    logger.info(f"Traffic analysis completed: {processed_count} locations processed")
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
    locations = get_locations_needing_processing(temp_path, "total_population", city)
    logger.info(f"Found {len(locations)} {city} locations needing demographic analysis")
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
        logger.info(f"Batch progress saved: {processed_count} records updated in CSV")
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
    locations = get_locations_needing_processing(temp_path, "total_households", city)
    logger.info(f"Found {len(locations)} {city} locations needing household analysis")
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
        logger.info(f"Batch progress saved: {processed_count} records updated in CSV")
        hh_results = {}  # Clear for next batch
    logger.info("Finalizing enriched output file...")
    os.rename(temp_path, output_path)
    logger.info(f"Household analysis completed: {processed_count} locations processed")
    logger.info(f"Enriched CSV with all data saved to: {output_path}")
    return output_path


def process_city_housing(csv_path: str, batch_size: int, city=CITY_FILTER):
    """
    Process records for housing analysis and save to a dedicated CSV for a city.
    Uses database queries instead of remote API calls.
    """
    base_path = csv_path.rsplit(".csv", 1)[0]
    city_csv_path = f"{base_path}_{city}.csv"
    output_path = f"{base_path}_{city}_enriched_with_housing.csv"
    temp_path = f"{base_path}_{city}_temp_housing.csv"

    logger.info(f"Starting housing analysis for {city} locations")
    logger.info(f"Input CSV: {city_csv_path}")
    logger.info(f"Enriched Output CSV: {output_path}")

    ensure_columns_in_csv(city_csv_path, HOUSING_COLUMNS, temp_path)
    locations = get_locations_needing_processing(temp_path, "total_housings", city)
    logger.info(f"Found {len(locations)} {city} locations needing housing analysis")
    if len(locations) == 0:
        logger.info(f"All {city} locations already have housing data")
        os.rename(temp_path, output_path)
        logger.info(f"All data saved to: {output_path}")
        return output_path

    processed_count = 0
    housing_results = {}
    total_locations = len(locations)

    for batch_start in range(0, total_locations, batch_size):
        batch = locations[batch_start : batch_start + batch_size]
        logger.info(
            f"Processing housing for batch {batch_start+1}-{min(batch_start+batch_size, total_locations)} of {total_locations}"
        )
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_loc = {
                executor.submit(
                    fetch_housing_from_db,
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
                    housing_result = future.result()
                except Exception as e:
                    logger.error(f"Housing DB query failed for {lat}, {lng}: {e}")
                    housing_result = {
                        "total_housings": 0,
                        "residential_housings": 0,
                        "non_residential_housings": 0,
                        "owned_housings": 0,
                        "rented_housings": 0,
                        "provided_housings": 0,
                        "other_residential_housings": 0,
                        "public_housing": 0,
                        "work_camps": 0,
                        "commercial_housings": 0,
                        "other_housings": 0,
                        "density_sum": 0.0,
                    }

                coord_key = f"{lat}_{lng}"
                housing_results[coord_key] = {
                    **housing_result,
                    "housing_analysis_date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                processed_count += 1
        logger.info(
            f"Progress checkpoint: {processed_count}/{total_locations} locations processed"
        )
        update_csv_with_results(temp_path, housing_results, HOUSING_COLUMNS)
        logger.info(f"Batch progress saved: {processed_count} records updated in CSV")
        housing_results = {}  # Clear for next batch
    logger.info("Finalizing enriched output file...")
    os.rename(temp_path, output_path)
    logger.info(f"Housing analysis completed: {processed_count} locations processed")
    logger.info(f"Enriched CSV with all data saved to: {output_path}")
    return output_path


process_real_estate_data()
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "..", "saudi_real_estate.csv")
add_listing_ids_to_csv(csv_path)
ensure_city_csv(csv_path)
process_city_demographics(csv_path, 10)
process_city_traffic(csv_path, 20)  # 1
process_city_household(csv_path, batch_size=10, city=CITY_FILTER)
process_city_housing(csv_path, batch_size=10, city=CITY_FILTER)
