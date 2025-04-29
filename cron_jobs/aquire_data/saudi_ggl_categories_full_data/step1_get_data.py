import asyncio
import aiohttp
import json
import os
from datetime import datetime


async def make_api_call(session, boolean_query, token, page_num):
    url = "http://localhost:7000/fastapi/fetch_dataset"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImEwODA2N2Q4M2YwY2Y5YzcxNjQyNjUwYzUyMWQ0ZWZhNWI2YTNlMDkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoidV9qZV91IiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2Rldi1zLWxvY2F0b3IiLCJhdWQiOiJkZXYtcy1sb2NhdG9yIiwiYXV0aF90aW1lIjoxNzQwNDI1MjY0LCJ1c2VyX2lkIjoiSm5hR0RDS29Tb1d0ajZOV0VWVzhNRE1CQ2lBMiIsInN1YiI6IkpuYUdEQ0tvU29XdGo2TldFVlc4TURNQkNpQTIiLCJpYXQiOjE3NDE5MjI1OTAsImV4cCI6MTc0MTkyNjE5MCwiZW1haWwiOiJ1X2plX3UyMDA4QGxpdmUuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsidV9qZV91MjAwOEBsaXZlLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.Xj2BCUBkwoabwwJY-r2KDq2pLQ2NyMGCdW-8qDDlhZogIn-x-SPNTssLOV4MlxSsXOdLJWYElvfyuPVsyDe-wsvWPlmxPDvLGcuAt7AePapMjjFYn8-zpTUajUfzEEDNBG4aQ1JTdHusYSx_zfSBW9TziYqbnilxoZlbYRVQ44aCW-Xpb_fbc3SEdG4iT90M1d3NJkmRASwFeSsoTHPgyntktKfVywFWqxClh89ZljilY_t0ppJ4U5bfXzHPhRgUBLwyStX_G8ljByPMeGgdv1YHlfgzJ3cQNlmZ5Ia9NZdBGa4D8FHhAAwtQfUdXgq4i6Kvqd09x8SD8spZtbx4zQ"
    }

    request_body = {
        "message": "string",
        "request_info": {},
        "request_body": {
            "user_id": "JnaGDCKoSoWtj6NWEVW8MDMBCiA2",
            "prdcer_lyr_id": "",
            "city_name": "Riyadh",
            "country_name": "Saudi Arabia",
            "boolean_query": boolean_query,
            "action": "full data",
            "page_token": token,
            "search_type": "default",
            "text_search": "",
            "zoom_level": 0,
            "radius": 30000,
        },
    }

    try:
        async with session.post(url, json=request_body, headers=headers) as response:
            print(f"Fetching page {page_num}, token: {token}")
            response.raise_for_status()
            return await response.json()
    except Exception as e:
        print(f"Error on page {page_num}: {str(e)}")
        # Retry once
        try:
            async with session.post(
                url, json=request_body, headers=headers
            ) as response:
                print(f"Retry page {page_num}, token: {token}")
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            print(f"Second attempt failed for page {page_num}: {str(e)}")
            return None


async def fetch_data(boolean_query: str):
    all_responses = []
    tokens_to_process = []

    # First call - must be done separately
    async with aiohttp.ClientSession() as session:
        first_response = await make_api_call(session, boolean_query, "", 1)
        if first_response:
            all_responses.append(first_response)
            next_token = first_response["data"]["next_page_token"]
            if next_token:
                tokens_to_process.append(next_token)

    # Process remaining tokens in batches of 10
    while tokens_to_process:
        async with aiohttp.ClientSession() as session:
            # Take up to 10 tokens at a time
            current_batch = tokens_to_process[:10]
            tokens_to_process = tokens_to_process[10:]

            # Create tasks for concurrent execution
            tasks = []
            for i, token in enumerate(current_batch, len(all_responses) + 1):
                task = make_api_call(session, boolean_query, token, i)
                tasks.append(task)

            # Wait for all tasks in the batch to complete
            batch_responses = await asyncio.gather(*tasks)

            # Process responses and collect new tokens
            for response in batch_responses:
                if response:
                    all_responses.append(response)
                    next_token = response["data"]["next_page_token"]
                    if next_token:
                        tokens_to_process.append(next_token)

    return all_responses


async def main():
    print("Starting data collection...")
    boolean="supermarket OR asian_grocery_store OR convenience_store OR food_store OR grocery_store OR market"
    responses = await fetch_data(boolean)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    boolean=boolean.replace(" ","")
    filename = f"saudi_{boolean}_{timestamp}.json"
    save_path = r"G:\My Drive\Personal\Work\offline\Jupyter\Git\zyte_scraper\cron_jobs\aquire_data\saudi_ggl_categories_full_data"
    full_path = os.path.join(save_path, filename)

    os.makedirs(save_path, exist_ok=True)

    if responses:
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(responses, f, ensure_ascii=False, indent=2)

    print(f"\nData saved to: {full_path}")
    print(f"Total pages collected: {len(responses)}")


# Run the async program
if __name__ == "__main__":
    asyncio.run(main())
