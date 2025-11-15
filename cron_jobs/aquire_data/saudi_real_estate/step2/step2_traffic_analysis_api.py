#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime
from time import sleep

import requests

from cron_jobs.aquire_data.saudi_real_estate.step2.step2 import TRAFFIC_COLUMNS, ensure_columns_in_csv, get_locations_needing_processing, update_csv_with_results

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

API_BASE_URL = "http://49.12.190.229:8000"  # Adjust if needed
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
                "ADMIN_PASSWORD", "123456"
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
                f"{JOB_STATUS_ENDPOINT}/{job_id}", headers=headers, timeout=60
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
                logger.info(f"Job {job_id} status: {status}, remaining: {remaining}")
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
                "traffic_analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
                "traffic_analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        return batch_results


def process_saudi_traffic(csv_path: str, batch_size: int):
    """
    Process records for traffic analysis across all of Saudi Arabia using the API endpoint.
    """
    base_path = csv_path.rsplit(".csv", 1)[0]
    saudi_csv_path = f"{base_path}_saudi.csv"
    output_path = f"{base_path}_saudi_enriched_with_traffic.csv"
    temp_path = f"{base_path}_saudi_traffic_temp_processing.csv"

    logging.info("Starting traffic analysis for all Saudi Arabia locations using API")
    logging.info(f"Input CSV: {saudi_csv_path}")
    logging.info(f"Enriched Output CSV: {output_path}")

    ensure_columns_in_csv(saudi_csv_path, TRAFFIC_COLUMNS, temp_path)
    locations = get_locations_needing_processing(temp_path, "traffic_score")
    logging.info(f"Found {len(locations)} locations needing traffic analysis")

    if len(locations) == 0:
        logging.info("All locations already have traffic data")
        os.rename(temp_path, output_path)
        logging.info(f"All data saved to: {output_path}")
        return output_path

    processed_count = 0
    traffic_results = {}
    total_locations = len(locations)

    # Get authentication token once
    try:
        auth_token = get_auth_token()
        auth_time = datetime.now()
        logging.info("Successfully authenticated with API")
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        return output_path

    # Process locations in batches
    for batch_start in range(0, total_locations, batch_size):
        batch = locations[batch_start : batch_start + batch_size]
        logging.info(
            f"Processing traffic for batch {batch_start + 1}-{min(batch_start + batch_size, total_locations)} of {total_locations}"
        )

        # Check if re-authentication is needed (every ~30 minutes)
        if (datetime.now() - auth_time).total_seconds() > 1800:
            try:
                auth_token = get_auth_token()
                auth_time = datetime.now()
                logging.info("Re-authenticated with API")
            except Exception as e:
                logging.error(f"Re-authentication failed: {e}")
                # Continue with existing token or handle error

        try:
            # Process batch through API
            batch_results = process_traffic_batch(batch, auth_token)
            traffic_results.update(batch_results)
            processed_count += len(batch)

        except Exception as e:
            logging.error(f"Failed to process batch {batch_start}: {e}")
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

        logging.info(
            f"Progress checkpoint: {processed_count}/{total_locations} locations processed"
        )
        update_csv_with_results(temp_path, traffic_results, TRAFFIC_COLUMNS)
        logging.info(f"Batch progress saved: {processed_count} records updated in CSV")
        traffic_results = {}  # Clear for next batch

    logging.info("Finalizing enriched output file...")
    os.rename(temp_path, output_path)
    logging.info(f"Traffic analysis completed: {processed_count} locations processed")
    logging.info(f"Enriched CSV with all data saved to: {output_path}")

    return output_path
