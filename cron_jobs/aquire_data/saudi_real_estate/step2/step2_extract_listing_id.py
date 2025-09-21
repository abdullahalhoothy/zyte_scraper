import re

import pandas as pd
import os

def extract_listing_id(url):
    """
    Extracts the listing ID from a real estate URL. If not found, generates a fallback ID
    using a combination of letters and numbers from the URL.
    """
    # Try to extract the ID at the end of the URL (before comma or end)
    match = re.search(r'-(\d+)(?:,|$)', url)
    if match:
        return match.group(1)
    # Fallback: create an ID from letters and numbers in the URL
    fallback = ''.join(re.findall(r'[A-Za-z0-9]+', url))[-12:]
    return fallback


def add_listing_ids_to_csv(csv_path, chunk_size=5000):
    """
    Adds a 'listing_id' column to the CSV, extracted from the 'url' column.
    Overwrites the original file, processes in chunks for large files.
    Args:
        csv_path: Path to the input CSV file.
        chunk_size: Number of rows per chunk.
    """
    temp_path = csv_path + ".tmp"
    first_chunk = True
    print(f"Processing CSV to add listing IDs: {csv_path}")
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        print(f"Processing chunk with {len(chunk)} rows")
        chunk['listing_id'] = chunk['url'].apply(extract_listing_id)
        if first_chunk:
            chunk.to_csv(temp_path, index=False, mode='w')
            first_chunk = False
        else:
            chunk.to_csv(temp_path, index=False, mode='a', header=False)
    os.replace(temp_path, csv_path)
    print(f"Updated CSV with listing IDs in-place: {csv_path}")

if __name__ == "__main__":
    # Example usage
    url = "https://sa.aqar.fm/استراحة-للبيع/الطائف/حي-جبرة/شارع-ابن-عقيل-الرحبة-الطائف-6341881,"
    listing_id = extract_listing_id(url)
    print("Listing ID:", listing_id)
