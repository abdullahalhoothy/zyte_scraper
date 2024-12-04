from dataclasses import dataclass
import json



def load_config(file_path="cron_jobs/aquire_data/aqar_zyte_gbucket_db/secret_config.json"):
    with open(file_path, "r") as config_file:
        return json.load(config_file)


def create_links_to_scrap() -> dict:
    
    cities = {
        "baqa":"%D8%A8%D9%82%D8%B9%D8%A7%D8%A1"
        # "jazan":"%D8%AC%D8%A7%D8%B2%D8%A7%D9%86",
        # "riydah":"%D8%B9%D9%82%D8%A7%D8%B1%D8%A7%D8%AA"
    }
    
    
    categories = {
        "land_sale":"%D8%A3%D8%B1%D8%A7%D8%B6%D9%8A-%D9%84%D9%84%D8%A8%D9%8A%D8%B9"
        # "villa_allrooms":"%D9%81%D9%84%D9%84-%D9%84%D9%84%D8%A8%D9%8A%D8%B9"
    }
    
    
    output = {
        
    }
    
    for city,city_coded_name in cities.items():
        for category,category_coded_name in categories.items():
            output[city+'_'+category] = "https://sa.aqar.fm/"+category_coded_name+'/'+city_coded_name
    
    return output

@dataclass
class ScraperConfig:
    api_key: str
    zyte_api_url: str
    base_url_info: dict
    listing_regex: str
    expected_listing_count: int
    pages_to_scrape_per_worker: tuple
    max_concurrent_requests: int
    pages_to_crawl_per_worker: tuple
    last_page_check_number: int
    last_page_regex: str
    crawling_progress_file_name: str
    response_data_file_name: str
    irregular_pages_file: str
    crawling_delay: tuple
    scraping_delay: tuple


CONF = ScraperConfig(
    api_key=load_config()["api_key"],
    zyte_api_url="https://api.zyte.com/v1/extract",
    base_url_info=create_links_to_scrap(),
    listing_regex=r'href="(/\d+/.*?)"',
    expected_listing_count=20,
    max_concurrent_requests=1,
    pages_to_scrape_per_worker=(8, 14),
    pages_to_crawl_per_worker=(1, 1),
    last_page_check_number=999,
    last_page_regex=r"/(\d+)$",
    crawling_progress_file_name="progress.json",
    response_data_file_name="response_data.json",
    irregular_pages_file="irregular_pages.json",
    crawling_delay=(1, 5),
    scraping_delay=(1, 5),
)