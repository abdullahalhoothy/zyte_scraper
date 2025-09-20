from datetime import datetime
import os
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from step2_traffic_analysis import GoogleMapsTrafficAnalyzer, logger
from step2_scrapy_transform_to_csv import process_real_estate_data
from step2_add_population import fetch_demographics


def filter_and_save_riyadh_records(csv_path, output_path, chunk_size=5000):
    """
    Filter Riyadh records from the input CSV and save to a new CSV file.
    """
    # Only keep required columns for Riyadh
    required_columns = ["url", "latitude", "longitude", "city"]
    first_chunk = True
    for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
        riyadh_chunk = chunk[chunk["city"] == "الرياض"].copy()
        riyadh_chunk = riyadh_chunk[required_columns]
        if first_chunk:
            riyadh_chunk.to_csv(output_path, index=False, mode="w")
            first_chunk = False
        else:
            riyadh_chunk.to_csv(
                output_path, index=False, mode="a", header=False
            )
    logger.info(f"Riyadh records saved to: {output_path}")


def add_columns_to_csv(csv_path, columns, temp_path, chunk_size=5000):
    """
    Add columns to CSV if they don't exist and save to temp file.
    """
    # Only keep minimal input columns plus new columns
    input_columns = ["url", "latitude", "longitude", "city"]
    all_columns = input_columns + columns
    first_chunk = True
    for chunk_idx, chunk in enumerate(
        pd.read_csv(csv_path, chunksize=chunk_size)
    ):
        # Only keep input columns
        chunk = chunk[input_columns]
        for col in columns:
            if col not in chunk.columns:
                chunk[col] = None
        chunk = chunk[all_columns]
        if first_chunk:
            chunk.to_csv(temp_path, index=False, mode="w")
            first_chunk = False
        else:
            chunk.to_csv(temp_path, index=False, mode="a", header=False)


def get_riyadh_locations(temp_path, key_column, chunk_size=5000):
    """
    Get Riyadh locations that need processing (where key_column is NaN).
    """
    locations = []
    for chunk in pd.read_csv(temp_path, chunksize=chunk_size):
        riyadh_chunk = chunk[chunk["city"] == "الرياض"].copy()
        if len(riyadh_chunk) > 0:
            unprocessed = riyadh_chunk[riyadh_chunk[key_column].isna()]
            for _, row in unprocessed.iterrows():
                locations.append(
                    {
                        "lat": row["latitude"],
                        "lng": row["longitude"],
                        "index": row.name if hasattr(row, "name") else None,
                    }
                )
    return locations


def update_csv_with_results(
    temp_path,
    results,
    columns,
    object_columns=[
        "demographics_details",
        "demographics_analysis_date",
        "traffic_details",
        "traffic_analysis_date",
    ],
    date_columns=["demographics_analysis_date", "traffic_analysis_date"],
    city_filter="الرياض",
    chunk_size=5000,
):
    """
    Update temp CSV file with results for Riyadh locations.
    """
    temp_updated_path = f"{temp_path}_updating"
    first_chunk_update = True
    # Only keep minimal input columns plus new columns
    input_columns = ["url", "latitude", "longitude", "city"]
    all_columns = input_columns + columns
    for chunk_idx, chunk in enumerate(
        pd.read_csv(temp_path, chunksize=chunk_size)
    ):
        # Ensure object dtype for relevant columns
        for col in object_columns:
            if col in chunk.columns:
                chunk[col] = chunk[col].astype("object")
        riyadh_mask = chunk["city"] == city_filter
        for idx in chunk[riyadh_mask].index:
            chunk_lat = chunk.loc[idx, "latitude"]
            chunk_lng = chunk.loc[idx, "longitude"]
            coord_key = f"{chunk_lat}_{chunk_lng}"
            if coord_key in results:
                for col in columns:
                    value = results[coord_key].get(col, None)
                    # Cast date columns to string
                    if col in date_columns and value is not None:
                        value = str(value)
                    chunk.loc[idx, col] = value
        # Only keep minimal columns before saving
        chunk = chunk[all_columns]
        if first_chunk_update:
            chunk.to_csv(temp_updated_path, index=False, mode="w")
            first_chunk_update = False
        else:
            chunk.to_csv(temp_updated_path, index=False, mode="a", header=False)
    os.replace(temp_updated_path, temp_path)


def process_riyadh_real_estate_traffic(csv_path: str, batch_size: int) -> str:
    """
    Process only Riyadh records for traffic analysis and save to a dedicated CSV.
    """
    base_path = csv_path.rsplit(".csv", 1)[0]
    riyadh_csv_path = f"{base_path}_riyadh.csv"
    output_path = f"{base_path}_riyadh_enriched_with_traffic.csv"
    temp_path = f"{base_path}__riyadh_traffic_temp_processing.csv"
    chunk_size = 5000
    traffic_columns = [
        "traffic_score",
        "traffic_details",
        "traffic_analysis_date",
    ]

    # ...existing code...
    logger.info("Starting traffic analysis for Riyadh locations")
    logger.info(f"Input CSV: {riyadh_csv_path}")
    logger.info(f"Enriched Output CSV: {output_path}")

    add_columns_to_csv(riyadh_csv_path, traffic_columns, temp_path, chunk_size)
    riyadh_locations = get_riyadh_locations(
        temp_path, "traffic_score", chunk_size
    )
    logger.info(
        f"Found {len(riyadh_locations)} Riyadh locations needing traffic analysis"
    )
    if len(riyadh_locations) == 0:
        logger.info("All Riyadh locations already have traffic data")
        os.rename(temp_path, output_path)
        logger.info(f"All data saved to: {output_path}")
        return output_path

    processed_count = 0
    traffic_results = {}
    total_locations = len(riyadh_locations)

    for batch_start in range(0, total_locations, batch_size):
        batch = riyadh_locations[batch_start:batch_start+batch_size]
        logger.info(f"Processing traffic for batch {batch_start+1}-{min(batch_start+batch_size, total_locations)} of {total_locations}")
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_loc = {
                executor.submit(
                    lambda loc: GoogleMapsTrafficAnalyzer(cleanup_driver=True).analyze_location_traffic(
                        lat=loc["lat"], lng=loc["lng"], day_of_week="Monday", target_time="6:00PM"
                    ), loc
                ): loc for loc in batch
            }
            for future in as_completed(future_to_loc):
                loc = future_to_loc[future]
                lat, lng = loc["lat"], loc["lng"]
                try:
                    traffic_result = future.result()
                except Exception as e:
                    logger.error(f"Traffic analysis failed for {lat}, {lng}: {e}")
                    traffic_result = {"score": 0, "error": str(e)}
                coord_key = f"{lat}_{lng}"
                traffic_results[coord_key] = {
                    "traffic_score": traffic_result.get("score", 0),
                    "traffic_details": json.dumps(traffic_result) if traffic_result else None,
                    "traffic_analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                processed_count += 1
        logger.info(f"Progress checkpoint: {processed_count}/{total_locations} locations processed")
        update_csv_with_results(
            temp_path,
            traffic_results,
            traffic_columns,
            object_columns=[
                "demographics_details",
                "demographics_analysis_date",
                "traffic_details",
                "traffic_analysis_date",
            ],
            date_columns=["demographics_analysis_date", "traffic_analysis_date"],
            city_filter="الرياض",
            chunk_size=chunk_size,
        )
        logger.info(f"Batch progress saved: {processed_count} records updated in CSV")
        traffic_results = {}  # Clear for next batch
    logger.info("Finalizing enriched output file...")
    os.rename(temp_path, output_path)
    logger.info(f"Traffic analysis completed: {processed_count} locations processed")
    logger.info(f"Enriched CSV with all data saved to: {output_path}")
    return output_path


def process_riyadh_real_estate_demographics(
    csv_path: str, batch_size: int
) -> str:
    """
    Process only Riyadh records for demographic analysis and save to a dedicated CSV.
    """
    base_path = csv_path.rsplit(".csv", 1)[0]
    riyadh_csv_path = f"{base_path}_riyadh.csv"
    output_path = f"{base_path}_riyadh_enriched_with_demographics.csv"
    temp_path = f"{base_path}_riyadh_temp_demographics.csv"
    chunk_size = 5000
    demographic_columns = [
        "total_population",
        "avg_density",
        "avg_median_age",
        "avg_income",
        "percentage_age_above_20",
        "percentage_age_above_25",
        "percentage_age_above_30",
        "percentage_age_above_35",
        "percentage_age_above_40",
        "percentage_age_above_45",
        "percentage_age_above_50",
        "demographics_details",
        "demographics_analysis_date",
    ]

    logger.info("Starting demographic analysis for Riyadh locations")
    logger.info(f"Input CSV: {riyadh_csv_path}")
    logger.info(f"Enriched Output CSV: {output_path}")

    add_columns_to_csv(
        riyadh_csv_path, demographic_columns, temp_path, chunk_size
    )
    riyadh_locations = get_riyadh_locations(
        temp_path, "total_population", chunk_size
    )
    logger.info(
        f"Found {len(riyadh_locations)} Riyadh locations needing demographic analysis"
    )
    if len(riyadh_locations) == 0:
        logger.info("All Riyadh locations already have demographic data")
        os.rename(temp_path, output_path)
        logger.info(f"All data saved to: {output_path}")
        return output_path

    processed_count = 0
    demo_results = {}
    total_locations = len(riyadh_locations)
    from step2_add_population import login_and_get_user

    for batch_start in range(0, total_locations, batch_size):
        batch = riyadh_locations[batch_start : batch_start + batch_size]
        logger.info(
            f"Processing demographics for batch {batch_start+1}-{min(batch_start+batch_size, total_locations)} of {total_locations}"
        )
        user_id, id_token = login_and_get_user()
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_loc = {
                executor.submit(
                    fetch_demographics,
                    loc["lat"],
                    loc["lng"],
                    user_id,
                    id_token,
                ): loc
                for loc in batch
            }
            for future in as_completed(future_to_loc):
                loc = future_to_loc[future]
                lat, lng = loc["lat"], loc["lng"]
                demo_result = future.result()
                demo_results[f"{lat}_{lng}"] = {
                    **demo_result,
                    "demographics_details": json.dumps(demo_result),
                    "demographics_analysis_date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                processed_count += 1
        logger.info(
            f"Progress checkpoint: {processed_count}/{total_locations} locations processed"
        )
        update_csv_with_results(temp_path, demo_results, demographic_columns)
        logger.info(
            f"Batch progress saved: {processed_count} records updated in CSV"
        )
        demo_results = {}  # Clear for next batch
    logger.info("Finalizing enriched output file...")
    os.rename(temp_path, output_path)
    logger.info(
        f"Demographic analysis completed: {processed_count} locations processed"
    )
    logger.info(f"Enriched CSV with all data saved to: {output_path}")
    return output_path


# Cross-platform check for Riyadh CSV age and creation
def ensure_riyadh_csv(csv_path, chunk_size=5000):
    base_path = csv_path.rsplit(".csv", 1)[0]
    riyadh_csv_path = f"{base_path}_riyadh.csv"
    need_create = True
    if os.path.exists(riyadh_csv_path):
        last_modified = datetime.fromtimestamp(
            os.path.getmtime(riyadh_csv_path)
        )
        now = datetime.now()
        if (now - last_modified).days < 1:
            need_create = False
    if need_create:
        print(f"Creating Riyadh CSV: {riyadh_csv_path}")
        filter_and_save_riyadh_records(csv_path, riyadh_csv_path, chunk_size)
    else:
        print(f"Riyadh CSV is up-to-date: {riyadh_csv_path}")
    return riyadh_csv_path


# Main script logic
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "..", "saudi_real_estate.csv")
chunk_size = 5000
# Ensure Riyadh CSV is created/updated if needed
ensure_riyadh_csv(csv_path, chunk_size)
# Example usage:
process_riyadh_real_estate_traffic(csv_path, 5)
# process_riyadh_real_estate_demographics(csv_path, 10)
