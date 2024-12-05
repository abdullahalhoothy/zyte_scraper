from dataclasses import dataclass
import json



def load_config(file_path="cron_jobs/aquire_data/aqar_zyte_gbucket_db/secret_config.json"):
    with open(file_path, "r") as config_file:
        return json.load(config_file)


def create_links_to_scrap() -> dict:
    
    cities = {
    "riyadh": "%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6",
    "jeddah": "%D8%AC%D8%AF%D8%A9",
    "dammam": "%D8%A7%D9%84%D8%AF%D9%85%D8%A7%D9%85",
    "khobar": "%D8%A7%D9%84%D8%AE%D8%A8%D8%B1",
    "medina": "%D8%A7%D9%84%D9%85%D8%AF%D9%8A%D9%86%D8%A9-%D8%A7%D9%84%D9%85%D9%86%D9%88%D8%B1%D8%A9",
    "mecca": "%D9%85%D9%83%D8%A9-%D8%A7%D9%84%D9%85%D9%83%D8%B1%D9%85%D8%A9",
    "buraidah": "%D8%A8%D8%B1%D9%8A%D8%AF%D8%A9",
    "taif": "%D8%A7%D9%84%D8%B7%D8%A7%D8%A6%D9%81",
    "khamis_mushait": "%D8%AE%D9%85%D9%8A%D8%B3-%D9%85%D8%B4%D9%8A%D8%B7",
    "abha": "%D8%A7%D8%A8%D9%87%D8%A7",
    "al_hufuf": "%D8%A7%D9%84%D9%87%D9%81%D9%88%D9%81",
    "jazan": "%D8%AC%D8%A7%D8%B2%D8%A7%D9%86",
    "alziziyah": "%D8%A7%D9%84%D8%B2%D9%8A%D8%B2%D9%8A%D8%A9",
    "aniyza": "%D8%B9%D9%86%D9%8A%D8%B2%D8%A9",
    "al_kharj": "%D8%A7%D9%84%D8%AE%D8%B1%D8%AC",
    "jubail": "%D8%A7%D9%84%D8%AC%D8%A8%D9%8A%D9%84",
    "dhahran": "%D8%A7%D9%84%D8%B8%D9%87%D8%B1%D8%A7%D9%86",
    "hail": "%D8%AD%D8%A7%D8%A6%D9%84",
    "al_bukayriyah": "%D8%A7%D9%84%D8%A8%D9%83%D9%8A%D8%B1%D9%8A%D8%A9",
    "al_mujamma": "%D8%A7%D9%84%D9%85%D8%AC%D9%85%D8%B9%D8%A9",
    "al_diryah": "%D8%A7%D9%84%D8%AF%D8%B1%D8%B9%D9%8A%D8%A9",
    "tabuk": "%D8%AA%D8%A8%D9%88%D9%83",
    "abu_arish": "%D8%A3%D8%A8%D9%88-%D8%B9%D8%B1%D9%8A%D8%B4",
    "thadiq": "%D8%AB%D8%A7%D8%AF%D9%82",
    "hafr_al_batin": "%D8%AD%D9%81%D8%B1-%D8%A7%D9%84%D8%A8%D8%A7%D8%AA%D9%86",
    "al_baha": "%D8%A7%D9%84%D8%A8%D8%A7%D9%87%D8%A9",
    "alzulfy": "%D8%A7%D9%84%D8%B2%D9%84%D9%81%D9%8A",
    "riyadh_khobar": "%D8%B1%D9%8A%D8%A7%D8%B6-%D8%A7%D9%84%D8%AE%D8%A8%D8%B1",
    "safwa": "%D8%B5%D9%81%D9%88%D8%A9",
    "al_rass": "%D8%A7%D9%84%D8%B1%D8%A7%D8%B3",
    "al_quwayiyah": "%D8%A7%D9%84%D9%82%D9%88%D9%8A%D8%A9",
    "al_na'iriyah": "%D8%A7%D9%84%D9%86%D8%B9%D9%8A%D8%B1%D9%8A%D8%A9",
    "al_shuqra": "%D8%A7%D9%84%D8%B4%D9%82%D8%B1%D8%A7",
    "thuwal": "%D8%AB%D9%88%D9%84",
    "al_dawadmi": "%D8%A7%D9%84%D8%AF%D9%88%D8%A7%D8%AF%D9%85%D9%8A",
    "baqiq": "%D8%A8%D9%82%D9%8A%D9%82",
    "muhayil": "%D9%85%D8%AD%D8%A7%D9%8A%D9%84",
    "king_abdullah_economic_city": "%D9%85%D8%AF%D9%8A%D9%86%D8%A9-%D8%A7%D9%84%D9%85%D9%84%D9%83-%D8%B9%D8%A8%D8%AF%D8%A7%D9%84%D9%84%D9%87-%D8%A7%D9%84%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF%D9%8A%D8%A9",
    "al_badiyah": "%D8%A7%D9%84%D8%A8%D8%AF%D8%A7%D8%A6%D8%B9",
    "najran": "%D9%86%D8%AC%D8%B1%D8%A7%D9%86",
    "al_mujardah": "%D8%A7%D9%84%D9%85%D8%AC%D8%A7%D8%B1%D8%AF%D8%A9",
    "rabab": "%D8%B1%D8%A7%D8%A8%D8%BA",
    "bisha": "%D8%A8%D9%8A%D8%B4%D8%A9",
    "al_nabahaniyah": "%D8%A7%D9%84%D9%86%D8%A8%D9%87%D8%A7%D9%86%D9%8A%D8%A9",
    "bish": "%D8%A8%D9%8A%D8%B4",
    "al_qunfudhah": "%D8%A7%D9%84%D9%82%D9%86%D9%81%D8%B0%D8%A9",
    "al_khafji": "%D8%A7%D9%84%D8%AE%D9%81%D8%AC%D9%8A",
    "sabiya": "%D8%B5%D8%A8%D9%8A%D8%A7",
    "al_haytham": "%D8%A7%D9%84%D9%87%D9%8A%D8%A7%D8%AB%D9%85",
    "biqaa": "%D8%A8%D9%82%D8%B9%D8%A7%D8%A1",
    "al_hanaqiyah": "%D8%A7%D9%84%D8%AD%D9%86%D8%A7%D9%83%D9%8A%D8%A9",
    "ar'ar": "%D8%B9%D8%B1%D8%B9%D8%B1",
    "al_shinan": "%D8%A7%D9%84%D8%B4%D9%86%D8%A7%D9%86",
    "al_qatif": "%D8%A7%D9%84%D9%82%D8%B7%D9%8A%D9%81",
    "ramah": "%D8%B1%D9%85%D8%A7%D8%AD",
    "hota_bani_tamim": "%D8%AD%D9%88%D8%B7%D8%A9-%D8%A8%D9%86%D9%8A-%D8%AA%D9%85%D9%8A%D9%85",
    "al_ghazalah": "%D8%A7%D9%84%D8%BA%D8%B2%D8%A7%D9%84%D8%A9"
}

    
    categories = {
    "apartments_for_rent": "%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1",
    "lands_for_sale": "%D8%A3%D8%B1%D8%A7%D8%B6%D9%8A-%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
    "villas_for_sale": "%D9%81%D9%84%D9%84-%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
    "houses_for_rent": "%D8%AF%D9%88%D8%B1-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1",
    "villas_for_rent": "%D9%81%D9%84%D9%84-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1",
    "apartments_for_sale": "%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
    "buildings_for_sale": "%D8%B9%D9%85%D8%A7%D8%A6%D8%B1-%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
    "shops_for_rent": "%D9%85%D8%AD%D9%84%D8%A7%D8%AA-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1",
    "house_for_sale": "%D8%A8%D9%8A%D8%AA-%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
    "chalet_for_sale": "%D8%A7%D8%B3%D8%AA%D8%B1%D8%A7%D8%AD%D8%A9-%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
    "house_for_rent": "%D8%A8%D9%8A%D8%AA-%D9%84%D9%84%D8%A5%D8%AC%D8%A7%D8%B1",
    "farm_for_sale": "%D9%85%D8%B2%D8%B1%D8%B9%D8%A9-%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
    "chalet_for_rent": "%D8%A7%D8%B3%D8%AA%D8%B1%D8%A7%D8%AD%D8%A9-%D9%84%D9%84%D8%A5%D8%AC%D8%A7%D8%B1",
    "commercial_office_for_rent": "%D9%85%D9%83%D8%AA%D8%A8-%D8%AA%D8%AC%D8%A7%D8%B1%D9%8A-%D9%84%D9%84%D8%A5%D8%AC%D8%A7%D8%B1",
    "lands_for_rent": "%D8%A3%D8%B1%D8%A7%D8%B6%D9%8A-%D9%84%D9%84%D8%A5%D8%AC%D8%A7%D8%B1",
    "buildings_for_rent": "%D8%B9%D9%85%D8%A7%D8%A6%D8%B1-%D9%84%D9%84%D8%A5%D8%AC%D8%A7%D8%B1",
    "warehouse_for_rent": "%D9%85%D8%B3%D8%AA%D9%88%D8%AF%D8%B9-%D9%84%D9%84%D8%A5%D8%AC%D8%A7%D8%B1",
    "camp_for_rent": "%D9%85%D8%AE%D9%8A%D9%85-%D9%84%D9%84%D8%A5%D8%AC%D8%A7%D8%B1",
    "rooms_for_rent": "%D8%BA%D8%B1%D9%81-%D9%84%D9%84%D8%A5%D8%AC%D8%A7%D8%B1",
    "shops_for_sale": "%D9%85%D8%AD%D9%84%D8%A7%D8%AA-%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
    "furnished_apartment": "%D8%B4%D9%82%D8%A9-%D9%85%D9%81%D8%B1%D9%88%D8%B4%D8%A9",
    "house_for_sale_2": "%D8%AF%D9%88%D8%B1-%D9%84%D9%84%D8%A8%D9%8A%D8%B9",
    "chalet_for_rent_2": "%D8%B4%D8%A7%D9%84%D9%8A%D9%87-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1"
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