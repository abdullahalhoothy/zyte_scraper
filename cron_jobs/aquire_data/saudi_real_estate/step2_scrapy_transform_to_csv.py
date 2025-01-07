import os
import pandas as pd

category_mapping_en = {
    1: "apartment_for_rent",
    2: "land_for_sale",
    3: "villa_for_sale",
    4: "floor_for_rent",
    5: "villa_for_rent",
    6: "apartment_for_sale",
    7: "building_for_sale",
    8: "shop_for_rent",
    9: "house_for_sale",
    10: "rest_house_for_sale",
    11: "house_for_rent",
    12: "farm_for_sale",
    13: "rest_house_for_rent",
    14: "commercial_office_for_rent",
    15: "land_for_rent",
    16: "building_for_rent",
    17: "warehouse_for_rent",
    18: "camp_for_rent",
    19: "room_for_rent",
    20: "shop_for_sale",
    21: "furnished_apartment_for_rent",
    22: "floor_for_sale",
    23: "chalet_for_rent"
}

rent_period_mapping = {
    0: "For Sale",
    1: "For Rent",
    2: "For Rent (Monthly)",
    3: "For Rent (Yearly)"
}

def process_real_estate_data(file_path):
    df = pd.read_csv(file_path, usecols=lambda x: x != 'data')
    
    if 'rent_period' not in df.columns or 'category_id' not in df.columns:
        raise ValueError("CSV must contain 'rent_period' and 'category_id' columns")
    
    df['category_id'] = pd.to_numeric(df['category_id'], errors='coerce')
    df = df.rename(columns={'category': 'category_ar'})
    df['category'] = df['category_id'].fillna(-1).astype(int).map(category_mapping_en).fillna('others')
    df['rent_period'] = pd.to_numeric(df['rent_period'], errors='coerce')
    
    # Set price_description based on category first
    for_sale_mask = df['category'].str.contains('for_sale', case=False, na=False)
    df.loc[for_sale_mask, 'price_description'] = 'For Sale'

    # if we have for_rent in category use rent_period_mapping
    for_rent_mask = df['category'].str.contains('for_rent', case=False, na=False)
    df.loc[for_rent_mask, 'price_description'] = df.loc[for_rent_mask, 'rent_period'].fillna(-1).astype(int).map(rent_period_mapping).fillna('For Rent')
    
    # else see if we have rent_period mapping otherwise keep it empty
    df.loc[~for_sale_mask & ~for_rent_mask, 'price_description'] = df.loc[~for_sale_mask & ~for_rent_mask, 'rent_period'].fillna(-1).astype(int).map(rent_period_mapping).fillna('')
    
    return df

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), 'ignore', 'raw_saudi_real_estate.csv')
    output_path = os.path.join(os.path.dirname(__file__), 'saudi_real_estate.csv')

    print("Processing raw data...")
    df = process_real_estate_data(file_path)
    print("Data processing complete. Saving to CSV...")
    df.to_csv(output_path, index=False, mode='w')
    print(f"CSV file saved to {output_path}")
