#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime
from typing import Any

import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

API_BASE_URL = "http://157.180.121.131:8000"  # Adjust if needed
LOGIN_ENDPOINT = f"{API_BASE_URL}/login"
ANALYZE_ENDPOINT = f"{API_BASE_URL}/process-locations"


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


def submit_traffic_job(
    locations_batch: list[dict[str, Any]], token: str
) -> dict[str, Any]:
    """Submit a batch of locations for traffic analysis"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "save_to_static": True,
            "save_to_db": True,
            "locations": [
                {
                    "lat": loc["lat"],
                    "lng": loc["lng"],
                    "storefront_direction": "north",  # Default direction
                    "day": "Monday",  # Default day
                    "time": "6PM",  # Default time (6:00 PM)
                    # "zoom": 18, # Default zoom (18z)
                }
                for loc in locations_batch
            ],
        }
        response = requests.post(
            ANALYZE_ENDPOINT, json=payload, headers=headers, timeout=200
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to submit traffic processing: {e}")
        raise


def process_traffic_batch(
    locations_batch: list[dict[str, Any]], token: str
) -> dict[str, Any]:
    """Process a batch of locations through the API"""
    try:
        # Submit job
        resp = submit_traffic_job(locations_batch, token)
        logger.info(
            f"Submitted process request {resp.get('request_id', '')} for {len(locations_batch)} locations"
        )

        # Extract and format results
        batch_results = {}
        results_data = resp.get("result", [])

        for loc, result in zip(locations_batch, results_data):
            lat, lng = loc["lat"], loc["lng"]
            coord_key = f"{lat}_{lng}"
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
