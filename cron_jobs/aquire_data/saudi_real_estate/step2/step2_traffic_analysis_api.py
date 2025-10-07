#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime
from time import sleep

import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

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
