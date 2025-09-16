#!/usr/bin/env python3
"""
Saudi Real Estate Data Pipeline

This script orchestrates the execution of the Saudi real estate data processing pipeline,
running each step in sequence and ensuring proper logging and error handling.
"""

import subprocess
import sys
import logging
import os
from datetime import datetime

def setup_logging():
    """Set up logging configuration for the Saudi real estate pipeline."""
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log filename with timestamp
    log_filename = os.path.join(log_dir, f"saudi_real_estate_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    return log_filename

def run_step(step_name, script_path):
    """Run a Saudi real estate pipeline step and verify its successful completion."""
    logging.info(f"Starting: {step_name}")
    logging.info(f"Script: {script_path}")
    logging.info("-" * 50)
    
    try:
        # Using current Python interpreter (which will be the virtual environment python)
        # We don't need to specify the virtual environment path since we're already in it
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            text=True
        )
        logging.info(f"SUCCESS: {step_name} completed")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"ERROR: {step_name} failed with exit code {e.returncode}")
        logging.error(f"Output: {e.stdout}")
        logging.error(f"Error: {e.stderr}")
        return False

def main():
    """Main Saudi real estate pipeline orchestration function."""
    log_file = setup_logging()
    logging.info(f"Starting Saudi Real Estate pipeline at {datetime.now()}")
    logging.info(f"Using Python interpreter: {sys.executable}")
    
    # Verify we're running in the virtual environment
    if 'VIRTUAL_ENV' in os.environ:
        logging.info(f"Virtual environment: {os.environ['VIRTUAL_ENV']}")
    else:
        logging.warning("Not running in a virtual environment!")
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define Saudi real estate pipeline steps in sequence
    steps = [
        # {
        #     "name": "Step 1: Acquiring Saudi real estate data",
        #     "script": os.path.join(base_dir, "cron_jobs", "aquire_data", "saudi_real_estate", "step1_scrapy_aquire_data.py")
        # },
        {
            "name": "Step 2: Transforming Saudi real estate data to CSV",
            "script": os.path.join(base_dir, "cron_jobs", "aquire_data", "saudi_real_estate", "step2.py")
        },
        {
            "name": "Step 3: Uploading Saudi real estate data to GCP",
            "script": os.path.join(base_dir, "cron_jobs", "aquire_data", "saudi_real_estate", "step3_upload_gcp.py")
        },
        {
            "name": "Step 4: GBucket to DB transfer",
            "script": os.path.join(base_dir, "cron_jobs", "step4_gbucket_to_db", "step4.py")
        },
        {
            "name": "Step 5: Raw to Ops transformation",
            "script": os.path.join(base_dir, "cron_jobs", "step5_raw_to_ops", "step5.py")
        }
    ]
    
    # Run each step in sequence
    for step in steps:
        if not run_step(step["name"], step["script"]):
            logging.error("Saudi real estate pipeline failed, exiting.")
            sys.exit(1)
    
    logging.info(f"Saudi real estate pipeline completed successfully at {datetime.now()}")
    logging.info(f"Full log available at: {log_file}")
    
if __name__ == "__main__":
    main()