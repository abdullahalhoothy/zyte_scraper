import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)


CITY_BOUNDS = {
    "Mecca": {"lat": (21.3500, 21.4500), "lon": (39.8000, 39.9000)},
    "Jeddah": {"lat": (21.4500, 21.5500), "lon": (39.1500, 39.2500)},
    "Riyadh": {"lat": (24.6000, 24.8000), "lon": (46.6000, 46.8000)},
    "Toronto": {"lat": (43.6000, 43.8000), "lon": (-79.4500, -79.3500)},
    "Montreal": {"lat": (45.5000, 45.6000), "lon": (-73.6500, -73.5500)},
}

NUM_RECORDS = 1000


def generate_economic_characteristics(num_records, city_bounds):
    economic_data = []
    industries = [
        "Technology",
        "Healthcare",
        "Education",
        "Finance",
        "Manufacturing",
        "Hospitality",
    ]
    employment_status = ["Full-time", "Part-time", "Self-employed", "Unemployed"]

    for _ in range(num_records):
        city = random.choice(list(city_bounds.keys()))
        lat = round(
            random.uniform(city_bounds[city]["lat"][0], city_bounds[city]["lat"][1]), 6
        )
        lon = round(
            random.uniform(city_bounds[city]["lon"][0], city_bounds[city]["lon"][1]), 6
        )
        emp_status = random.choice(employment_status)

        record = {
            "city": city,
            "geo_location": f"{lat}, {lon}",
            "annual_income": round(random.uniform(20000, 250000), 2),
            "employment_status": emp_status,
            "industry": random.choice(industries),
            "years_in_current_job": random.randint(0, 30),
            "unemployment_duration_months": (
                random.randint(0, 24) if emp_status == "Unemployed" else 0
            ),
        }
        economic_data.append(record)

    return pd.DataFrame(economic_data)


economic_df = generate_economic_characteristics(NUM_RECORDS, CITY_BOUNDS)
economic_df.to_csv("economic_characteristics_data.csv", index=False)
print(f"Economic Characteristics Data - Total records: {len(economic_df)}")
