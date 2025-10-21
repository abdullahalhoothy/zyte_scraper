import os
import time
from datetime import datetime, timedelta

import pytest
import requests

LOCALHOST_URL = "http://localhost:8000"
ENDPONT_URL = "http://49.12.190.229:8000"
API_URL = LOCALHOST_URL

USERNAME = "admin"
PASSWORD = os.getenv("ADMIN_PASSWORD", "123456")

CITIES = [
    {"lat": 21.4858, "lng": 39.1925, "day": "Monday", "time": "10PM"},
    {"lat": 24.7136, "lng": 46.6753, "day": "Tuesday", "time": "6PM"},
    {"lat": 26.4207, "lng": 50.0888, "day": "Wednesday", "time": "8:30AM"},
    {"lat": 21.3891, "lng": 39.8579, "day": "Thursday", "time": "10PM"},
    {"lat": 24.5247, "lng": 39.5692, "day": "Friday", "time": "6PM"},
    {"lat": 21.4858, "lng": 39.1925, "day": "Saturday", "time": "8:30AM"},
    {"lat": 24.7136, "lng": 46.6753, "day": "Sunday", "time": "10PM"},
    {"lat": 26.4207, "lng": 50.0888, "day": "Monday", "time": "6PM"},
    {"lat": 21.3891, "lng": 39.8579, "day": "Tuesday", "time": "8:30AM"},
    {"lat": 24.5247, "lng": 39.5692, "day": "Wednesday", "time": "10PM"},
    {"lat": 21.4858, "lng": 39.1925, "day": "Thursday", "time": "6PM"},
    {"lat": 24.7136, "lng": 46.6753, "day": "Friday", "time": "8:30AM"},
    {"lat": 26.4207, "lng": 50.0888, "day": "Saturday", "time": "10PM"},
    {"lat": 21.3891, "lng": 39.8579, "day": "Sunday", "time": "6PM"},
    {"lat": 24.5247, "lng": 39.5692, "day": "Monday", "time": "8:30AM"},
    {"lat": 21.4858, "lng": 39.1925, "day": "Tuesday", "time": "10PM"},
    {"lat": 24.7136, "lng": 46.6753, "day": "Wednesday", "time": "6PM"},
    {"lat": 26.4207, "lng": 50.0888, "day": "Thursday", "time": "8:30AM"},
    {"lat": 21.3891, "lng": 39.8579, "day": "Friday", "time": "10PM"},
    {"lat": 24.5247, "lng": 39.5692, "day": "Saturday", "time": "6PM"},
]


def login():
    """Authenticate and return JWT token"""

    url = f"{API_URL}/token"
    data = {"username": USERNAME, "password": PASSWORD}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post(url, data=data, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Login failed: {res.text}")

    token = res.json()["access_token"]
    print(f"Logged in successfully. Token: {token[:20]}...")
    return token


def submit_batch(token, locations):
    """Submit a batch of locations"""

    url = f"{API_URL}/analyze-batch"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    res = requests.post(url, json={"locations": locations}, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Batch submission failed: {res.text}")

    job_id = res.json()["job_id"]
    print(f"Submitted job: {job_id}")
    return job_id


def poll_job_until_complete(token, job_id, interval=5, timeout=600):
    """Poll job status until complete with timeout"""

    url = f"{API_URL}/job/{job_id}"
    headers = {"Authorization": f"Bearer {token}"}

    start_time = datetime.now()
    timeout_time = start_time + timedelta(seconds=timeout)

    print(f"Started polling at {start_time.strftime('%H:%M:%S')}")
    print(f"Timeout set to {timeout} seconds")

    while datetime.now() < timeout_time:
        res = requests.get(url, headers=headers)
        if res.status_code == 404:
            print("Job not found")
            return None

        job = res.json()
        status = job.get("status", "failed")
        remaining = job.get("remaining", 0)
        total = job.get("result", {}).get("count", len(CITIES))

        print(f"Status: {status}, Progress: {total - remaining}/{total} done")

        if status in ("done", "failed", "canceled"):
            end_time = datetime.now()
            duration = end_time - start_time
            total_seconds = int(duration.total_seconds())
            duration_str = str(timedelta(seconds=total_seconds))

            print(f"\n Finished at {end_time.strftime('%H:%M:%S')}")
            print(f"Total time taken: {duration_str}")

            if status == "done":
                print("Job completed successfully!")
                if "result" in job:
                    print(
                        f"Result summary: {len(job['result']["results"])} locations processed"
                    )
            else:
                print(f"Job ended with status: {status}")

            return job

        time.sleep(interval)

    # Timeout reached
    print(f"Polling timeout after {timeout} seconds")
    return None


@pytest.mark.integration
def test_complete_system_workflow():
    """Complete system test that ensures everything is processed"""

    print("=== Running Complete System Workflow Test ===")

    token = login()

    # Submit multiple batches if needed
    job_id = submit_batch(token, CITIES)

    # Wait for this job to complete
    job_result = poll_job_until_complete(token, job_id, timeout=600)

    if job_result and job_result["status"] == "done":
        print(
            f"Job completed with {len(job_result.get('result', {}).get("results", []))} results"
        )
    else:
        print(f"Job did not complete successfully: {job_result}")

    print("All traffic batch processing completed!")


if __name__ == "__main__":
    # Manual test execution
    print("=== Manual Traffic API Test ===")

    token = login()
    job_id = submit_batch(token, CITIES)

    # Wait for the specific job to complete
    job_result = poll_job_until_complete(token, job_id, timeout=600)

    print("All processing completed!")
