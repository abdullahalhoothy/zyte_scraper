#!/usr/bin/env python3
"""
Data Pipeline

This script orchestrates the execution of the  data processing pipeline,
running each step in sequence and ensuring proper logging and error handling.
"""

import subprocess
import sys
import logging
import os
from datetime import datetime
from logging_utils import setup_logging

def run_step(step_name, script_path, log_file):
    """Run a Saudi DB Enrichment pipeline step and verify its successful completion."""
    logging.info(f"Starting: {step_name}")
    logging.info(f"Script: {script_path}")
    logging.info("-" * 50)

    try:
        result = subprocess.run(
            [sys.executable, script_path, "--log-file", log_file],
            check=True,
            text=True,
            capture_output=True
        )

        # Log output from the step
        if result.stdout:
            logging.info(result.stdout.strip())
        if result.stderr:
            logging.warning(result.stderr.strip())

        logging.info(f"SUCCESS: {step_name} completed")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"ERROR: {step_name} failed with exit code {e.returncode}")
        if e.stdout:
            logging.error(f"Output: {e.stdout}")
        if e.stderr:
            logging.error(f"Error: {e.stderr}")
        return False
  
def main():
    """Main pipeline orchestration function."""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"main_pipeline{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    setup_logging(log_file)
    logging.info(f"Starting pipeline at {datetime.now()}")
    logging.info(f"Using Python interpreter: {sys.executable}")
    
    # Verify we're running in the virtual environment
    if 'VIRTUAL_ENV' in os.environ:
        logging.info(f"Virtual environment: {os.environ['VIRTUAL_ENV']}")
    else:
        logging.warning("Not running in a virtual environment!")
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define  pipeline steps in sequence
    steps = [
        {
            "name": "Executing Saudi Census pipeline",
            "script": os.path.join(base_dir,  "aqar_saudi_census_pipeline.py")
        },
        {
            "name": "Executing Zad Income pipeline",
            "script": os.path.join(base_dir, "aqar_zad_income_pipeline.py")
        },
        {
            "name": "Executing Saudi Real Estate pipeline",
            "script": os.path.join(base_dir,  "aqar_real_estate_pipeline.py")
        },
        {
            "name": "Executing DB Enrichment pipeline",
            "script": os.path.join(base_dir, "aqar_db_enrichment_pipeline.py")
        },
    ]
    
    # Run each step in sequence
    for step in steps:
        if not run_step(step["name"], step["script"], log_file):
            logging.error(" pipeline failed, exiting.")
            sys.exit(1)
    
    logging.info(f"Data pipeline completed successfully at {datetime.now()}")
    logging.info(f"Full log available at: {log_file}")
    
if __name__ == "__main__":
    main()