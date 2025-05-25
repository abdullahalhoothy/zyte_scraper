# before importing need to add grandparent directory to path
# currently we are in cron_jobs\aquire_data\saudi_census\population\step3_upload_gcp.py
# we need to add cron_jobs to path
import sys
import os
import json # Although json might not be strictly needed if directories is hardcoded

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up to the grandparent directory (cron_jobs)
# cron_jobs/aquire_data/saudi_census/population -> cron_jobs/aquire_data/saudi_census -> cron_jobs/aquire_data -> cron_jobs
grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "..")) 

# Add the grandparent directory to the system path
sys.path.append(grandparent_dir)


from cron_jobs.step3_add_to_gbucket.upload_to_gbucket import (
    upload_dev_gcp,
    upload_prod_gcp,
)


directories = [{"saudi_census": ["population"]}]

upload_success = upload_dev_gcp(directories)
print(upload_success) # Original likely printed the return of the function

# upload_success = upload_prod_gcp(directories)
# print(upload_success) # Original likely printed this as well

# It's good practice to remove the path from sys.path if it's no longer needed,
# especially if this script could be imported by another.
# However, if it's a standalone script that exits, it might be omitted.
# For robustness, let's try to add it.
try:
    sys.path.remove(grandparent_dir)
except ValueError:
    pass # In case it was already removed or not there for some reason
