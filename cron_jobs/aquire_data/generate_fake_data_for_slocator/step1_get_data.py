import pandas as pd
import numpy as np
from faker import Faker
import random

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

fake = Faker()


CITY_BOUNDS = {
    'Mecca': {'lat': (21.3500, 21.4500), 'lon': (39.8000, 39.9000)},
    'Jeddah': {'lat': (21.4500, 21.5500), 'lon': (39.1500, 39.2500)},
    'Riyadh': {'lat': (24.6000, 24.8000), 'lon': (46.6000, 46.8000)},
    'Toronto': {'lat': (43.6000, 43.8000), 'lon': (-79.4500, -79.3500)},
    'Montreal': {'lat': (45.5000, 45.6000), 'lon': (-73.6500, -73.5500)}
}

NUM_RECORDS = 1000

def generate_housing_units(num_records, city_bounds):
    housing_data = []
    housing_types = ['Apartment', 'Single-Family Home', 'Townhouse', 'Condominium', 'Duplex']
    ownership_status = ['Owned', 'Rented', 'Shared']
    
    for _ in range(num_records):
        city = random.choice(list(city_bounds.keys()))
        lat = round(random.uniform(city_bounds[city]['lat'][0], city_bounds[city]['lat'][1]), 6)
        lon = round(random.uniform(city_bounds[city]['lon'][0], city_bounds[city]['lon'][1]), 6)
        
        record = {
            'city': city,
            'geo_location': f'{lat}, {lon}',
            'housing_type': random.choice(housing_types),
            'ownership_status': random.choice(ownership_status),
            'total_rooms': random.randint(1, 6),
            'total_bathrooms': random.randint(1, 3),
            'square_footage': random.randint(500, 3000),
            'year_built': random.randint(1950, 2023),
            'property_value': round(random.uniform(50000, 1000000), 2)
        }
        housing_data.append(record)
    
    return pd.DataFrame(housing_data)

def generate_social_characteristics(num_records, city_bounds):
    social_data = []
    education_levels = ['High School', 'Bachelor', 'Master', 'PhD', 'Associate Degree']
    languages = ['Arabic', 'English', 'French', 'Spanish', 'Mandarin']
    
    for _ in range(num_records):
        city = random.choice(list(city_bounds.keys()))
        lat = round(random.uniform(city_bounds[city]['lat'][0], city_bounds[city]['lat'][1]), 6)
        lon = round(random.uniform(city_bounds[city]['lon'][0], city_bounds[city]['lon'][1]), 6)
        primary_language = random.choice(languages)
        
        record = {
            'city': city,
            'geo_location': f'{lat}, {lon}',
            'education_level': random.choice(education_levels),
            'primary_language': primary_language,
            'secondary_language': random.choice([lang for lang in languages if lang != primary_language]),
            'language_proficiency': round(random.uniform(0, 100), 2),
            'years_of_education': random.randint(12, 25)
        }
        social_data.append(record)
    
    return pd.DataFrame(social_data)

def generate_economic_characteristics(num_records, city_bounds):
    economic_data = []
    industries = ['Technology', 'Healthcare', 'Education', 'Finance', 'Manufacturing', 'Hospitality']
    employment_status = ['Full-time', 'Part-time', 'Self-employed', 'Unemployed']
    
    for _ in range(num_records):
        city = random.choice(list(city_bounds.keys()))
        lat = round(random.uniform(city_bounds[city]['lat'][0], city_bounds[city]['lat'][1]), 6)
        lon = round(random.uniform(city_bounds[city]['lon'][0], city_bounds[city]['lon'][1]), 6)
        emp_status = random.choice(employment_status)
        
        record = {
            'city': city,
            'geo_location': f'{lat}, {lon}',
            'annual_income': round(random.uniform(20000, 250000), 2),
            'employment_status': emp_status,
            'industry': random.choice(industries),
            'years_in_current_job': random.randint(0, 30),
            'unemployment_duration_months': random.randint(0, 24) if emp_status == 'Unemployed' else 0
        }
        economic_data.append(record)
    
    return pd.DataFrame(economic_data)

def generate_demographics(num_records, city_bounds):
    demographic_data = []
    age_groups = ['0-18', '19-35', '36-50', '51-65', '65+']
    household_types = ['Single', 'Couple', 'Family with Children', 'Multi-generational']
    
    for _ in range(num_records):
        city = random.choice(list(city_bounds.keys()))
        lat = round(random.uniform(city_bounds[city]['lat'][0], city_bounds[city]['lat'][1]), 6)
        lon = round(random.uniform(city_bounds[city]['lon'][0], city_bounds[city]['lon'][1]), 6)
        
        record = {
            'city': city,
            'geo_location': f'{lat}, {lon}',
            'age_group': random.choice(age_groups),
            'household_type': random.choice(household_types),
            'household_size': random.randint(1, 6),
            'gender': random.choice(['Male', 'Female']),
            'marital_status': random.choice(['Single', 'Married', 'Divorced', 'Widowed'])
        }
        demographic_data.append(record)
    
    return pd.DataFrame(demographic_data)

housing_df = generate_housing_units(NUM_RECORDS, CITY_BOUNDS)
housing_df.to_csv('housing_units_data.csv', index=False)
print(f"Housing Units Data - Total records: {len(housing_df)}")

social_df = generate_social_characteristics(NUM_RECORDS, CITY_BOUNDS)
social_df.to_csv('social_characteristics_data.csv', index=False)
print(f"Social Characteristics Data - Total records: {len(social_df)}")

economic_df = generate_economic_characteristics(NUM_RECORDS, CITY_BOUNDS)
economic_df.to_csv('economic_characteristics_data.csv', index=False)
print(f"Economic Characteristics Data - Total records: {len(economic_df)}")

demographics_df = generate_demographics(NUM_RECORDS, CITY_BOUNDS)
demographics_df.to_csv('demographics_data.csv', index=False)
print(f"Demographics Data - Total records: {len(demographics_df)}")