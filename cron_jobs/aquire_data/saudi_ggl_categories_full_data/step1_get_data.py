import asyncio
import aiohttp
import json
import os
from datetime import datetime
from time import sleep

# Define base URL as a constant to avoid repetition
BASE_URL = "http://localhost:7005/fastapi"

LOGIN_URL = f"{BASE_URL}/login"
FETCH_DATASET_URL = f"{BASE_URL}/fetch_dataset"

async def make_api_call(session, boolean_query, token, page_num, search_type, obtained_auth_token):

    headers = {
        "Authorization": f"Bearer {obtained_auth_token}"
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
            "search_type": search_type,
            "text_search": "",
            "zoom_level": 0,
            "radius": 30000,
        },
    }

    try:
        async with session.post(FETCH_DATASET_URL, json=request_body, headers=headers) as response:
            print(f"Fetching page {page_num}, token: {token}")
            response.raise_for_status()
            return await response.json()
    except Exception as e:
        print(f"Error on page {page_num}: {str(e)}")
        # Retry once
        try:
            async with session.post(
                FETCH_DATASET_URL, json=request_body, headers=headers
            ) as response:
                print(f"Retry page {page_num}, token: {token}")
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            print(f"Second attempt failed for page {page_num}: {str(e)}")
            return None


async def fetch_data(boolean_query: str, search_type: str, obtained_auth_token):
    all_responses = []
    tokens_to_process = await initial_call(boolean_query, search_type, obtained_auth_token, all_responses)

    sleep(15)  # Wait for the backend to register the new token

    # Process remaining tokens one at a time sequentially
    async with aiohttp.ClientSession() as session:
        page_num = len(all_responses) + 1
        
        while tokens_to_process:
            # Take one token at a time
            current_token = tokens_to_process.pop(0)
            
            # Make a single API call
            response = await make_api_call(session, boolean_query, current_token, page_num, 
                                         search_type, obtained_auth_token)
            
            # Process the response
            if response:
                all_responses.append(response)
                next_token = response["data"]["next_page_token"]
                if next_token:
                    tokens_to_process.append(next_token)
                    
            page_num += 1

    return all_responses

async def initial_call(boolean_query, search_type, obtained_auth_token, all_responses):
    tokens_to_process = []

    # First call - must be done separately
    async with aiohttp.ClientSession() as session:
        first_response = await make_api_call(session, boolean_query, "", 1, search_type, obtained_auth_token)
        if first_response:
            all_responses.append(first_response)
            next_token = first_response["data"]["next_page_token"]
            if next_token:
                tokens_to_process.append(next_token)
    return tokens_to_process


async def login_and_get_token(username, password): # Removed 'session' parameter
    """
    Logs in to the API and retrieves an authentication token.
    Manages its own aiohttp.ClientSession.
    """
    request_body_payload = {
        "email": username,
        "password": password
    }
    full_request_body = {
        "message": "string",
        "request_info": {},
        "request_body": request_body_payload
    }

    # Create a new session specifically for this login attempt
    async with aiohttp.ClientSession() as session: # Session is created and managed here
        try:
            async with session.post(LOGIN_URL, json=full_request_body) as response:
                response.raise_for_status()
                login_data = await response.json()
                
                auth_token = login_data.get("data", {}).get("idToken")
                
                if not auth_token:
                    print("Error: idToken not found in login response.")
                    print(f"Login response data: {login_data}")
                    return None
                return auth_token
        except aiohttp.ClientResponseError as e:
            print(f"Login HTTP error: {e.status} {e.message}")
            try:
                error_content = await e.text()
                print(f"Login error response body: {error_content}")
            except Exception:
                pass
            return None
        except Exception as e:
            print(f"Login failed due to an unexpected error: {str(e)}")
            return None

async def main():
    api_email = "u_je_u2008@live.com"
    api_password = "12351235"

    print("Logging in to get auth token...")
    obtained_auth_token = await login_and_get_token(api_email, api_password)

    if not obtained_auth_token:
        print("Login failed or token not retrieved. Exiting application.")
        return # Exit if login is unsuccessful

    # wait for backend to register new token before using it
    print("Waiting for backend to register new token...")
    sleep(2)    

    print("Starting data collection...")
    # boolean ="""Museum"""
    # tryp ="category_search"
    # boolean = "@auto parts@ "
    # type = "keyword_search"
    # boolean ="""(auto_parts_store OR @auto parts@ OR @car repair@ OR @car parts@ OR @car repair parts@ OR @قطع غيار السيارات@) AND NOT @بنشر@"""
    # type = "category_search + keyword_search"
    
    # boolean ="""@متحف@ OR @Museum@"""
    # responses = await fetch_data(boolean, "keyword_search", obtained_auth_token)

    # boolean ="""university"""
    # responses = await fetch_data(boolean, "category_search", obtained_auth_token)

    boolean ="""plumber"""
    responses = await fetch_data(boolean, "category_search", obtained_auth_token)

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    boolean= boolean.replace(" ","")
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
