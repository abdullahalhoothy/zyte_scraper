import pandas as pd
import os

# Define the locations with their bounding boxes
locations = [
    {
        "name": "Jeddah",
        "max_lat": 21.904,
        "min_lat": 21.003,
        "max_lon": 39.400,
        "min_lon": 39.034
    },
    {
        "name": "Riyadh",
        "max_lat": 25.162,
        "min_lat": 24.292,
        "max_lon": 47.346,
        "min_lon": 46.295
    },
    {
        "name": "Makkah",
        "max_lat": 21.594,
        "min_lat": 21.278,
        "max_lon": 40.002,
        "min_lon": 39.69
    }
]

# Function to find the city for a given latitude and longitude
def find_city(lat, lon):
    for location in locations:
        if (location["min_lat"] <= lat <= location["max_lat"] and
            location["min_lon"] <= lon <= location["max_lon"]):
            return location["name"]
    return "Unknown"  # Return "Unknown" if the point is not in any city



if __name__ == "__main__":
    # loop over csv file in the csv_files directory
    for file in os.listdir("csv_files"):
        if file.endswith(".csv"):
            data = pd.read_csv(file)
            data["City"] = data.apply(lambda row: find_city(row["Latitude"], row["Longitude"]), axis=1)
            data.to_csv(file, index=False)
            print(f"City added to {file}")