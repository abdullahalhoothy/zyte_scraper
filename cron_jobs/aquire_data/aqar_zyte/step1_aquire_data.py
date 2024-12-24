import asyncio
import json
import logging
import os
import random
from base64 import b64decode, b64encode
from contextlib import asynccontextmanager
from typing import Any, List, Union
import sys
import time

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
)
from cron_jobs.aquire_data.aqar_zyte.load_config import CONF
from cron_jobs.aquire_data.aqar_zyte.utils.aqar_html_parsers import (
    get_last_page,
    extract_listing_hrefs,
    extract_all_data,
)

import aiofiles
import aiohttp


class RequestError(Exception):
    pass


def setup_logger():
    # Get the directory of the current module
    module_dir = os.path.dirname(os.path.abspath(__file__))

    logger_cls = logging.getLogger(__name__)
    logger_cls.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
    )

    # Console handler setup
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger_cls.addHandler(console_handler)

    # File handler setup with full path
    log_file_path = os.path.join(module_dir, "crawler.log")
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger_cls.addHandler(file_handler)

    return logger_cls


logger = setup_logger()


# Load configuration from a JSON file
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


async def use_json(
    filename: str,
    keys: Union[str, List[str]] = None,
    value: Any = None,
    extend_list_value: bool = False,
    recreate_file: bool = False,
) -> Any:
    async with file_lock_manager.acquire(filename):
        if recreate_file:
            if os.path.exists(filename):
                os.remove(filename)
            data = {}
        else:
            try:
                async with aiofiles.open(filename, mode="r") as f:
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

                async with aiofiles.open(filename, mode="w") as f:
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
                async with aiofiles.open(filename, mode="w") as f:
                    json_string = json.dumps(data, indent=2)
                    await f.write(json_string)
            # Return all data if no key is specified and no value to write
            return data


async def load_directory_json_files(directory: str) -> dict:
    """Load all JSON files from a directory into a dictionary."""
    files_data = {}
    try:
        for filename in os.listdir(directory):
            if filename.endswith("_response_data.json"):
                file_path = os.path.join(directory, filename)
                try:
                    async with aiofiles.open(file_path, mode="r") as f:
                        content = await f.read()
                        if content:  # Check if file is not empty
                            files_data[filename] = json.loads(content)
                        else:
                            files_data[filename] = {}
                except (json.JSONDecodeError, FileNotFoundError):
                    files_data[filename] = {}
    except Exception as e:
        logger.error(f"Error loading directory {directory}: {str(e)}")
        return {}

    return files_data


def get_elapsed_time(start_time):
    """Calculate elapsed time and return formatted string"""
    elapsed = time.time() - start_time
    if elapsed < 60:
        return f"{elapsed:.2f} seconds"
    elif elapsed < 3600:
        minutes = elapsed // 60
        seconds = elapsed % 60
        return f"{int(minutes)} minutes {int(seconds)} seconds"
    else:
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        return f"{int(hours)} hours {int(minutes)} minutes {int(seconds)} seconds"


async def make_zyte_request(
    client,
    url,
    response_data_file_path,
    worker_id,
    city,
    category,
    max_retries=3,
    parsing_func=None,
):
    for attempt in range(max_retries):
        try:
            # Try to get cached response
            cached_response = await use_json(response_data_file_path, keys=url)
            if cached_response and cached_response != {} and cached_response != "":
                logger.info(
                    f"Worker-{worker_id}-{city}-{category} Using cached response for {url}"
                )
                try:
                    return b64decode(cached_response).decode("utf-8")
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
                    "geolocation": "DE",
                    "actions": [],
                    # "echoData": url,
                    # "sessionContext": [], # don't know how to use it , but helps avoid bans
                    # "sessionContextParameters": "", # goes with the above
                },
                "headers": headers,
                "timeout": 30,  # Set a timeout for the request
            }
            logger.info(
                f"Worker-{worker_id}-{city}-{category} attempt number ({attempt}) to make request to {url}"
            )
            async with client.post(**request_params) as response:
                response_json = await response.json()
                status_code = response.status

                if status_code == 200:
                    http_response_body = response_json.get("httpResponseBody", "")
                    return_data = b64decode(http_response_body)
                    save_data = http_response_body
                    if parsing_func is not None:
                        return_data = parsing_func(return_data)
                        save_data = return_data
                    # echodata = response_json.get("echoData", "")
                    await use_json(response_data_file_path, keys=url, value=save_data)
                    logger.info(
                        f"Worker-{worker_id}-{city}-{category} Successfully retrieved and saved response for {url}"
                    )
                    return return_data

                elif status_code in [400, 401, 403, 422, 451, 500, 521]:
                    error_detail = response_json.get("detail", "No detail provided")
                    raise RequestError(f"Error {status_code}: {error_detail}")
                elif status_code in [429, 503, 520]:
                    raise RequestError(f"Error {status_code}: {response_json}")
                else:
                    raise RequestError(f"Unexpected status code: {status_code}")

        except aiohttp.ClientError as e:
            logger.error(
                f"Worker-{worker_id}-{city}-{category} Network error occurred while requesting {url}: {str(e)}"
            )
        except json.JSONDecodeError:
            logger.error(
                f"Worker-{worker_id}-{city}-{category} Failed to decode JSON response for {url}"
            )
        except RequestError as e:
            if "429" in str(e) or "503" in str(e) or "520" in str(e):
                retry_after = int(int(response.headers.get("Retry-After", 2)) / 6)
                logger.error(
                    f"Worker-{worker_id}-{city}-{category} {str(e)} (attempt {attempt + 1}/{max_retries}) retrying after {retry_after}"
                )
                await asyncio.sleep(max(retry_after, 2**attempt))
                continue
        except Exception as e:
            logger.error(
                f"Worker-{worker_id}-{city}-{category} Unexpected error occurred while requesting {url}: {str(e)}"
            )

            # Exponential backoff
        delay = 2**attempt
        logger.warning(
            f"Worker-{worker_id}-{city}-{category} Retrying request for {url} (attempt {attempt + 1} of {max_retries}) after {delay} seconds"
        )
        await asyncio.sleep(delay)

    logger.error(
        f"Worker-{worker_id}-{city}-{category} Failed to get valid response for {url} after {max_retries} attempts"
    )
    save_data = f"Error {status_code}: {response_json}"
    await use_json(response_data_file_path, keys=url, value=save_data)
    return save_data


async def fetch_crawling_prog(dir_name, base_url):
    crawling_prog_file = f"{dir_name}/{CONF.crawling_progress_file_name}"
    progress_tracker = await use_json(crawling_prog_file)
    crawled_pages = None
    pages_to_process = None
    last_page = None
    if base_url in progress_tracker:
        crawled_pages = list(set(progress_tracker[base_url]["crawled_pages"]))
        scraped_all_listings_from_pages = progress_tracker[base_url].get(
            "scraped_all_listings_from_pages", []
        )
        scraped_all_listings_from_pages = list(set(scraped_all_listings_from_pages))
        pages_to_process = [
            page
            for page in crawled_pages
            if page not in scraped_all_listings_from_pages
        ]
        last_page = progress_tracker[base_url]["last_page"]
        pages_to_process.sort()

    return progress_tracker, crawled_pages, pages_to_process, last_page


async def update_crawling_prog(dir_name, key, value, **kwargs):
    await use_json(
        f"{dir_name}/{CONF.crawling_progress_file_name}",
        keys=key,
        value=value,
        **kwargs,
    )


async def initialize_and_validate_new_run(
    client, dir_name, base_url, worker_id, city, category
):
    url = f"{base_url}/{CONF.last_page_check_number}"
    response_data_file_path = f"{dir_name}/{CONF.response_data_file_name}"
    response_data = await make_zyte_request(
        client, url, response_data_file_path, worker_id, city, category
    )
    crawling_prog, _, _, _ = await fetch_crawling_prog(dir_name, base_url)

    if base_url not in crawling_prog:
        last_page = get_last_page(response_data)
        if last_page > 50:
            last_page = 50
        crawling_prog[base_url] = {
            "last_page": last_page,
            "crawled_pages": [],
            "scraped_all_listings_from_pages": [],
        }
    else:
        # Load all JSON files from directory at once
        all_response_files = await load_directory_json_files(dir_name)

        # Validate existing crawled pages
        valid_crawled_pages = []
        valid_scraped_pages = []

        for page in crawling_prog[base_url]["crawled_pages"]:
            page_response_filename = f"{page}_response_data.json"
            page_data = all_response_files.get(page_response_filename, {})

            if page_data and len(page_data) > 0:
                valid_crawled_pages.append(page)
            else:
                logger.warning(
                    f"Worker-{worker_id}-{city}-{category} Invalid or empty response file for page {page}"
                )

        crawling_prog[base_url]["crawled_pages"] = valid_crawled_pages

        # Validate scraped pages
        try:
            for page in crawling_prog[base_url]["scraped_all_listings_from_pages"]:
                page_response_filename = f"{page}_response_data.json"
                page_data = all_response_files.get(page_response_filename, {})

                if page_data and len(page_data) > 0:
                    valid_scraped_pages.append(page)
                else:
                    logger.warning(
                        f"Worker-{worker_id}-{city}-{category} Invalid or empty response file for scraped page {page}"
                    )
            crawling_prog[base_url][
                "scraped_all_listings_from_pages"
            ] = valid_scraped_pages

        except KeyError:
            pass

        logger.info(
            f"Worker-{worker_id}-{city}-{category} Validated pages - Crawled: {len(valid_crawled_pages)}, Scraped: {len(valid_scraped_pages)}"
        )

    # Save updated progress
    await update_crawling_prog(dir_name, key=base_url, value=crawling_prog[base_url])


async def check_page_fully_scraped(
    selected_page, dir_name, base_url, worker_id, city, category
):
    page_response_file = f"{dir_name}/{selected_page}_response_data.json"
    page_response_data = await use_json(page_response_file)
    remaining_urls = [url for url, value in page_response_data.items() if value == ""]
    if page_response_data == {}:
        remaining_urls = [20]  # TODO temp fix
    if len(remaining_urls) == 0:
        await update_crawling_prog(
            dir_name,
            key=[base_url, "scraped_all_listings_from_pages"],
            value=[selected_page],
            extend_list_value=True,
        )
        logger.info(
            f"Worker-{worker_id}-{city}-{category} page={selected_page} fully scrapped"
        )


async def scrape_listings(client, page_number, dir_name, worker_id, city, category):
    start_time = time.time()
    page_response_file = f"{dir_name}/{page_number}_response_data.json"
    page_response_data = await use_json(page_response_file)
    all_listing_urls = [url for url, value in page_response_data.items() if value == ""]

    logger.info(
        f"Worker-{worker_id}-{city}-{category} Found {len(all_listing_urls)} available urls to scrape in page={page_number}"
    )
    sample_size = min(
        len(all_listing_urls), random.randint(*CONF.pages_to_scrape_per_worker)
    )
    random_sample = random.sample(all_listing_urls, sample_size)


    for idx, url in enumerate(random_sample, 0):
        url_start_time = time.time()
        logger.info(
            f"Worker-{worker_id}-{city}-{category} Beginning to scrape {len(random_sample)} urls of {len(all_listing_urls)} available urls"
        )
        logger.info(
            f"Worker-{worker_id}-{city}-{category} Processing listing {idx}/{len(random_sample)} from page {page_number} "
            f"in {city} for category {category}"
        )

        response_data = await make_zyte_request(
            client,
            url,
            page_response_file,
            worker_id,
            city,
            category,
            parsing_func=extract_all_data,
        )
        url_elapsed = get_elapsed_time(url_start_time)

        if response_data == "":
            logger.error(
                f"Worker-{worker_id}-{city}-{category} Failed to process listing {idx}/{len(random_sample)} from page {page_number} "
                f"Moving to next listing. (took {url_elapsed})"
            )

        delay = random.uniform(*CONF.scraping_delay)
        logger.info(
            f"Worker-{worker_id}-{city}-{category} Sleeping for {delay:.2f} seconds before next listing"
        )
        await asyncio.sleep(delay)

    total_elapsed = get_elapsed_time(start_time)
    logger.info(
        f"Worker-{worker_id}-{city}-{category} Completed processing {len(random_sample)} listings from page {page_number} "
        f"in {city} for category {category} (total time: {total_elapsed})"
    )


async def scrape_urls_of_page(
    client,
    base_url,
    dir_name,
    worker_id,
    city,
    category,
):
    scrape_start = time.time()
    logger.info(
        f"Worker-{worker_id}-{city}-{category} fetching crawled pages pending scraping"
    )
    _, _, crawled_pages_pending_scraping, _ = await fetch_crawling_prog(
        dir_name, base_url
    )
    city, category = dir_name.split("/")[-1].split("_", 1)

    logger.info(
        f"Worker-{worker_id}-{city}-{category} crawled pages pending scraping ={crawled_pages_pending_scraping}"
    )
    if not crawled_pages_pending_scraping:
        logger.warning(f"Worker-{worker_id}-{city}-{category}  No listings to scrap ")
        return "finished"

    # Use modulo to wrap around the worker_id to available pages
    page_index = worker_id % len(crawled_pages_pending_scraping)

    logger.info(
        f"Worker-{worker_id}-{city}-{category} scraping listing of page {crawled_pages_pending_scraping[page_index]} of {len(crawled_pages_pending_scraping)} available pages)"
    )

    await scrape_listings(
        client,
        crawled_pages_pending_scraping[page_index],
        dir_name,
        worker_id,
        city,
        category,
    )
    await check_page_fully_scraped(
        crawled_pages_pending_scraping[page_index],
        dir_name,
        base_url,
        worker_id,
        city,
        category,
    )


async def crawl_page_batch(
    client, base_url, dir_name, worker_id, city, category, start_time
):
    status = "Not Finished"

    _, crawled_pages, _, last_page = await fetch_crawling_prog(dir_name, base_url)
    logger.info(
        f"Worker-{worker_id}-{city}-{category} Fetched crawling progress: {len(crawled_pages)} pages crawled, last page is {last_page}"
    )

    if len(crawled_pages) >= last_page:
        logger.info(
            f"Worker-{worker_id}-{city}-{category} All pages have been crawled. Finishing."
        )
        status = "finished"
        total_elapsed = get_elapsed_time(start_time)
        logger.info(
            f"Worker-{worker_id}-{city}-{category} finished crawling all pages, Total time: {total_elapsed}"
        )
        return status

    pages_to_crawl = set(range(1, last_page + 1)) - set(crawled_pages)
    crawling_batch_size = min(
        random.randint(*CONF.pages_to_crawl_per_worker), len(pages_to_crawl)
    )
    page_batch = list(pages_to_crawl)[0:crawling_batch_size]
    logger.info(
        f"Worker-{worker_id}-{city}-{category} Selected batch of size {len(page_batch)} pages to crawl"
    )

    response_data_file_path = f"{dir_name}/{CONF.response_data_file_name}"
    successfully_crawled_pages = []

    for page in page_batch:
        page_str = f"/{page}" if page != 1 else ""
        url = f"{base_url}{page_str}"
        batch_start = time.time()
        logger.info(f"Worker-{worker_id}-{city}-{category} beginning page batch crawl")
        logger.info(f"Worker-{worker_id}-{city}-{category} Crawling page {page}: {url}")

        html_response = await make_zyte_request(
            client, url, response_data_file_path, worker_id, city, category
        )
        logger.info(
            f"Worker-{worker_id}-{city}-{category} Received response for page {page}"
        )

        listing_urls, suspicious_count = extract_listing_hrefs(html_response, base_url)
        logger.info(
            f"Worker-{worker_id}-{city}-{category} Extracted {len(listing_urls)} listing URLs from page {page}"
        )

        if suspicious_count > 0:
            filename = f"{dir_name}/_{page}_{CONF.irregular_pages_file}"
            logger.warning(
                f"Worker-{worker_id}-{city}-{category} Found {suspicious_count} suspicious listings on page {page}"
            )
            irregular_pages = await use_json(filename)
            irregular_pages[url] = listing_urls
            await use_json(
                filename, keys=None, value=irregular_pages, recreate_file=True
            )
            logger.info(
                f"Worker-{worker_id}-{city}-{category} Updated irregular pages file: {filename}"
            )  # TODO add "ignore pages" to prog file
        else:
            init_response_data = {url: "" for url in listing_urls}
            await use_json(
                f"{dir_name}/{page}_{CONF.response_data_file_name}",
                value=init_response_data,
                recreate_file=True,
            )

        successfully_crawled_pages.append(page)
        logger.info(
            f"Worker-{worker_id}-{city}-{category} Successfully crawled page {page}"
        )

    logger.info(
        f"Worker-{worker_id}-{city}-{category} Finished crawling batch. {len(successfully_crawled_pages)} pages crawled successfully"
    )

    # save crawling progress
    await update_crawling_prog(
        dir_name,
        key=[base_url, "crawled_pages"],
        value=successfully_crawled_pages,
        extend_list_value=True,
    )
    logger.info(f"Worker-{worker_id}-{city}-{category} Updated crawling progress")
    batch_elapsed = get_elapsed_time(batch_start)
    logger.info(
        f"Worker-{worker_id}-{city}-{category} completed page batch crawl. (took {batch_elapsed})"
    )


async def crawl_and_scrape(semaphore, client, base_url, dir_name, worker_id):
    start_time = time.time()
    try:
        for city_name, category_name in CONF.base_url_info.items():
            if category_name == base_url:
                city, category = city_name.split("_", 1)
                break
    except Exception as e:
        logger.error(
            f"Worker-{worker_id}-{city}-{category} Error parsing city and category from URL: {e}"
        )
        city = "unknown_city"
        category = "unknown_category"

    logger.info(f"Worker-{worker_id}-{city}-{category} started crawl and scrap")

    async with semaphore:
        while True:
            iteration_start_time = time.time()

            # Crawl page batch
            crawling_status = await crawl_page_batch(
                client,
                base_url,
                dir_name,
                worker_id,
                city,
                category,
                start_time,
            )

            # Scrape URLs of page
            scraping_status = await scrape_urls_of_page(
                client,
                base_url,
                dir_name,
                worker_id,
                city,
                category,
            )
            logger.info

            time_elapsed = get_elapsed_time(iteration_start_time)
            logger.info(
                f"Worker-{worker_id}-{city}-{category} finished crawl and scrap, took {time_elapsed}"
                f"crawl_status={crawling_status}, scraping_status={scraping_status}"
            )

            if crawling_status == "finished" and scraping_status == "finished":
                break
            # Sleep before next iteration
            delay = random.uniform(*CONF.crawling_delay)
            logger.info(
                f"Worker-{worker_id}-{city}-{category} sleeping for {delay:.2f} seconds "
            )
            await asyncio.sleep(delay)

    total_elapsed = get_elapsed_time(start_time)
    logger.info(
        f"Worker-{worker_id}-{city}-{category} completed all tasks Total time: {total_elapsed}"
    )


async def aquire_data():
    start_time = time.time()
    logger.info("Starting data acquisition process")
    semaphore = asyncio.Semaphore(CONF.max_concurrent_requests)
    connector = aiohttp.TCPConnector(
        limit_per_host=CONF.max_concurrent_requests, force_close=True
    )
    tasks = []
    worker_info = {}  # Store city/category info for each worker

    try:
        async with aiohttp.ClientSession(connector=connector) as client:
            # Initialize tasks for each worker
            for worker_id, (dir_name, url) in enumerate(
                CONF.base_url_info.items(), start=0
            ):
                try:
                    # Parse city and category from dir_name
                    city, category = dir_name.split("/")[-1].split("_", 1)
                    worker_info[worker_id] = {"city": city, "category": category}

                    logger.info(
                        f"Worker-{worker_id}-{city}-{category} Initializing Worker"
                    )

                    valid_dir_name = (
                        os.path.dirname(os.path.abspath(__file__)) + "/" + dir_name
                    )
                    os.makedirs(valid_dir_name, exist_ok=True)

                    # Initialize base URL
                    await initialize_and_validate_new_run(
                        client, valid_dir_name, url, worker_id, city, category
                    )

                    # Create task for worker
                    task = asyncio.create_task(
                        crawl_and_scrape(
                            semaphore, client, url, valid_dir_name, worker_id
                        ),
                        name=f"Worker-{worker_id}-{city}-{category}",
                    )
                    tasks.append(task)

                    logger.info(
                        f"Worker-{worker_id}-{city}-{category} Successfully initialized Worker"
                    )

                except Exception as e:
                    worker_details = worker_info.get(
                        worker_id, {"city": "unknown", "category": "unknown"}
                    )
                    logger.error(
                        f"Worker-{worker_id}-{city}-{category} Error initializing Worker: {str(e)}"
                    )
                    continue

            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            success_count = 0
            for i, result in enumerate(results):
                worker_details = worker_info.get(
                    i, {"city": "unknown", "category": "unknown"}
                )
                if isinstance(result, Exception):
                    logger.error(
                        f"Worker-{i} for {worker_details['city']} - {worker_details['category']} "
                        f"failed with exception: {result}"
                    )
                else:
                    success_count += 1
                    logger.info(
                        f"Worker-{i} for {worker_details['city']} - {worker_details['category']} "
                        f"completed successfully"
                    )

            logger.info(
                f"Completed {success_count} out of {len(tasks)} workers successfully. "
                f"Failed workers: {len(tasks) - success_count}"
            )

    except asyncio.CancelledError:
        logger.warning("Received cancellation signal - cleaning up all workers...")
        # Cancel all pending tasks
        for task in tasks:
            worker_id = int(task.get_name().split("-")[1])
            worker_details = worker_info.get(
                worker_id, {"city": "unknown", "category": "unknown"}
            )
            logger.info(
                f"Cancelling Worker-{worker_id} for "
                f"{worker_details['city']} - {worker_details['category']}"
            )
            if not task.done():
                task.cancel()
        # Wait for tasks to complete cancellation
        await asyncio.gather(*tasks, return_exceptions=True)
        raise

    except Exception as e:
        logger.error(f"Unexpected error in aquire_data: {str(e)}")
        raise

    finally:
        # Cleanup any remaining tasks
        for task in tasks:
            if not task.done():
                worker_id = int(task.get_name().split("-")[1])
                worker_details = worker_info.get(
                    worker_id, {"city": "unknown", "category": "unknown"}
                )
                logger.info(
                    f"Cleaning up Worker-{worker_id} for "
                    f"{worker_details['city']} - {worker_details['category']}"
                )
                task.cancel()

        # Wait for cancelled tasks to finish
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        # Ensure connector is closed
        if not connector.closed:
            await connector.close()

        total_elapsed = get_elapsed_time(start_time)
        logger.info(f"Total execution time: {total_elapsed}")

    if success_count == len(tasks):
        logger.info("FINISHED SUCCESS - All workers completed successfully")
    else:
        logger.warning(
            f"FINISHED WITH {len(tasks) - success_count} FAILED WORKERS - "
            f"Successfully completed: {success_count}/{len(tasks)}"
        )


asyncio.run(aquire_data())
