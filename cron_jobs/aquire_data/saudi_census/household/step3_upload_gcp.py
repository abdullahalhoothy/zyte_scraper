import sys
import os
# import json # Likely not needed if directories is hardcoded

current_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the main 'cron_jobs' directory from 'household' dir
grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))
sys.path.append(grandparent_dir)

from cron_jobs.step3_add_to_gbucket.upload_to_gbucket import (
    upload_dev_gcp,
    upload_prod_gcp,
)

# Specific for household
directories = [{"saudi_census": ["household"]}] 

upload_success_dev = upload_dev_gcp(directories)
print(f"Development upload success for household: {upload_success_dev}")

# upload_success_prod = upload_prod_gcp(directories)
# print(f"Production upload success for household: {upload_success_prod}")

try:
    sys.path.remove(grandparent_dir)
except ValueError:
    pass
