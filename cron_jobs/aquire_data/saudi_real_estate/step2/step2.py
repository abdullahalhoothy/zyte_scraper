import os
from step2_scrapy_transform_to_csv import process_real_estate_data
from step2_traffic_analysis import process_riyadh_real_estate_traffic



process_real_estate_data()
# Get the directory of the current file and construct relative path
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "..", "saudi_real_estate.csv")
process_riyadh_real_estate_traffic(csv_path, 2)