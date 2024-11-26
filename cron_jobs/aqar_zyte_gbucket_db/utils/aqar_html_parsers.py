from urllib.parse import unquote, urlparse, urljoin
import json
import re
from bs4 import BeautifulSoup


def get_last_page(response_html):
    soup = BeautifulSoup(response_html, 'html.parser')
    # Look for a div that contains multiple numeric links and class containting pagination
    potential_pagination_divs = soup.find_all('div', class_=lambda x: x and 'pagination' in x.lower())

    for div in potential_pagination_divs:
        # Find all links with numeric content
        numeric_links = [a for a in div.find_all('a') if a.text.strip().isdigit()]
        if numeric_links:
            # Sort the links by their numeric value and get the highest
            last_page = max(int(a.text.strip()) for a in numeric_links)
            return last_page

    # If we couldn't find it that way, try a more general approach
    all_links = soup.find_all('a', href=True)
    page_numbers = []
    for link in all_links:
        # Look for links that end with a number
        match = re.search(r'/(\d+)/?$', link['href'])
        if match:
            page_numbers.append(int(match.group(1)))

    return max(page_numbers) if page_numbers else 1


def is_suspicious(link, full_url):
    # Check for suspicious patterns in the URL
    suspicious_words = ['trap', 'honey', 'pot', 'spider', 'crawler', 'bot']
    if any(word in unquote(full_url).lower() for word in suspicious_words):
        return True

    listing_card = link.find('div',
                             class_=lambda x: x and any(word in x for word in ['listingCard', 'content', 'Card']))
    if listing_card:
        style = listing_card.get('style', '').lower()
        classes = listing_card.get('class', [])

        if 'display: none' in style or 'visibility: hidden' in style:
            return True

        if any('hidden' in cls.lower() for cls in classes):
            return True

    return False


def extract_listing_hrefs(html_content, base_url, expected_count=20):
    parsed_url = urlparse(base_url)
    path = parsed_url.path
    path_parts = path.strip('/').split('/')

    if len(path_parts) >= 2:
        pattern = f"/{path_parts[0]}/{path_parts[1]}"
    else:
        pattern = f"/{path_parts[0]}"

    escaped_pattern = re.escape(pattern)

    soup = BeautifulSoup(html_content, 'html.parser')

    all_links = soup.find_all('a', href=re.compile(escaped_pattern))

    full_urls = []
    suspicious_count = 0

    for link in all_links:
        listing_card = link.find('div',
                                 class_=lambda x: x and any(word in x for word in ['listingCard', 'content', 'Card']))
        if listing_card:
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                if is_suspicious(link, full_url):
                    suspicious_count += 1
                    print(f"Suspicious URL detected: {full_url}")
                full_urls.append(full_url)

    if len(full_urls) != expected_count:
        suspicious_count += 1
        print(f"Warning: Expected {expected_count} URLs, but got {len(full_urls)}")

    return full_urls, suspicious_count


def extract_specs(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    specs_div = soup.find('div', class_=lambda x: x and 'specs' in x)
    specs = {}
    if specs_div:
        items = specs_div.find_all('div', class_=lambda x: x and 'item' in x)
        for item in items:
            key_elem = item.find('p')
            value_elem = item.find('p', class_=lambda x: x and ('brandText' in x or 'label' in x))
            if key_elem:
                key = key_elem.text.strip()
                if value_elem:
                    value = value_elem.text.strip()
                else:
                    # Check for availability icon
                    available_icon = item.find('img', alt='Available-colored')
                    value = 'متوفر' if available_icon else 'غير متوفر'
                specs[key] = value
    return specs


def extract_json_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    script = soup.find('script', id='__NEXT_DATA__')
    if script:
        try:
            return json.loads(script.string)
        except json.JSONDecodeError:
            print("Error decoding JSON data")
    return None



def extract_price(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    price_div = soup.find('div', class_=lambda x: x and 'financing' in x)
    if price_div:
        price_text = price_div.find('h2', class_=lambda x: x and 'price' in x)
        if price_text:
            # Extract numbers from the text
            price = re.search(r'\d{1,3}(?:,\d{3})*', price_text.text)
            if price:
                return price.group().replace(',', '')  # Remove commas
    return None


def extract_all_data(html_content):
    price = extract_price(html_content)
    specs = extract_specs(html_content)
    json_data = extract_json_data(html_content)

    combined_data = {
        "price": price,
        "specifications": specs,
        "additional_data": json_data
    }

    return combined_data


def encode_arabic(obj):
    if isinstance(obj, str):
        return obj.encode('utf-8').decode('utf-8')
    elif isinstance(obj, dict):
        return {encode_arabic(key): encode_arabic(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [encode_arabic(element) for element in obj]
    else:
        return obj


#
#
# import json
#
# # Specify the file path
# file_path = r'G:\My Drive\Personal\Work\offline\Jupyter\Git\testwebscraping\riyadh_villa_allrooms\response_data.json'
#
# # Open the JSON file and load the data
# with open(file_path, 'r') as file:
#     data = json.load(file)
#
# new_data={}
# def get_last_page(response_html):
#     soup = BeautifulSoup(response_html, 'html.parser')
#     # Look for a div that contains multiple numeric links and class containting pagination
#     potential_pagination_divs = soup.find_all('div', class_=lambda x: x and 'pagination' in x.lower())
#
#     for div in potential_pagination_divs:
#         # Find all links with numeric content
#         numeric_links = [a for a in div.find_all('a') if a.text.strip().isdigit()]
#         if numeric_links:
#             # Sort the links by their numeric value and get the highest
#             last_page = max(int(a.text.strip()) for a in numeric_links)
#             return last_page
#
#     # If we couldn't find it that way, try a more general approach
#     all_links = soup.find_all('a', href=True)
#     page_numbers = []
#     for link in all_links:
#         # Look for links that end with a number
#         match = re.search(r'/(\d+)/?$', link['href'])
#         if match:
#             page_numbers.append(int(match.group(1)))
#
#     return max(page_numbers) if page_numbers else 1
#
# file_path = r'G:\My Drive\Personal\Work\offline\Jupyter\Git\testwebscraping\riyadh_villa_allrooms\new_response_data.json'
# key999 =  list(data.keys())[0]
# new_data[key999] = get_last_page(b64decode(data[key999]).decode('utf-8'))
#
# for i, key in enumerate(list(data.keys())[1:], start=1):
#     value,_ = extract_listing_hrefs(b64decode(data[key]).decode('utf-8'), key)
#     new_data[key] = value
# with open(file_path, 'w') as file:
#     json.dump(new_data, file, indent=4)
#
