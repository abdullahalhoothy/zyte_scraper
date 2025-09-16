from step2.step2_scrapy_transform_to_csv import process_real_estate_data
from step2.step2_traffic_analysis import process_riyadh_real_estate_traffic



process_real_estate_data()
csv_path = r"F:\git\zyte_scraper\cron_jobs\aquire_data\saudi_real_estate\saudi_real_estate.csv"
process_riyadh_real_estate_traffic(csv_path, 2)