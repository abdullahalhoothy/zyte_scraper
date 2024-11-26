import json
import os
from psycopg2.extras import Json
from psycopg2.extras import Json
import glob
import re
import os

from cron_jobs.aqar_zyte_gbucket_db.step2_transform_to_csv import flatten_json



def move_to_front(lst, items_to_move):
    front_items = [item for item in items_to_move if item in lst]
    remaining_items = [item for item in lst if item not in items_to_move]
    return front_items + remaining_items


def generate_insert_sql(directory, url, flattened_data, all_keys):
    items_to_move = [
        "price",
        "additional__WebListing_uri___location_lat",
        "additional__WebListing_uri___location_lng",
    ]
    all_keys = move_to_front(all_keys, items_to_move)
    columns = ["url"] + all_keys
    all_keys.remove("original_specifications")
    all_keys.remove("original_additional_data")
    values = [url]
    values.extend([flattened_data.get(key, None) for key in all_keys])
    values.extend(
        [
            Json(flattened_data.get("specifications", {})),
            Json(flattened_data.get("additional_data", {})),
        ]
    )

    placeholders = ", ".join([f"%s" for _ in range(len(columns))])
    column_names = ", ".join(f"{col.lower()}" for col in columns)

    sql = f"""
    INSERT INTO {directory} ({column_names})
    VALUES ({placeholders})
    ON CONFLICT (url) DO UPDATE
    SET {', '.join([f'{col.lower()} = EXCLUDED.{col.lower()}' for col in columns])};
    """

    return sql, tuple(values)


def process_and_insert_data(directory, cursor, all_keys, limit=3):
    json_files = glob.glob(os.path.join(directory, "*_response_data.json"))
    processed_files = set()
    sql_log_dir = "sql_logs"
    os.makedirs(sql_log_dir, exist_ok=True)

    files_processed = 0

    for file_path in json_files:
        if files_processed >= limit:
            break

        file_number = re.search(r"(\d+)_response_data\.json", file_path)
        if not file_number:
            print(f"Skipping file with invalid name format: {file_path}")
            continue

        file_number = file_number.group(1)
        log_file = os.path.join(sql_log_dir, f"{file_number}.sql")

        if os.path.exists(log_file):
            print(f"Skipping already processed file: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        sql_statements = []
        for url, listing_data in data.items():
            # Skip empty listings or listings with empty string values
            if not listing_data or all(v == "" for v in listing_data.values()):
                continue

            flattened = flatten_json(listing_data)
            sql, values = generate_insert_sql(
                directory, url, flattened, [col for col in all_keys if col and col != "url"]
            )
            sql_statements.append((sql, values))

        if not sql_statements:
            print(f"Skipping file with no valid data: {file_path}")
            continue

        # Execute SQL statements
        for sql, values in sql_statements:
            cursor.execute(sql, values)

        # Save SQL statements to log file
        with open(log_file, "w", encoding="utf-8") as log:
            for sql, values in sql_statements:
                log.write(f"{sql}\n{values}\n\n")

        processed_files.add(file_path)
        print(f"Processed file: {file_path}")

        files_processed += 1

    return processed_files


# def save_to_db(directories, conn):
#     try:


#         cursor = conn.cursor()

#         for directory in directories:

#             # Get all keys from the first 50 files
#             all_keys = get_all_keys(directory)

#             # Process and filter data
#             columns = process_and_filter_data(directory, all_keys)
#             columns.extend(["original_specifications", "original_additional_data"])

#             # Use the filtered DataFrame to create the table
#             create_table_sql = f"""
#             CREATE TABLE IF NOT EXISTS {directory} (
#                 url TEXT PRIMARY KEY,
#                 {', '.join([f'{col.lower()} TEXT' for col in columns if col and col != 'url'])},
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#             """

#             cursor.execute(create_table_sql)

#             # Process and insert data
#             processed_files = process_and_insert_data(
#                 directory, cursor, columns, limit=100
#             )

#             conn.commit()
#         print(
#             f"Data processing and insertion completed successfully. Processed {len(processed_files)} files."
#         )

#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()


