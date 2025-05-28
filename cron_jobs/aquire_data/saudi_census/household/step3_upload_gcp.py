# before importing need to add grandparent directory to path
# currently we are in cron_jobs\aquire_data\saudi_real_estate\step3_upload_gcp.py
# we need to add cron_jobs to path
import sys
import os
import json

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up to the grandparent directory (cron_jobs)
grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..",".."))

# Add the grandparent directory to the system path
sys.path.append(grandparent_dir)


from cron_jobs.step3_add_to_gbucket.upload_to_gbucket import (
    upload_dev_gcp,
    upload_prod_gcp,
)


directories = [{"saudi_census": ["household"]}]

upload_success = upload_dev_gcp(directories)
print(upload_success)

# upload_success = upload_prod_gcp(directories)
# print(upload_success)
