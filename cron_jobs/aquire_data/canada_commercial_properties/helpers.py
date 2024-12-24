import random
import httpx
import tenacity
from bs4 import BeautifulSoup

BASE_URL = 'https://www.centris.ca'

@tenacity.retry(
    retry=tenacity.retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
    stop=tenacity.stop_after_attempt(3),
    before_sleep=lambda retry_state: print(f"Request failed (get_inscriptions), retrying in {retry_state.next_action.sleep} seconds... (Attempt {retry_state.attempt_number}/3)")
)
async def get_inscriptions(client, start_position):
    response = await client.post(
        f'{BASE_URL}/Property/GetInscriptions',
        json={'startPosition': start_position}
    )
    response.raise_for_status()
    return response.json()

@tenacity.retry(
    retry=tenacity.retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
    stop=tenacity.stop_after_attempt(3),
    before_sleep=lambda retry_state: print(f"Request failed (establish_session), retrying in {retry_state.next_action.sleep} seconds... (Attempt {retry_state.attempt_number}/3)")
)
async def establish_session(client):
    uc = random.randint(1, 100)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'origin': BASE_URL,
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    client.headers.update(headers)
    response = await client.get(f'{BASE_URL}/en/commercial-properties~for-rent?view=Summary&uc={uc}')
    response.raise_for_status()

    client.headers.update({
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/json; charset=UTF-8',
        'x-centris-uc': str(uc),
        'x-requested-with': 'XMLHttpRequest',
    })

async def get_total_property_count(client):
    response = await get_inscriptions(client, 0)
            
    if not response or not response.get('d'):
        print("Failed to get initial response")
        return

    result = response['d'].get('Result', {})
    return result.get('count', 0)


async def get_property_data(client, demographic_endpoint_client, html_content):
    property_data = parse_property_data(html_content)

    if property_data.get('city_id') is not None:
        socio_demographic_data = await demographic_endpoint_client(city_id=property_data.get('city_id'))
        if socio_demographic_data is None:
            raise Exception("Unable to get Socio Demographic Data")
        socio_demographic_data = parse_socio_demographic_data(socio_demographic_data)
    else:
        socio_demographic_data = {}


    transport_scores = await get_location_scores(client, property_data.get('latitude'), property_data.get('longitude'))
    if transport_scores is None:
        raise Exception("Unable to get Transport Scores")
    
    property_data['transport_scores'] = transport_scores
    property_data['socio_demographic_data'] = socio_demographic_data
    return property_data
    

def parse_property_data(html_content):
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, "html.parser")

    # 0. URL
    url_element = soup.find("input", id="calculatorLink")
    url = url_element.get("value") if url_element else None
    if url:
        url = url.split("?")[0]
        url = f"{BASE_URL}{url}"

    # 1. Address
    page_title_element = soup.find("h1", itemprop="category")
    page_title = page_title_element.get_text(strip=True) if page_title_element else None

    address_element = soup.find("h2", itemprop="address")
    address = address_element.get_text(strip=True) if address_element else None

    if page_title and address:
        address = f"{page_title}: {address}"

    # 2. Price
    price_container = soup.find("div", class_="price-container")
    price_element = price_container.find_all("span", class_="text-nowrap")[1]
    price = price_element.get_text(strip=True) if price_element else None

    # 3. Use of Property
    use_of_property_element = soup.find("div", class_="carac-title", string="Use of property")
    if use_of_property_element:
        use_of_property = use_of_property_element.find_next_sibling("div", class_="carac-value").get_text(strip=True)
    else:
        use_of_property = None

    # 4. Available commercial area
    commercial_area_element = soup.find(
        "div", class_="carac-title", string="Available commercial area"
    )
    if commercial_area_element:
        commercial_area = commercial_area_element.find_next_sibling(
            "div", class_="carac-value"
        ).get_text(strip=True)
    else:
        commercial_area = None

    # 5. Number of units
    units_element = soup.find("div", class_="carac-title", string="Number of units")
    if units_element:
        units = units_element.find_next_sibling("div", class_="carac-value").get_text(
            strip=True
        )
    else:
        units = None

    # 6. Type of Business
    type_of_business_element = soup.find("div", class_="carac-title", string="Type of business")
    
    if type_of_business_element:
        type_of_business = type_of_business_element.find_next_sibling("div", class_="carac-value").get_text(strip=True)
    else:
        type_of_business = None


    # 7. Walk Score
    walk_score_element = soup.find("div", class_="walkscore")
    if walk_score_element:
        walk_score = walk_score_element.find("span").get_text(strip=True)
    else:
        walk_score = None

    # 8. Description
    description_element = soup.find("div", itemprop="description")
    description = (
        description_element.get_text(strip=True) if description_element else None
    )

    # 9. Geo Location
    latitude_element = soup.find("span", id="PropertyLat")
    longitude_element = soup.find("span", id="PropertyLng")
    if latitude_element and longitude_element:
        latitude = latitude_element.get_text(strip=True)
        longitude = longitude_element.get_text(strip=True)
    else:
        latitude = None
        longitude = None

    # 10. Region Stats Summary
    region_stats_summary = None
    region_stats_div = soup.find("div", class_="region-stats")
    if region_stats_div:
        info_div = region_stats_div.find("div", id="info")
        if info_div:
            stats = []
            for table in info_div.find_all("table"):
                for row in table.find_all("tr"):
                    columns = row.find_all("td")
                    if len(columns) == 2:
                        label = columns[0].get_text(strip=True)
                        value = columns[1].get_text(strip=True)
                        stats.append(f"{label}: {value}")
            
            region_stats_summary = " - ".join(stats)
            region_stats_summary = region_stats_summary.replace("hab/km2", " hab/km²")

    # 11. City ID
    city_id_element = soup.find("input", id="cityId")
    city_id = city_id_element.get("value") if city_id_element else None

    # 12. City Name
    city_name_element = soup.find("input", id="cityName")
    city_name = city_name_element.get("value") if city_name_element else None

    return {
        "url": url,
        "address": address,
        "price": price,
        "use_of_property": use_of_property,
        "available_commercial_area": commercial_area,
        "number_of_units": units,
        "type_of_business": type_of_business,
        "walk_score": walk_score,
        "description": description,
        "latitude": latitude,
        "longitude": longitude,
        "region_stats_summary": region_stats_summary,
        "city_id": city_id,
        "city_name": city_name,
    }

def demographic_endpoint_closure_client():
    # Initialize shared client state only for demographic endpoint within the closure
    # Please avoid modifying or using these cookies and headers.
    cookies = {
        'AnonymousId': 'a2a67422d10d49569a6da98276493d94',
        'll-search-selection': '',
        '.AspNetCore.Session': 'CfDJ8IB3rL%2B2cctNufqZUezgpUFhP3ANOVYbOJhgFcTX3y0bg5iCdZo5iPeFIN9oghMDvotr5bhKKab4xvLbVH%2FTUBDTu2vPM%2BS%2BaxTjtLfs53SQZbb6YFXDwpgHcbsPlNhvywRZNL8YGfwJAFa0cvclM5OcZpeM0WMJ%2BQ3dxWQqmch2',
        'ARRAffinity': 'bc8e171b7c002d3bb23de8e3244cd18e70004f34dd2c93bbe3345e8d9a795961',
        'ARRAffinitySameSite': 'bc8e171b7c002d3bb23de8e3244cd18e70004f34dd2c93bbe3345e8d9a795961',
    }

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json; charset=UTF-8',
        'origin': 'https://www.centris.ca',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'x-centris-uc': '0',
        'x-centris-uck': '3ebbf1e2-9102-49ec-bcd6-22d565611d24',
        'x-requested-with': 'XMLHttpRequest',
    }

    client = httpx.AsyncClient(
        headers=headers,
        cookies=cookies,
    )

    @tenacity.retry(
        retry=tenacity.retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
        wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
        stop=tenacity.stop_after_attempt(3),
        before_sleep=lambda retry_state: print(f"Request failed (get_socio_demographic_data), retrying in {retry_state.next_action.sleep} seconds... (Attempt {retry_state.attempt_number}/3)")
    )
    async def get_socio_demographic_data(city_id):
        nonlocal client  
        response = await client.post(
            f'{BASE_URL}/api/statistics/GetDonneesSocioDemographic',
            json={
                'munId': city_id,
                'regionId': ''
            }
        )
        response.raise_for_status()
        return response.json()
    
    return get_socio_demographic_data


def parse_socio_demographic_data(data):
    predefined_keys = {
        'Population By Age Group': 'age',
        'Household Income': 'incomes',
        'Household Size': 'household',
        'Family Types': 'family',
        'Housing Tenure': 'occupation',
        'Construction Date': 'construction',
        'Housing Types': 'housing',
        'Education': 'schooling',
        'Immigration': 'immigration',
        'Languages Spoken': 'language'
    }

    result_dict = {}

    if not data.get('Succeeded') or 'Result' not in data:
        return result_dict

    for entry in data['Result']:
        title = entry.get('Title', 'Unknown')
        key = predefined_keys.get(title, title)
        slices = entry.get('Slices', [])
        average = entry.get('Average', '')

        slices_str = ' - '.join(f"{slice['Label']}: {slice['Value']}%" for slice in slices)

        results = [f"Details: {slices_str}"]
        average_cleaned = average.replace('\n', ' ') if average else ''
        if average_cleaned:
            results.append(f"Average: {average_cleaned}")

        result_dict[key] = '; '.join(results)

    return result_dict


@tenacity.retry(
    retry=tenacity.retry_if_exception_type((httpx.HTTPStatusError, httpx.RequestError)),
    wait=tenacity.wait_exponential(multiplier=1, min=1, max=10),
    stop=tenacity.stop_after_attempt(3),
    before_sleep=lambda retry_state: print(f"Request failed (get_transport_scores), retrying in {retry_state.next_action.sleep} seconds... (Attempt {retry_state.attempt_number}/3)")
)
async def get_location_scores(client, lat, lng):
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Authorization': 'V3 lERfIZokEQL7BG2FbuKrX3xB328aF9po.c6b1aa0a-fb31-417c-95e1-5cf990e51871',
        'Referer': 'https://sdk.locallogic.co/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'x-ll-sdk-name': 'local-content',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }

    params = {
        'locale': 'en',
        'product': 'local-content',
        'environment': 'undefined',
        'lat': float(lat),
        'lng': float(lng),
        'include': 'transit_friendly,car_friendly,pedestrian_friendly,cycling_friendly,primary_schools,high_schools,daycares,groceries,restaurants,shopping,cafes,quiet,nightlife,vibrant,historic,parks,greenery',
        'geography_levels': '20,30',
        'location_scores_rounding': 'none',
        'language': 'en',
    }

    response = await client.get('https://api.locallogic.co/v3/scores', params=params, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    location_scores = data['data']['location']
    
    def format_score(score_obj, key):
        value = score_obj.get(key, {}).get('value')
        if value is None:
            return 0.0
        return f"{float(value) * 2:.2f}"
    
    return {
        'walking_transport_score': format_score(location_scores, 'pedestrian_friendly'),
        'transit_transport_score': format_score(location_scores, 'transit_friendly'),
        'cycling_transport_score': format_score(location_scores, 'cycling_friendly'),
        'driving_transport_score': format_score(location_scores, 'car_friendly'),
        'primary_schools_score': format_score(location_scores, 'primary_schools'),
        'high_schools_score': format_score(location_scores, 'high_schools'),
        'daycares_score': format_score(location_scores, 'daycares'),
        'groceries_score': format_score(location_scores, 'groceries'),
        'restaurants_score': format_score(location_scores, 'restaurants'),
        'shopping_score': format_score(location_scores, 'shopping'),
        'cafes_score': format_score(location_scores, 'cafes'),
        'quiet_score': format_score(location_scores, 'quiet'),
        'nightlife_score': format_score(location_scores, 'nightlife'),
        'vibrant_score': format_score(location_scores, 'vibrant'),
        'historic_score': format_score(location_scores, 'historic'),
        'parks_score': format_score(location_scores, 'parks'),
        'greenery_score': format_score(location_scores, 'greenery'),
    }
