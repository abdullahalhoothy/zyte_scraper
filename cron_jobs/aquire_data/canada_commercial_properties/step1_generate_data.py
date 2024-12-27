import os
import httpx
import asyncio
import pandas as pd

from .helpers import establish_session, get_inscriptions, get_total_property_count, get_property_data, demographic_endpoint_closure_client


async def process_property(semaphore, client, demographic_endpoint_client, i, total_count):
    async with semaphore:
        print(f"Processing property {i+1}/{total_count}")
        response = await get_inscriptions(client, i)
        html_content = response['d'].get('Result', {}).get('html')
        if html_content is None:
            raise Exception("Unable to get Property Data")

        property_data = await get_property_data(client, demographic_endpoint_client, html_content)

        transport_scores = property_data.get('transport_scores', {})
        socio_demographic_data = property_data.get('socio_demographic_data', {})

        flat_data = {
            'url': property_data.get('url'),
            'address': property_data.get('address'),
            'price': property_data.get('price'),
            'use_of_property': property_data.get('use_of_property'),
            'available_commercial_area': property_data.get('available_commercial_area'),
            'number_of_units': property_data.get('number_of_units'),
            'type_of_business': property_data.get('type_of_business'),
            'walk_score': property_data.get('walk_score'),
            'description': property_data.get('description'),
            'latitude': property_data.get('latitude'),
            'longitude': property_data.get('longitude'),
            'region_stats_summary': property_data.get('region_stats_summary'),
            'city_id': property_data.get('city_id'),
            'city_name': property_data.get('city_name'),
            'walking_transport_score': transport_scores.get('walking_transport_score'),
            'transit_transport_score': transport_scores.get('transit_transport_score'),
            'cycling_transport_score': transport_scores.get('cycling_transport_score'),
            'driving_transport_score': transport_scores.get('driving_transport_score'),
            'primary_schools_score': transport_scores.get('primary_schools_score'),
            'high_schools_score': transport_scores.get('high_schools_score'),
            'daycares_score': transport_scores.get('daycares_score'),
            'groceries_score': transport_scores.get('groceries_score'),
            'restaurants_score': transport_scores.get('restaurants_score'),
            'shopping_score': transport_scores.get('shopping_score'),
            'cafes_score': transport_scores.get('cafes_score'),
            'quiet_score': transport_scores.get('quiet_score'),
            'nightlife_score': transport_scores.get('nightlife_score'),
            'vibrant_score': transport_scores.get('vibrant_score'),
            'historic_score': transport_scores.get('historic_score'),
            'parks_score': transport_scores.get('parks_score'),
            'greenery_score': transport_scores.get('greenery_score'),
            'age': socio_demographic_data.get('age'),
            'incomes': socio_demographic_data.get('incomes'),
            'household': socio_demographic_data.get('household'),
            'family': socio_demographic_data.get('family'),
            'occupation': socio_demographic_data.get('occupation'),
            'construction': socio_demographic_data.get('construction'),
            'housing': socio_demographic_data.get('housing'),
            'schooling': socio_demographic_data.get('schooling'),
            'immigration': socio_demographic_data.get('immigration'),
            'language': socio_demographic_data.get('language')
        }
        print(f"Processed property {i+1}/{total_count}: {property_data.get('address')}")
        return flat_data

async def process_batch(semaphore, client, demographic_endpoint_client, property_indices, total_count):
    tasks = [
        process_property(semaphore, client, demographic_endpoint_client, i, total_count)
        for i in property_indices
    ]
    results = await asyncio.gather(*tasks)
    return [result for result in results if result is not None]  


async def main():
    batch_size = 10
    temp_dir = os.path.join(os.path.dirname(__file__), "ignore")
    os.makedirs(temp_dir, exist_ok=True)

    output_file = os.path.join(temp_dir, 'raw_commercial_properties.csv')

    async with httpx.AsyncClient() as client:
        await establish_session(client)
        demographic_endpoint_client = demographic_endpoint_closure_client()
        total_count = await get_total_property_count(client)
        print(f"Total properties: {total_count}")

        if total_count <= 0:
            print("Unable to fetch properties. Please Check.")
            return

        semaphore = asyncio.Semaphore(batch_size)

        properties_list = []

        for i in range(0, total_count, batch_size):
            batch_indices = range(i, min(i + batch_size, total_count))
            print(f"Processing batch of properties: {batch_indices}")
            batch_results = await process_batch(semaphore, client, demographic_endpoint_client, batch_indices, total_count)
            properties_list.extend(batch_results)
            print(f"Batch completed. Processed {len(properties_list)}/{total_count} properties.")

        # Create DataFrame and clean data
        df = pd.DataFrame(properties_list)
        df = df.drop_duplicates()
        
        # Replace newlines, commas and other problematic characters
        for column in df.columns:
            if df[column].dtype == 'object':
                df[column] = df[column].fillna('').astype(str).apply(lambda x: x.replace('\n', ' ')
                                                        .replace('\r', ' ')
                                                        .replace(',', '¸')
                                                        .strip())

        print("Total Properties: ", len(df))
        try:
            df.to_csv(output_file, sep=',', index=False, encoding='utf-8-sig')
            print(f"Data saved to {output_file} ({len(df)} unique properties)")
        except Exception as e:
            print(f"Failed to write to CSV: {e}")


if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

