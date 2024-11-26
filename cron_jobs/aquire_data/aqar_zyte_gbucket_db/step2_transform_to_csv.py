import numpy as np


import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from cron_jobs.aquire_data.aqar_zyte_gbucket_db.load_config import CONF
import pandas as pd
import re
import pickle
import glob
import json


def contains_arabic(text):
    arabic_pattern = re.compile("[\u0600-\u06FF]")
    return bool(arabic_pattern.search(str(text)))


def is_boolean_or_binary(series):
    unique_values = set(series.dropna().unique())
    return unique_values.issubset(
        {True, False, 0, 1, "0", "1", "True", "False", "true", "false"}
    )


def clean_key(key):
    # Remove numbers from the key
    key = re.sub(r"\d+", "", key)

    # If the key contains 'additional_data', remove numbers and Arabic letters
    if "additional_data" in key:
        key = re.sub(r"[\d\u0600-\u06FF]+", "", key)
    # Split the key into parts
    parts = key.split("_")

    # Keep the first part if it's 'specifications' or 'additional_data'
    first_part = parts[0]

    # Clean the last part
    key = re.sub(r"-+", "-", key)
    key = re.sub(r"\s+", "_", key)
    key = re.sub(r"[/\\]", "_", key)
    key = re.sub(r"['\"]+", "", key)
    key = re.sub(r"[\(\)\{\}\[\]]", "", key)
    key = re.sub(r"[!@#$%^&*+~;,.]", "", key)
    key = re.sub(r"[:-]", "_", key)

    # Truncate to PostgreSQL's column name length limit (63 bytes)
    last_part = key[-30:].replace(f"{first_part}_", "") if len(parts) > 1 else ""

    # Combine parts
    if first_part and last_part:
        cleaned_key = f"{first_part}_{last_part}"
    elif first_part:
        cleaned_key = first_part
    else:
        cleaned_key = last_part

    # Ensure the key doesn't start with a number
    if cleaned_key and cleaned_key[0].isdigit():
        cleaned_key = "col_" + cleaned_key

    # Remove any trailing underscores
    cleaned_key = cleaned_key.rstrip("_")

    return cleaned_key


def flatten_json(y):
    out = {}

    def flatten(x, name=""):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + "_")
        elif isinstance(x, list):
            for i, a in enumerate(x):
                flatten(a, name + str(i) + "_")
        else:
            clean_name = clean_key(name[:-1])
            out[clean_name] = x

    flatten(y)
    return out


def process_and_filter_data(directory, all_keys, num_files=350):
    dir_path = os.path.dirname(os.path.abspath(__file__)) + "\\" + directory
    df_save_path = os.path.join(dir_path, "processed_dataframe.pkl")
    all_col_names_path = os.path.join(dir_path, "process_and_filter_data.json")

    if os.path.exists(all_col_names_path):
        with open(all_col_names_path, "r", encoding="utf-8") as file:
            json_obj = json.load(file)
            return json_obj["sorted_new_keep_cols"]
    # Define the path for the saved DataFrame

    # Check if the processed DataFrame already exists
    if os.path.exists(df_save_path):
        print("Loading existing processed DataFrame...")
        with open(df_save_path, "rb") as f:
            df = pickle.load(f)
    else:
        print("Processing data and creating new DataFrame...")

        json_files = glob.glob(os.path.join(dir_path, "*_response_data.json"))
        data = []

        for file_path in json_files[:num_files]:
            with open(file_path, "r", encoding="utf-8") as file:
                file_data = json.load(file)
                for url, listing_data in file_data.items():
                    flattened = flatten_json(listing_data)
                    flattened["url"] = url
                    data.append(flattened)

        df = pd.DataFrame(data)

        # Save the DataFrame
        with open(df_save_path, "wb") as f:
            pickle.dump(df, f)
        print(f"DataFrame saved to {df_save_path}")

    if len(df.columns) > len(all_keys):
        all_keys.extend(df.columns)
        all_keys = list(set(all_keys))

    # Choose specific columns and drop others
    print("Dropping unnecessary columns...")
    columns_to_drop = [
        "additional_rops_path_listing_location_lat",
        "additional_lasticWebListing__location_lat",
        "additional_ended_details_national_address_latitude",
        "additional_rops_path_listing_location_lng",
        "additional_lasticWebListing__location_lng",
        "additional_ended_details_national_address_longitude",
    ]

    spec_cols = [col for col in all_keys if "specifications" in col]
    non_spec_cols = [col for col in all_keys if col not in spec_cols]
    df = df.drop(columns=[col for col in columns_to_drop if col in non_spec_cols])

    print("Selecting columns to keep...")
    value_counts = df.nunique() / len(df)
    columns_to_keep = [
        col
        for col in df.columns
        if value_counts[col] >= 0.00015 or is_boolean_or_binary(df[col])
    ]
    columns_to_keep.extend(
        [
            "additional__WebListing_uri___location_lat",
            "additional__WebListing_uri___location_lng",
        ]
    )

    df = df[columns_to_keep]

    # Drop columns with 'video' or 'img' in the name
    print("Dropping columns with 'video' or 'img' in the name...")
    df = df.drop(columns=[col for col in df.columns if "video" in col.lower()])
    df = df.drop(columns=[col for col in df.columns if "img" in col.lower()])

    # Drop columns where more than 50% of values contain more than 3 '/' or '\'
    print("Dropping columns with excessive slashes...")
    slash_mask = np.vectorize(lambda x: str(x).count("/") + str(x).count("\\") > 3)(
        df.values
    )
    slash_cols = df.columns[np.mean(slash_mask, axis=0) > 0.5]
    https_mask = np.vectorize(lambda x: str(x).startswith("https:"))(
        df[slash_cols].values
    )
    slash_cols = slash_cols[~np.any(https_mask, axis=0)]
    df = df.drop(columns=slash_cols)
    if "additional_rops_pageProps_path_listing_id" in df.columns:
        print(
            "Dropping columns related to 'additional_rops_pageProps_path_listing_id'..."
        )
        listing_id_col = df["additional_rops_pageProps_path_listing_id"].astype(str)
        id_mask = np.vectorize(lambda x: str(x) in listing_id_col.values)(df.values)
        id_cols = df.columns[np.mean(id_mask, axis=0) > 0.5]
        df = df.drop(
            columns=[
                col
                for col in id_cols
                if col != "additional_rops_pageProps_path_listing_id"
            ]
        )

    # Keep only the columns that are in all_keys plus 'url'
    print("Keeping only the required columns...")
    df = df[["url"] + [col for col in all_keys if col in df.columns]]
    new_keep_cols = df.columns.tolist()

    # Sort the columns
    print("Sorting the columns...")

    arabic_cols = [col for col in new_keep_cols if "specifications" in col]
    non_arabic_cols = [col for col in new_keep_cols if col not in arabic_cols]
    # Combine the sorted lists, with Arabic columns first
    sorted_new_keep_cols = arabic_cols + spec_cols + non_arabic_cols
    re_spec_cols = list(
        set([col for col in sorted_new_keep_cols if "specifications" in col])
    )
    re_nonspec_cols = list(
        set([col for col in sorted_new_keep_cols if "specifications" not in col])
    )
    re_nonspec_cols.remove("url")
    # re_nonspec_cols.remove("price")
    sorted_new_keep_cols = ["url", "price"] + re_spec_cols + re_nonspec_cols

    output_data = {"sorted_new_keep_cols": sorted_new_keep_cols}
    with open(all_col_names_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to: {all_col_names_path}")

    return sorted_new_keep_cols


def get_all_keys(directory, num_files=50):
    all_col_names_path = (
        os.path.dirname(os.path.abspath(__file__)) + "\\" + "all_col_names.json"
    )
    if os.path.exists(all_col_names_path):
        with open(all_col_names_path, "r", encoding="utf-8") as file:
            all_keys = json.load(file)
            return all_keys["all_col_names"]
    all_keys = set()
    json_files = glob.glob(os.path.join(directory, "*_response_data.json"))

    for file_path in json_files[:num_files]:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for listing_data in data.values():
            flattened = flatten_json(listing_data)
            all_keys.update(flattened.keys())

    list_all_keys = list(all_keys)
    list_all_keys.sort(reverse=True)
    try:
        list_all_keys.remove("")
    except:
        pass

    output_data = {"all_col_names": list(all_keys)}
    with open(all_col_names_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"Data saved to: {all_col_names_path}")
    return list_all_keys


def save_to_csv(directories):
    for directory in directories:
        # Get all keys from the first 50 files
        dir_path = os.path.dirname(os.path.abspath(__file__)) + "\\" + directory
        all_keys = get_all_keys(directory)

        # Process and filter data to get the columns
        columns = process_and_filter_data(directory, all_keys)
        columns.extend(["original_specifications", "original_additional_data"])

        # Create an empty list to store all data
        all_data = []

        # Process JSON files
        json_files = glob.glob(os.path.join(dir_path, "*_response_data.json"))

        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                for url, listing_data in data.items():
                    # Skip empty listings
                    if not listing_data or all(v == "" for v in listing_data.values()):
                        continue

                    flattened = flatten_json(listing_data)
                    flattened["url"] = url
                    all_data.append(flattened)

        # Create DataFrame
        df = pd.DataFrame(all_data)

        # Ensure all columns from the processed columns list exist
        for col in columns:
            if col not in df.columns:
                df[col] = None

        # Reorder columns to match the processed columns list
        df = df[columns]

        # Save to CSV
        df['city'] = dir_path.split("\\")[-1].split("_")[0]
        csv_filename = dir_path + "\\" + "data.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}")


save_to_csv(CONF.base_url_info)
