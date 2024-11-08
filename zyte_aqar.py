import asyncio
import json
import logging
import os
import random
from base64 import b64decode, b64encode
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, List, Union

from store_json_into_db import save_to_db

import aiofiles
import aiohttp

from aqar_html_parsers import get_last_page, extract_listing_hrefs, extract_all_data


def setup_logger():
    logger_cls = logging.getLogger(__name__)
    logger_cls.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger_cls.addHandler(console_handler)

    file_handler = logging.FileHandler('crawler.log')
    file_handler.setFormatter(formatter)
    logger_cls.addHandler(file_handler)

    return logger_cls


logger = setup_logger()


class RequestError(Exception):
    pass


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


# Load configuration from a JSON file
def load_config(file_path='secret_config.json'):
    with open(file_path, 'r') as config_file:
        return json.load(config_file)


CONF = ScraperConfig(
    api_key=load_config()["api_key"],
    zyte_api_url="https://api.zyte.com/v1/extract",
    base_url_info={
        "shaqra_villa_allrooms":"https://sa.aqar.fm/%D9%81%D9%84%D9%84-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%B4%D9%82%D8%B1%D8%A7%D8%A1",
        "sqdiq_villa_allrooms":"https://sa.aqar.fm/%D9%81%D9%84%D9%84-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%AB%D8%A7%D8%AF%D9%82"
        # "riyadh_villa_allrooms": "https://sa.aqar.fm/%D9%81%D9%84%D9%84-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6",
        # Add more base URLs here
    },
    listing_regex=r'href="(/\d+/.*?)"',
    expected_listing_count=20,
    max_concurrent_requests=1,
    pages_to_scrape_per_worker=(8, 14),
    pages_to_crawl_per_worker=(1, 1),
    last_page_check_number=999,
    last_page_regex=r'/(\d+)$',
    crawling_progress_file_name='progress.json',
    response_data_file_name='response_data.json',
    irregular_pages_file="irregular_pages.json",
    crawling_delay=(1, 5),
    scraping_delay=(1, 5),
)


class FileLock:
    def __init__(self):
        self.locks = {}

    @asynccontextmanager
    async def acquire(self, filename):
        if filename not in self.locks:
            self.locks[filename] = asyncio.Lock()

        await self.locks[filename].acquire()
        try:
            yield
        finally:
            self.locks[filename].release()


file_lock_manager = FileLock()


async def use_json(filename: str, keys: Union[str, List[str]] = None,
                   value: Any = None, extend_list_value: bool = False, recreate_file: bool = False) -> Any:
    async with file_lock_manager.acquire(filename):
        if recreate_file:
            if os.path.exists(filename):
                os.remove(filename)
            data = {}
        else:
            try:
                async with aiofiles.open(filename, mode='r') as f:
                    data = json.loads(await f.read())
            except FileNotFoundError:
                data = {}

        if keys is not None:
            if isinstance(keys, str):
                keys = [keys]

            if value is not None:
                # Write or append mode
                current = data
                for key in keys[:-1]:
                    current = current.setdefault(key, {})

                if extend_list_value and isinstance(current.get(keys[-1]), list):
                    current[keys[-1]].extend(value)
                else:
                    current[keys[-1]] = value

                async with aiofiles.open(filename, mode='w') as f:
                    json_string = json.dumps(data, indent=2)
                    await f.write(json_string)
                return value
            else:
                # Read key mode
                current = data
                for key in keys:
                    if isinstance(current, dict) and key in current:
                        current = current[key]
                    else:
                        return None
                return current
        else:
            # If no keys are provided and value is not None, replace entire file content
            if value is not None and recreate_file:
                data = value
                async with aiofiles.open(filename, mode='w') as f:
                    json_string = json.dumps(data, indent=2)
                    await f.write(json_string)
            # Return all data if no key is specified and no value to write
            return data


async def make_zyte_request(client, url, response_data_file_path, max_retries=5, parsing_func=None):
    for attempt in range(max_retries):
        try:
            # Try to get cached response
            cached_response = await use_json(response_data_file_path, keys=url)
            if cached_response and cached_response != {} and cached_response != '':
                logger.info(f"Using cached response for {url}")
                try:
                    return b64decode(cached_response).decode('utf-8')
                except UnicodeDecodeError:
                    return cached_response

            auth_string = b64encode(f"{CONF.api_key}:".encode()).decode()
            headers = {"Authorization": f"Basic {auth_string}"}

            request_params = {
                "url": CONF.zyte_api_url,
                "json": {
                    "url": url,
                    "httpResponseBody": True,
                    # "ipType":"residential",
                    # "geolocation":"CA",
                    "echoData": url,
                    # "sessionContext": [], # don't know how to use it , but helps avoid bans
                    # "sessionContextParameters": "", # goes with the above
                },
                "headers": headers,
                "timeout": 30  # Set a timeout for the request
            }
            logger.info(f"Attempting to make request to {url}")
            async with client.post(**request_params) as response:
                logger.info(f"Request to {url} successful")
                response_json = await response.json()
                status_code = response.status

                if status_code == 200:
                    http_response_body = response_json.get("httpResponseBody", "")
                    return_data = b64decode(http_response_body)
                    save_data = http_response_body
                    if parsing_func is not None:
                        return_data = parsing_func(return_data)
                        save_data = return_data
                    echodata = response_json.get("echoData", "")
                    await use_json(response_data_file_path, keys=url, value=save_data)
                    logger.info(f"Successfully retrieved and saved response for {url}")
                    return return_data

                elif status_code in [400, 401, 403, 422, 451, 500, 521]:
                    error_detail = response_json.get('detail', 'No detail provided')
                    raise RequestError(f"Error {status_code}: {error_detail}")
                elif status_code in [429, 503, 520]:
                    retry_after = int(response.headers.get('Retry-After', 2))
                    raise RequestError(f"Error {status_code}: Too many requests. Retry after {retry_after} seconds.")
                else:
                    raise RequestError(f"Unexpected status code: {status_code}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error occurred while requesting {url}: {str(e)}")
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON response for {url}")
        except RequestError as e:
            logger.error(str(e))
            if "429" in str(e) or "503" in str(e) or "520" in str(e):
                retry_after = int(str(e).split()[-2])  # Extract retry_after value from error message
                await asyncio.sleep(max(retry_after, 2 ** attempt))
                continue
        except Exception as e:
            logger.error(f"Unexpected error occurred while requesting {url}: {str(e)}")

            # Exponential backoff
        delay = 2 ** attempt
        logger.warning(f"Retrying request for {url} (attempt {attempt + 1} of {max_retries}) after {delay} seconds")
        await asyncio.sleep(delay)

    logger.error(f"Failed to get valid response for {url} after {max_retries} attempts")
    return ""


async def fetch_crawling_prog(dir_name, base_url):
    crawling_prog_file = f"{dir_name}/{CONF.crawling_progress_file_name}"
    crawling_prog = await use_json(crawling_prog_file)
    crawled_pages = None
    pages_to_process = None
    last_page = None
    if base_url in crawling_prog:
        logger.info(f"Starting crawl_page_batch for {base_url}")
        crawled_pages = crawling_prog[base_url]['crawled_pages']
        scraped_all_listings_from_pages = crawling_prog[base_url].get('scraped_all_listings_from_pages', [])
        pages_to_process = [page for page in crawled_pages if
                            page not in scraped_all_listings_from_pages]
        last_page = crawling_prog[base_url]['last_page']
        pages_to_process.sort()

    return crawling_prog, crawled_pages, pages_to_process, last_page


async def update_crawling_prog(dir_name, key, value, **kwargs):
    await use_json(f"{dir_name}/{CONF.crawling_progress_file_name}", keys=key, value=value, **kwargs)


async def initialize_base_url_if_new(client, dir_name, base_url):
    url = f"{base_url}/{CONF.last_page_check_number}"
    response_data_file_path = f"{dir_name}/{CONF.response_data_file_name}"
    response_data = await make_zyte_request(client, url, response_data_file_path)
    crawling_prog, _, _, _ = await fetch_crawling_prog(dir_name, base_url)
    if base_url not in crawling_prog:
        crawling_prog[base_url] = {
            'last_page': get_last_page(response_data),
            'crawled_pages': []
        }
        await update_crawling_prog(dir_name, key=base_url, value=crawling_prog[base_url])


async def check_page_fully_scraped(selected_page, dir_name, base_url):
    page_response_file = f"{dir_name}/{selected_page}_response_data.json"
    page_response_data = await use_json(page_response_file)
    remaining_urls = [url for url, value in page_response_data.items() if value == '']
    if page_response_data == {}:
        remaining_urls = [20]  # TODO temp fix
    if len(remaining_urls) == 0:
        await update_crawling_prog(dir_name, key=[base_url, 'scraped_all_listings_from_pages'], value=[selected_page],
                                   extend_list_value=True)
        logger.info(f"page={selected_page} fully scrapped")


async def process_listings(client, selected_page, dir_name):
    logger.info(f"Scraping page={selected_page}")
    page_response_file = f"{dir_name}/{selected_page}_response_data.json"
    page_response_data = await use_json(page_response_file)
    all_listing_urls = [url for url, value in page_response_data.items() if value == '']
    logger.info(f"Found {len(all_listing_urls)} available urls to scrape in page={selected_page}")
    sample_size = min(len(all_listing_urls), random.randint(*CONF.pages_to_scrape_per_worker))
    random_sample = random.sample(all_listing_urls, sample_size)
    logger.info(f"beginning to scrape {len(random_sample)} urls of {len(all_listing_urls)} available urls")
    for url in random_sample:
        try:

            await make_zyte_request(client, url, page_response_file, parsing_func=extract_all_data)
            delay = random.uniform(*CONF.scraping_delay)
            logger.info(f"Successfully make_zyte_request sleeping for {delay:.2f} seconds")
            await asyncio.sleep(delay)
        except Exception as exce:
            print(f"Error processing listing {url}: {str(exce)}")
    logger.info(f"worked on {len(random_sample)} elements in page {selected_page}")


async def scrape_urls_of_page(client, base_url, dir_name, worker_id):
    _, _, pages_to_process, _ = await fetch_crawling_prog(dir_name, base_url)
    logger.info(f"Worker {worker_id} started scrape_urls_of_page")

    if pages_to_process:
        selected_page = pages_to_process[worker_id]
        await process_listings(client, selected_page, dir_name)
        await check_page_fully_scraped(selected_page, dir_name, base_url)


async def crawl_page_batch(client, base_url, dir_name):
    _, crawled_pages, _, last_page = await fetch_crawling_prog(dir_name, base_url)
    logger.info(f"Fetched crawling progress: {len(crawled_pages)} pages crawled, last page is {last_page}")

    if len(crawled_pages) >= last_page:
        logger.info("All pages have been crawled. Finishing.")
        return 'finished'

    pages_to_crawl = set(range(1, last_page + 1)) - set(crawled_pages)
    crawling_batch_size = min(random.randint(*CONF.pages_to_crawl_per_worker), len(pages_to_crawl))
    page_batch = list(pages_to_crawl)[0:crawling_batch_size]
    logger.info(f"Selected batch of {len(page_batch)} pages to crawl")

    response_data_file_path = f"{dir_name}/{CONF.response_data_file_name}"
    successfully_crawled_pages = []

    for page in page_batch:
        page_str = f"/{page}" if page != 1 else ""
        url = f"{base_url}{page_str}"
        logger.info(f"Crawling page {page}: {url}")

        html_response = await make_zyte_request(client, url, response_data_file_path)
        logger.info(f"Received response for page {page}")

        listing_urls, suspicious_count = extract_listing_hrefs(html_response, base_url)
        logger.info(f"Extracted {len(listing_urls)} listing URLs from page {page}")

        if suspicious_count > 0:
            filename = f"{dir_name}/_{page}_{CONF.irregular_pages_file}"
            logger.warning(f"Found {suspicious_count} suspicious listings on page {page}")
            irregular_pages = await use_json(filename)
            irregular_pages[url] = listing_urls
            await use_json(filename, keys=None, value=irregular_pages, recreate_file=True)
            logger.info(f"Updated irregular pages file: {filename}")  # TODO add "ignore pages" to prog file
        else:
            init_response_data = {url: '' for url in listing_urls}
            await use_json(f"{dir_name}/{page}_{CONF.response_data_file_name}",
                           value=init_response_data, recreate_file=True)

        successfully_crawled_pages.append(page)
        logger.info(f"Successfully crawled page {page}")

    logger.info(f"Finished crawling batch. {len(successfully_crawled_pages)} pages crawled successfully")

    # save crawling progress
    await update_crawling_prog(dir_name, key=[base_url, 'crawled_pages'], value=successfully_crawled_pages,
                               extend_list_value=True)
    logger.info("Updated crawling progress")


async def crawl_and_process(semaphore, client, base_url, dir_name, worker_id):
    logger.info(f"Worker {worker_id} started for {base_url}")
    async with semaphore:
        while True:
            logger.info(f"Worker {worker_id} starting new iteration")

            # Crawl page batch
            status = await crawl_page_batch(client, base_url, dir_name)
            logger.info(f"Worker {worker_id} completed crawl_page_batch with status: {status}")
            #
            if status == "finished":
                logger.info(f"Worker {worker_id} finished crawling all pages for {base_url}")
                break

            # Scrape URLs of page
            await scrape_urls_of_page(client, base_url, dir_name, worker_id)

            # Sleep before next iteration
            delay = random.uniform(*CONF.crawling_delay)
            logger.info(f"Worker {worker_id} sleeping for {delay:.2f} seconds")
            await asyncio.sleep(delay)

    # logger.info(f"Worker {worker_id} completed all tasks for {base_url}")


async def main():
    semaphore = asyncio.Semaphore(CONF.max_concurrent_requests)
    connector = aiohttp.TCPConnector(limit_per_host=CONF.max_concurrent_requests)
    async with aiohttp.ClientSession(connector=connector) as client:
        tasks = []
        for worker_id, (dir_name, url) in enumerate(CONF.base_url_info.items(), start=0):
            os.makedirs(dir_name, exist_ok=True)
            await initialize_base_url_if_new(client, dir_name, url)
            task = asyncio.create_task(
                crawl_and_process(semaphore, client, url, dir_name, worker_id),
                name=f"Worker-{worker_id}"
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Task failed with exception: {result}")
                
        save_to_db(list(CONF.base_url_info.keys()))
        
        logger.info("FINISHED SUCCESS----")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Critical error occurred: {str(e)}", exc_info=True)
