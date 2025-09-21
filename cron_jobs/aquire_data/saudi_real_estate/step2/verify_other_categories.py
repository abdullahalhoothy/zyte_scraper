import os
import pandas as pd

def find_other_categories():
    # Locate the processed CSV file
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saudi_real_estate.csv')
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return
    df = pd.read_csv(csv_path)
    # Find rows with category == 'others'
    others_df = df[df['category'] == 'others']
    if others_df.empty:
        print("No listings with unrecognized categories.")
    else:
        print(f"Found {len(others_df)} listings with unrecognized categories:")
        print(others_df[['category_id', 'category', 'rent_period', 'price_description']].drop_duplicates())

if __name__ == "__main__":
    find_other_categories()
