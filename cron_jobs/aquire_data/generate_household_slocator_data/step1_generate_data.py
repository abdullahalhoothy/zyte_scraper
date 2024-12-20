import pandas as pd
import numpy as np
import random
import os

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

def generate_household_data(num_records, city_bounds):
    household_data = []
    degrees = ["District", "City", "Region", "Country"]
    zoom_levels = ["11", "10", "8", "4"]  # Corresponding to the degrees
    
    for _ in range(num_records):
        city = random.choice(list(city_bounds.keys()))
        lat = round(
            random.uniform(city_bounds[city]["lat"][0], city_bounds[city]["lat"][1]), 6
        )
        lon = round(
            random.uniform(city_bounds[city]["lon"][0], city_bounds[city]["lon"][1]), 6
        )
        
        degree_idx = random.randint(0, len(degrees)-1)
        degree = degrees[degree_idx]
        zoom_level = zoom_levels[degree_idx]
        
        avg_size = round(random.uniform(2.5, 6.5), 1)
        median_size = round(avg_size + random.uniform(-0.5, 0.5), 1)
        
        record = {
            "Location": city,
            "geo_location": f"{lat}, {lon}",
            "Household Average Size": str(avg_size),
            "Household Median Size": str(median_size),
            "Degree": degree,
            "Zoom Level": zoom_level
        }
        household_data.append(record)
    
    return pd.DataFrame(household_data)
# Generate the data
household_df = generate_household_data(NUM_RECORDS, CITY_BOUNDS)
output_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "household_data.csv"
)
household_df.to_csv(output_path, index=False)
