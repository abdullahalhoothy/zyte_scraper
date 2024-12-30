import geopandas as gpd
import pandas as pd
import zipfile
import os

# Set up paths
zip_file_path = r"cron_jobs\aquire_data\canada_census\ignore\lda_000a21a_e.zip"
ontario_csv = r"cron_jobs\aquire_data\canada_census\ignore\ontario_eng.csv"
quebec_csv = r"cron_jobs\aquire_data\canada_census\ignore\quebec_eng.csv"
temp_dir = r"cron_jobs\aquire_data\canada_census\ignore"
output_dir = r"cron_jobs\aquire_data\canada_census\canada_census"

# Create directories
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

def process_census_data(csv_file):
   # Read and process census data
   census_data = pd.read_csv(csv_file,
                            skiprows=7,
                            thousands=',')
   
   census_data.columns = ['DA_ID'] + list(census_data.columns[1:])
   census_data = census_data[census_data['DA_ID'] != 'Geographic name']
   census_data = census_data[census_data['DA_ID'].str.match(r'^\d+$|^\d+\s+\d+$', na=False)]
   
   # Clean up the data types
   for col in census_data.columns[1:]:
       census_data[col] = pd.to_numeric(census_data[col], errors='coerce')
   
   # Clean up DA_ID
   census_data['DA_ID'] = census_data['DA_ID'].str.replace(' ', '')
   
   return census_data

# Process shapefile
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
   zip_ref.extractall(temp_dir)

shp_file = gpd.read_file(os.path.join(temp_dir, "lda_000a21a_e.shp"))
shp_file_projected = shp_file.to_crs('EPSG:3347')
centroids = shp_file_projected.geometry.centroid
centroids = gpd.GeoSeries(centroids, crs='EPSG:3347').to_crs('EPSG:4326')

shp_file['longitude'] = centroids.x
shp_file['latitude'] = centroids.y
shp_file = shp_file[['DAUID', 'longitude', 'latitude']]

# Process both provinces
ontario_data = process_census_data(ontario_csv)
quebec_data = process_census_data(quebec_csv)

# Add province column to each dataset
ontario_data['province'] = 'Ontario'
quebec_data['province'] = 'Quebec'

# Combine the provincial data
combined_census_data = pd.concat([ontario_data, quebec_data], ignore_index=True)

# Merge with geographic data
merged_data = combined_census_data.merge(shp_file,
                                      left_on='DA_ID',
                                      right_on='DAUID',
                                      how='left')

# Drop duplicate DAUID column if exists
if 'DAUID' in merged_data.columns:
   merged_data = merged_data.drop('DAUID', axis=1)

# Clean up column names
merged_data.columns = [col.lower().replace(' ', '_').replace(',', '').strip() 
                     for col in merged_data.columns]

# Save to CSV in the canada_census folder
output_file = os.path.join(output_dir, 'canada_census_data.csv')
merged_data.to_csv(output_file, index=False)

print("Number of records processed:", len(merged_data))
print("Column names:")
print(merged_data.columns.tolist())
print("\nSample of first few rows:")
print(merged_data.head())
print(f"\nData saved to: {output_file}")