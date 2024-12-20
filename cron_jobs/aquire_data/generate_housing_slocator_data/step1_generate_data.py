import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

CITY_BOUNDS = {
    # "Mecca": {"lat": (21.3500, 21.4500), "lon": (39.8000, 39.9000)},
    # "Jeddah": {"lat": (21.4500, 21.5500), "lon": (39.1500, 39.2500)},
    # "Riyadh": {"lat": (24.6000, 24.8000), "lon": (46.6000, 46.8000)},
    "Toronto": {"lat": (43.6000, 43.8000), "lon": (-79.4500, -79.3500)},
    "Montreal": {"lat": (45.5000, 45.6000), "lon": (-73.6500, -73.5500)},
}

NUM_RECORDS = 1000

def generate_housing_data(num_records, city_bounds):
    housing_data = []
    
    for _ in range(num_records):
        city = random.choice(list(city_bounds.keys()))
        lat = round(random.uniform(city_bounds[city]["lat"][0], city_bounds[city]["lat"][1]), 6)
        lon = round(random.uniform(city_bounds[city]["lon"][0], city_bounds[city]["lon"][1]), 6)
        
        # Generate base numbers ensuring they make logical sense
        total_dwellings = random.randint(100, 1000)
        residential = random.randint(int(total_dwellings * 0.7), int(total_dwellings * 0.9))
        non_residential = total_dwellings - residential
        
        # Break down residential dwellings
        owned = random.randint(int(residential * 0.3), int(residential * 0.5))
        rented = random.randint(int(residential * 0.2), int(residential * 0.4))
        provided = random.randint(int(residential * 0.05), int(residential * 0.15))
        other_residential = residential - (owned + rented + provided)
        
        # Break down non-residential dwellings
        public_housing = random.randint(int(non_residential * 0.2), int(non_residential * 0.4))
        work_camps = random.randint(int(non_residential * 0.1), int(non_residential * 0.3))
        commercial = random.randint(int(non_residential * 0.1), int(non_residential * 0.3))
        other_dwellings = non_residential - (public_housing + work_camps + commercial)
        
        record = {
            "geo_location": f"{lat}, {lon}",
            "Total Dwellings": total_dwellings,
            "Residential Dwellings": residential,
            "Owned Dwellings": owned,
            "Rented Dwellings": rented,
            "Provided Dwellings": provided,
            "Other Residential Dwellings": other_residential,
            "Non-Residential Dwellings": non_residential,
            "Public Housing": public_housing,
            "Work Camps": work_camps,
            "Commercial Dwellings": commercial,
            "Other Dwellings": other_dwellings
        }
        housing_data.append(record)
    
    return pd.DataFrame(housing_data)

housing_df = generate_housing_data(NUM_RECORDS, CITY_BOUNDS)
housing_df.to_csv("housing_units_data.csv", index=True)
print(f"Housing Units Data - Total records: {len(housing_df)}")