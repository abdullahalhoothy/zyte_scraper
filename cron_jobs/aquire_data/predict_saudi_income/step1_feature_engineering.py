import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import geopandas as gpd
from shapely.geometry import box
import contextily as ctx
import folium


class GeoIntelligence:
    def __init__(
        self,
        db_access_key,
        cities,
        grid_size=0.05,
        zoom_level=6,
        input_file_path=None,
        version=None,
        data_dir=None,
    ):
        self.cities = cities
        self.grid_size = grid_size
        self.zoom_level = zoom_level
        self.version = version
        self.data_dir = data_dir
        engine = create_engine(db_access_key)

        self.real_estate_data = pd.read_sql(
            """
                SELECT url, price, latitude, longitude, category_ar, category_id, city, city_id, title, address, rent_period, category, price_description
                FROM raw_schema_marketplace.saudi_real_estate;
            """,
            engine,
        )

        # Use the provided path for all_features.json
        population_data = gpd.GeoDataFrame.from_features(
            pd.read_json(input_file_path).features
        )
        self.population_grid = population_data.copy().fillna(0.0)

        if self.grid_size is None:
            self.grid_size = np.round((population_data.geometry.area.max())**0.5, 5) * 2.5
            self.grid_size = max(self.grid_size, 0.05)

        points = population_data.geometry.map(lambda x: x.centroid)
        population_data["longitude"] = points.map(lambda x: x.x)
        population_data["latitude"] = points.map(lambda x: x.y)
        population_data = (
            pd.DataFrame(population_data.drop("geometry", axis=1))
            .rename(columns={"PCNT": "TotalPopulation", "GLEVEL": "zoom_level"})
            .assign(
                MedianAgeMale=0.0, MedianAgeFemale=0.0, HouseholdAverageSize=0.0
            )
        )
        self.census_data = population_data

        x = self.real_estate_data.category.str.split("_for_")
        self.real_estate_data["building_type"] = x.map(lambda x: x[0])
        self.real_estate_data["trade_type"] = x.map(lambda x: x[1])

        self.housing_data = pd.read_sql(
            f"""
        SELECT "Location", "Selector", "Degree", "TotalDwellings", "ResidentialDwellings", "OwnedDwellings", "RentedDwellings", "ProvidedDwellings", "OtherResidentialDwellings", "Non-ResidentialDwellings", "PublicHousing", "WorkCamps", "CommercialDwellings", "OtherDwellings", "ZoomLevel", "TopLeftDegree", "BottomRightDegree", "ID", "Parent"
        FROM raw_schema_marketplace.housing {f'WHERE "ZoomLevel" = {zoom_level}' if zoom_level is not None else ''};
              """,
            engine,
        )

        x = self.housing_data.Location.str.split("-").map(lambda x: x[-1])
        self.housing_data["Location"] = x

        # Updated paths for CSV files
        self.city_data = {}
        for city in cities:
            city_name = city[-1]
            city_lower = city_name.lower()
            self.city_data[city_name] = {
                "google_data": pd.read_csv(
                    os.path.join(data_dir, f"restaurants_{city_lower}_full.csv")
                ).rename(columns={"lat": "latitude", "lng": "longitude"}),
                "royal_houses": pd.read_csv(
                    os.path.join(data_dir, f"{city_lower}_royal_houses.csv")
                ).rename(columns={"lat": "latitude", "lng": "longitude"}),
                "luxury_hotels": pd.read_csv(
                    os.path.join(data_dir, f"{city_lower}_luxury hotel.csv")
                ).rename(columns={"lat": "latitude", "lng": "longitude"}),
                "gyms": pd.read_csv(
                    os.path.join(data_dir, f"{city_lower}_gym.csv")
                ).rename(columns={"lat": "latitude", "lng": "longitude"}),
                "luxurious_areas": pd.read_csv(
                    os.path.join(data_dir, f"{city_lower}_luxurious_areas.csv")
                ).rename(columns={"lat": "latitude", "lng": "longitude"}),
            }

        self.city_boundaries = {}
        for city in cities:
            x1 = self.real_estate_data.loc[
                self.real_estate_data.city.isin(city)
            ][["latitude", "longitude", "building_type", "price"]]
            x1 = gpd.GeoDataFrame(
                x1, geometry=gpd.points_from_xy(x1.longitude, x1.latitude)
            )
            self.city_boundaries[city[-1]] = x1.unary_union.convex_hull

        self.norm = lambda x: (
            (x - x.min()) / (x.max() - x.min())
            if len(x) > 0 and x.max() != x.min()
            else x
        )
        self.grids = {}
        self.cmaps = [
            "Greys",
            "Purples",
            "Blues",
            "Greens",
            "Oranges",
            "Reds",
            "YlOrBr",
            "YlOrRd",
            "OrRd",
            "PuRd",
            "RdPu",
            "BuPu",
            "GnBu",
            "PuBu",
            "YlGnBu",
            "PuBuGn",
            "BuGn",
            "YlGn",
        ]
        self.population_grid = pd.concat([self.population_grid.loc[self.population_grid.within(cb)] for cb in self.city_boundaries.values()])

    def calculate_city_scores_task_1(self, city):
        # Get the city boundary for the current city
        city_boundary = self.city_boundaries[city[-1]]

        # Prepare real estate data for sale properties
        sale_properties = self.real_estate_data.loc[
            self.real_estate_data.city.isin(city)
        ].assign(
            is_villa=lambda df: df.building_type == "villa",
            is_apartment=lambda df: df.building_type == "apartment",
            is_above_average=lambda df: df.price > df.price.median(),
            selling_price=lambda df: np.where(
                df.trade_type == "sale", df.price, np.nan
            ),
            renting_price=lambda df: np.where(
                df.trade_type == "rent", df.price / df.rent_period, np.nan
            ),
        )
        sale_properties_gdf = gpd.GeoDataFrame(
            sale_properties,
            geometry=gpd.points_from_xy(
                sale_properties.longitude, sale_properties.latitude
            ),
        )

        # Prepare census data with age calculation
        census_data = self.census_data.assign(
            age=lambda df: df.MedianAgeMale * 0.5 + df.MedianAgeFemale * 0.5
        )[["TotalPopulation", "age", "longitude", "latitude"]]
        census_gdf = gpd.GeoDataFrame(
            census_data,
            geometry=gpd.points_from_xy(
                census_data.longitude, census_data.latitude
            ),
        )

        # Prepare restaurant data
        restaurants = self.city_data[city[-1]]["google_data"][
            ["rating", "longitude", "latitude"]
        ]
        restaurants_gdf = gpd.GeoDataFrame(
            restaurants,
            geometry=gpd.points_from_xy(
                restaurants.longitude, restaurants.latitude
            ),
        )

        # Prepare housing data
        housing_data = self.housing_data.loc[
            self.housing_data.Location == city[-1]
        ]
        degree_split = housing_data.Degree.str.split(" ")
        housing_data = housing_data.assign(
            latitude=degree_split.map(lambda x: float(x[1])),
            longitude=degree_split.map(lambda x: float(x[0])),
        )[["latitude", "longitude", "TotalDwellings"]]
        housing_gdf = gpd.GeoDataFrame(
            housing_data,
            geometry=gpd.points_from_xy(
                housing_data.longitude, housing_data.latitude
            ),
        )

        # Prepare royal houses data
        royal_houses = self.city_data[city[-1]]["royal_houses"][
            ["name", "longitude", "latitude"]
        ]
        royal_houses_gdf = gpd.GeoDataFrame(
            royal_houses,
            geometry=gpd.points_from_xy(
                royal_houses.longitude, royal_houses.latitude
            ),
        )

        # Prepare luxury hotels data
        luxury_hotels = self.city_data[city[-1]]["luxury_hotels"][
            ["name", "longitude", "latitude"]
        ]
        luxury_hotels_gdf = gpd.GeoDataFrame(
            luxury_hotels,
            geometry=gpd.points_from_xy(
                luxury_hotels.longitude, luxury_hotels.latitude
            ),
        )

        # Prepare gyms data
        gyms = self.city_data[city[-1]]["gyms"][
            ["name", "longitude", "latitude"]
        ]
        gyms_gdf = gpd.GeoDataFrame(
            gyms, geometry=gpd.points_from_xy(gyms.longitude, gyms.latitude)
        )

        # Prepare luxurious areas data
        luxurious_areas = self.city_data[city[-1]]["luxurious_areas"][
            ["name", "longitude", "latitude"]
        ]
        luxurious_areas_gdf = gpd.GeoDataFrame(
            luxurious_areas,
            geometry=gpd.points_from_xy(
                luxurious_areas.longitude, luxurious_areas.latitude
            ),
        )

        # Filter data to within city boundaries
        sale_properties_gdf = sale_properties_gdf.loc[
            sale_properties_gdf.within(city_boundary)
        ]
        census_gdf = census_gdf.loc[census_gdf.within(city_boundary)]
        restaurants_gdf = restaurants_gdf.loc[
            restaurants_gdf.within(city_boundary)
        ]
        housing_gdf = housing_gdf.loc[housing_gdf.within(city_boundary)]
        royal_houses_gdf = royal_houses_gdf.loc[
            royal_houses_gdf.within(city_boundary)
        ]
        luxury_hotels_gdf = luxury_hotels_gdf.loc[
            luxury_hotels_gdf.within(city_boundary)
        ]
        gyms_gdf = gyms_gdf.loc[gyms_gdf.within(city_boundary)]
        luxurious_areas_gdf = luxurious_areas_gdf.loc[
            luxurious_areas_gdf.within(city_boundary)
        ]

        # Create grid cells
        minx, miny, maxx, maxy = census_gdf.total_bounds
        grid_cells = [
            box(x, y, x + self.grid_size, y + self.grid_size)
            for x in np.arange(minx, maxx, self.grid_size)
            for y in np.arange(miny, maxy, self.grid_size)
        ]
        grid = gpd.GeoDataFrame(geometry=grid_cells, crs=census_gdf.crs)

        # Perform spatial joins
        joined_population = gpd.sjoin(
            census_gdf, grid, how="inner", predicate="within"
        )
        joined_real_estate = gpd.sjoin(
            sale_properties_gdf, grid, how="inner", predicate="within"
        )
        joined_restaurants = gpd.sjoin(
            restaurants_gdf, grid, how="inner", predicate="within"
        )
        joined_housing = gpd.sjoin(
            housing_gdf, grid, how="inner", predicate="within"
        )
        joined_royal_houses = gpd.sjoin(
            royal_houses_gdf, grid, how="inner", predicate="within"
        )
        joined_luxury_hotels = gpd.sjoin(
            luxury_hotels_gdf, grid, how="inner", predicate="within"
        )
        joined_gyms = gpd.sjoin(gyms_gdf, grid, how="inner", predicate="within")
        joined_luxurious_areas = gpd.sjoin(
            luxurious_areas_gdf, grid, how="inner", predicate="within"
        )

        # Aggregate data into the grid
        grid = pd.concat(
            [
                grid,
                joined_population.groupby("index_right")[
                    "TotalPopulation"
                ].sum(),
                joined_population.groupby("index_right")["age"].mean(),
                joined_real_estate.groupby("index_right")[
                    "selling_price"
                ].mean(),
                joined_real_estate.groupby("index_right")[
                    "renting_price"
                ].mean(),
                joined_real_estate.groupby("index_right")["is_villa"]
                .sum()
                .rename("villa_count"),
                joined_real_estate.groupby("index_right")["is_apartment"]
                .sum()
                .rename("apartment_count"),
                joined_real_estate.groupby("index_right")["is_above_average"]
                .sum()
                .rename("number_of_properties_above_average_price"),
                joined_restaurants.groupby("index_right")["rating"]
                .count()
                .rename("restaurant_count"),
                joined_housing.groupby("index_right")["TotalDwellings"].sum(),
                joined_royal_houses.groupby("index_right")["name"]
                .count()
                .rename("royal_property_count"),
                joined_luxury_hotels.groupby("index_right")["name"]
                .count()
                .rename("luxury_hotel_count"),
                joined_gyms.groupby("index_right")["name"]
                .count()
                .rename("gym_count"),
                joined_luxurious_areas.groupby("index_right")["name"]
                .count()
                .rename("luxury_area_count"),
            ],
            axis=1,
        )

        # Calculate villa-to-apartment ratio with safeguards
        grid = grid.assign(
            villa_to_apartment_ratio=lambda df: df.villa_count
            / (df.villa_count + df.apartment_count).replace(0, np.nan)
        )

        # Create a copy of the grid for reference
        grid_backup = grid.copy(deep=True)

        # Calculate indices and scores
        mask = grid.iloc[:, 1:].isna().all(axis=1)
        grid = (
            grid.fillna(0.0)
            .assign(
                real_estate_index=lambda df: 0.33
                * (
                    (self.norm(df.selling_price) + self.norm(df.renting_price))
                    / 2.0
                )
                + 0.33 * df.villa_to_apartment_ratio
                + 0.33 * self.norm(df.royal_property_count),
                population_index=lambda df: self.norm(df.TotalPopulation),
                amenity_index=lambda df: 0.3 * self.norm(df.restaurant_count)
                + 0.3 * self.norm(df.TotalDwellings)
                + 0.3 * self.norm(df.luxury_hotel_count)
                + 0.1 * self.norm(df.gym_count),
            )
            .assign(
                base_score=lambda df: 0.4 * df.real_estate_index
                + 0.3 * df.population_index
                + 0.3 * df.amenity_index,
                manual_rating=lambda df: self.norm(df.luxury_area_count),
            )
            .assign(
                consistency_score=lambda df: (df.base_score - df.manual_rating)
                .abs()
                .max()
                - (df.base_score - df.manual_rating).abs(),
                final_score=lambda df: df.base_score
                * (1 + df.consistency_score**0.2),
            )
        )

        # Combine original grid with calculated scores
        grid = pd.concat([grid_backup, grid.iloc[:, -7:]], axis=1)

        # Sort and handle missing values
        grid = grid.sort_values(by="base_score", ascending=False)
        grid.loc[mask, grid.columns[1:]] = np.nan

        # Store results
        self.grids[city[-1]] = grid.copy(deep=True)

    def save_grids_to_csv(self, output_dir):
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        for city in self.cities:
            city_name = city[-1]
            if city_name in self.grids:
                output_file = os.path.join(output_dir, f"{city_name}.csv")
                self.grids[city_name].to_csv(output_file, index=False)
                print(f"Saved: {output_file}")




# Main execution code
# Process all versions from 8 to 16
data_dir = "cron_jobs/aquire_data/saudi_census/get_data_using_requests"
max_version =  16

for version in range(8, max_version + 1):
    version_str = f"v{version}"
    max_version_str =  f"v{max_version}"

    print(f"\nProcessing {version_str}")

    # Define input and output paths
    input_path = os.path.join(
        "cron_jobs",
        "aquire_data",
        "saudi_census",
        "get_data_using_requests",
        "population_json_files",
        version_str,
        "all_features.json",
    )

    input_path_mx = os.path.join(
        "cron_jobs",
        "aquire_data",
        "saudi_census",
        "get_data_using_requests",
        "population_json_files",
        max_version_str,
        "all_features.json",
    )

    output_dir_mx = os.path.join("income_json_files", max_version_str)
    output_dir = os.path.join("income_json_files", version_str)

    # Skip if input file doesn't exist
    if not os.path.isfile(input_path):
        print(f"File not found: {input_path} - skipping version {version_str}")
        continue

    # Create output directory
    os.makedirs(output_dir_mx, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Initialize GeoIntelligence for this version
    output_geojson_mx = os.path.join(output_dir_mx, "all_features.json")

    if not os.path.isfile(output_geojson_mx):
        geo_intelligence = GeoIntelligence(
            db_access_key="postgresql://scraper_user:scraper_password@s-locator.northernacs.com:5432/dbo_operational",
            cities=[
                ["جدة", "Jeddah"],
                ["الرياض", "Riyadh"],
                ["مكة المكرمة", "Makkah"],
            ],
            grid_size=None,
            zoom_level=None,
            input_file_path=input_path_mx,
            version=max_version_str,
            data_dir=data_dir,
        )

        # Process all cities for this version
        for city in geo_intelligence.cities:
            print(f"Calculating for {', '.join(city)} using {version_str}")
            try:
                geo_intelligence.calculate_city_scores_task_1(city)
            except Exception as e:
                print(f"Error calculating scores for {city[-1]}: {str(e)}")
                continue

        # Save the grid data to CSV
        geo_intelligence.save_grids_to_csv(output_dir_mx)
    
        # Create and save the geojson output
        try:
            grids = pd.concat(
                [
                    v.reset_index(drop=True)
                    for v in geo_intelligence.grids.values()
                ]
            )
            population = geo_intelligence.population_grid.dropna().reset_index(drop=True)
            joined = gpd.sjoin(population, grids, how="left", predicate="within")

            # Save geojson to the version-specific directory
            joined.drop("index_right", axis=1).to_file(output_geojson_mx, driver="GeoJSON")
            print(f"Saved geojson: {output_geojson_mx}")
        except Exception as e:
            print(f"Error creating geojson for {max_version_str}: {str(e)}")

        print(f"Successfully completed processing for {max_version_str}")

    output_geojson = os.path.join(output_dir, "all_features.json")
    if not os.path.isfile(output_geojson):
        output_mx = gpd.read_file(output_geojson_mx)
        population_data = gpd.GeoDataFrame.from_features(pd.read_json(input_path).features)
        # output = adapt(output_mx, population_data)
        
        output_geojson = os.path.join(output_dir, "all_features.json")
        output.to_file(output_geojson, driver="GeoJSON")
        print(f"Saved geojson: {output_geojson}")
    else:
        print("Already exists")
    