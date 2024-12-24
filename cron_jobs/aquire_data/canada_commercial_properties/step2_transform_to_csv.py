import pandas as pd
import os

# Set up paths
input_csv = os.path.join(os.path.dirname(__file__), "ignore", "raw_commercial_properties.csv")
output_dir = os.path.dirname(__file__)

# Create output directory
os.makedirs(output_dir, exist_ok=True)

def process_commercial_data(csv_file):
    df = pd.read_csv(csv_file)
    
    # Split price into price and price_description
    df[['price', 'price_description']] = df['price'].str.split('/', n=1, expand=True)
    df['price_description'] = "/" + df['price_description']
    
    # Split address into address and property_type
    df[['property_type', 'address']] = df['address'].str.split(':', n=1, expand=True)

    # Extract city from city_name
    df['city'] = df['city_name'].str.split().str[0]

    # strip whitespace from all columns
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    
    return df

# Process the data
if not os.path.exists(input_csv):
    print(f"Input file {input_csv} does not exist")
    exit(1)

commercial_data = process_commercial_data(input_csv)

# Save to CSV
output_file = os.path.join(output_dir, 'canada_commercial_properties.csv')
commercial_data.to_csv(output_file, index=False, encoding='utf-8-sig')

print("Number of records processed:", len(commercial_data))
print(f"\nData saved to: {output_file}")

