import os
import numpy as np
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry import box
from scipy.spatial import cKDTree

import logging
from sklearn.model_selection import RepeatedKFold
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_absolute_error, r2_score

from sklearn.model_selection import RepeatedKFold
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import (
    RandomForestRegressor,
    StackingRegressor,
)
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
import joblib

import os
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from typing import Tuple, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _load_or_cache_from_database(
    database_connection_key: str, sql_query: str, cache_filename: str
) -> pd.DataFrame:
    """
    Load data from cache if available, otherwise fetch from database and cache it.
    
    This implements a simple caching strategy to avoid repeated expensive database queries.
    The cache is stored as CSV files for quick loading and data persistence.
    
    Example scenario:
    - First call: Fetches 100,000 real estate listings from database (takes 30 seconds)
    - Subsequent calls: Loads from cache file (takes 0.5 seconds)
    """
    logger = logging.getLogger(__name__)
    cache_filepath = f"cache/{cache_filename}"
    
    # Check if cached data exists to avoid expensive database queries
    if os.path.isfile(cache_filepath):
        logger.info(f"Loading cached data from {cache_filepath}")
        df = pd.read_csv(cache_filepath)
        logger.info(f"Loaded {len(df)} rows from cache. Shape: {df.shape}")
        return df
    
    # If no cache exists, fetch from database
    logger.info(f"Cache not found. Fetching data from database...")
    logger.debug(f"SQL Query: {sql_query[:100]}...")  # Log first 100 chars of query
    
    database_engine = create_engine(database_connection_key)
    dataframe = pd.read_sql(sql_query, database_engine)
    
    logger.info(f"Fetched {len(dataframe)} rows from database. Shape: {dataframe.shape}")
    logger.info(f"Columns retrieved: {list(dataframe.columns)}")
    
    # Cache the data for future use
    dataframe.to_csv(cache_filepath, index=False)
    logger.info(f"Cached data to {cache_filepath} for future use")
    
    return dataframe


def _load_csv_with_coordinate_renaming(
    city_code: str, dataset_type: str
) -> pd.DataFrame:
    """
    Load CSV file and rename lat/lng columns to latitude/longitude for consistency.
    
    This standardization is crucial for geospatial operations as different data sources
    use different naming conventions (lat/lng, latitude/longitude, y/x, etc.)
    
    Example scenario:
    - Input: DataFrame with columns ['name', 'lat', 'lng', 'rating']
    - Output: DataFrame with columns ['name', 'latitude', 'longitude', 'rating']
    """
    logger = logging.getLogger(__name__)
    
    # Different dataset types have different file naming patterns
    filename = (
        f"cache/{dataset_type}_{city_code}_full.csv"
        if dataset_type == "restaurants"
        else f"cache/{city_code}_{dataset_type}.csv"
    )
    
    logger.info(f"Loading {dataset_type} data for {city_code} from {filename}")
    
    dataframe = pd.read_csv(filename)
    initial_shape = dataframe.shape
    
    # Standardize coordinate column names across all datasets
    dataframe = dataframe.rename(columns={"lat": "latitude", "lng": "longitude"})
    
    logger.info(f"Loaded {len(dataframe)} {dataset_type} records. Shape: {initial_shape}")
    logger.info(f"Coordinate columns renamed: lat→latitude, lng→longitude")
    
    # Log sample coordinates to verify data integrity
    if len(dataframe) > 0:
        sample_lat = dataframe['latitude'].iloc[0]
        sample_lon = dataframe['longitude'].iloc[0]
        logger.debug(f"Sample coordinate: ({sample_lat}, {sample_lon})")
    
    return dataframe


def _load_geojson_with_crs(geojson_filename: str) -> gpd.GeoDataFrame:
    """
    Load GeoJSON file and ensure proper Coordinate Reference System (CRS) is set.
    
    CRS is critical for accurate geospatial calculations. EPSG:4326 is WGS84,
    the standard lat/lon coordinate system used by GPS and most web mapping.
    
    Example scenario:
    - Input: GeoJSON with undefined CRS
    - Output: GeoDataFrame with EPSG:4326 (WGS84) projection
    - This ensures distance calculations are accurate (e.g., 1 degree ≈ 111km at equator)
    """
    logger = logging.getLogger(__name__)
    
    filepath = f"cache/{geojson_filename}"
    logger.info(f"Loading GeoJSON from {filepath}")
    
    geodataframe = gpd.read_file(filepath)
    initial_crs = geodataframe.crs
    
    logger.info(f"Loaded {len(geodataframe)} features. Initial CRS: {initial_crs}")
    
    # Ensure CRS is set to WGS84 (EPSG:4326) for compatibility
    # This is the standard geographic coordinate system
    geodataframe = geodataframe.set_crs(epsg=4326).to_crs(epsg=4326)
    
    logger.info(f"Set CRS to EPSG:4326 (WGS84). Geometry types: {geodataframe.geometry.type.value_counts().to_dict()}")
    
    # Log bounds to understand spatial extent
    bounds = geodataframe.total_bounds  # [minx, miny, maxx, maxy]
    logger.debug(f"Spatial extent: minx={bounds[0]:.4f}, miny={bounds[1]:.4f}, maxx={bounds[2]:.4f}, maxy={bounds[3]:.4f}")
    
    return geodataframe


def load_data(database_connection_key: str, city_names: List[str]) -> Tuple[
    pd.DataFrame,  # real_estate_listings
    pd.DataFrame,  # housing_statistics
    gpd.GeoDataFrame,  # population_features
    pd.DataFrame,  # restaurant_locations
    pd.DataFrame,  # royal_house_locations
    pd.DataFrame,  # luxury_hotel_locations
    pd.DataFrame,  # gym_locations
    pd.DataFrame,  # luxurious_area_locations
    gpd.GeoDataFrame,  # dental_clinic_locations
    gpd.GeoDataFrame,  # electrician_service_locations
    gpd.GeoDataFrame,  # plumber_service_locations
    gpd.GeoDataFrame,  # police_station_locations
    gpd.GeoDataFrame,  # embassy_locations
    gpd.GeoDataFrame,  # university_locations
]:
    """
    Load all required datasets for real estate analysis.
    
    This function orchestrates loading of diverse geospatial and demographic data
    that will be used as features for income prediction. The variety of data sources
    provides rich features for the machine learning model.

    Args:
        database_connection_key: Database connection string
        city_names: List of city names (last element used as city code)

    Returns:
        Tuple of all loaded datasets
        
    Example scenario:
    - Input: city_names=['Al Riyadh', 'Riyadh', 'riyadh']
    - Output: 14 datasets with locations and attributes for real estate analysis
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Starting data load for cities: {city_names}")
    
    # Create cache directory
    os.makedirs("cache", exist_ok=True)
    logger.info("Cache directory ensured")

    # Extract city code from the last city name
    # This handles different naming conventions (e.g., 'Al-Riyadh' vs 'Riyadh')
    city_code = city_names[-1].lower()
    logger.info(f"Using city code: {city_code}")

    # Load database-backed datasets with caching
    logger.info("Loading real estate listings...")
    real_estate_listings = _load_or_cache_from_database(
        database_connection_key,
        """
        SELECT url, price, latitude, longitude, category_ar, category_id, 
               city, city_id, title, address, rent_period, category, price_description
        FROM raw_schema_marketplace.saudi_real_estate;
        """,
        "real_estate_data.csv",
    )
    logger.info(f"Real estate data: {len(real_estate_listings)} listings, avg price: {real_estate_listings['price'].mean():.2f}")

    logger.info("Loading housing statistics...")
    housing_statistics = _load_or_cache_from_database(
        database_connection_key,
        """
        SELECT "Location", "Selector", "Degree", "TotalDwellings", "ResidentialDwellings", 
               "OwnedDwellings", "RentedDwellings", "ProvidedDwellings", "OtherResidentialDwellings", 
               "Non-ResidentialDwellings", "PublicHousing", "WorkCamps", "CommercialDwellings", 
               "OtherDwellings", "ZoomLevel", "TopLeftDegree", "BottomRightDegree", "ID", "Parent"
        FROM raw_schema_marketplace.housing;
        """,
        "housing_data.csv",
    )
    logger.info(f"Housing data: {len(housing_statistics)} records, total dwellings: {housing_statistics['TotalDwellings'].sum():,}")

    # Load population data from JSON
    # Level 14 provides age and gender demographics at a granular spatial resolution
    logger.info("Loading population features at zoom level 14...")
    population_features = gpd.GeoDataFrame.from_features(
        pd.read_json(r"cron_jobs\aquire_data\saudi_census\population\population_json_files\v14\all_features.geojson").features
    )
    logger.info(f"Population data: {len(population_features)} grid cells")

    # Load Point of Interest (POI) datasets
    # These provide socioeconomic indicators based on nearby amenities
    logger.info("Loading POI datasets...")
    
    # Restaurants indicate commercial activity and foot traffic
    restaurant_locations = _load_csv_with_coordinate_renaming(city_code, "restaurants")
    
    # Royal houses and luxury hotels indicate high-income areas
    royal_house_locations = _load_csv_with_coordinate_renaming(city_code, "royal_houses")
    luxury_hotel_locations = _load_csv_with_coordinate_renaming(city_code, "luxury hotel")
    
    # Gyms indicate health-conscious, potentially higher-income demographics
    gym_locations = _load_csv_with_coordinate_renaming(city_code, "gym")
    
    # Luxurious areas are direct indicators of wealth concentration
    luxurious_area_locations = _load_csv_with_coordinate_renaming(city_code, "luxurious_areas")

    # Load service and infrastructure GeoJSON datasets
    # These indicate urban development and service quality
    logger.info("Loading infrastructure datasets...")
    
    # Healthcare and services indicate developed neighborhoods
    dental_clinic_locations = _load_geojson_with_crs("geojson_saudi_dental_clinic_20250512_110022.geojson")
    electrician_service_locations = _load_geojson_with_crs("geojson_saudi_electrician_20250512_122401.geojson")
    plumber_service_locations = _load_geojson_with_crs("geojson_saudi_plumber_20250512_123014.geojson")
    
    # Security and diplomatic presence indicate safe, developed areas
    police_station_locations = _load_geojson_with_crs("geojson_saudi_police_20250512_103953.geojson")
    embassy_locations = _load_geojson_with_crs("geojson_saudi_embassy_20250512_102151.geojson")
    
    # Universities indicate educated demographics and student housing demand
    university_locations = _load_geojson_with_crs("geojson_saudi_university_20250512_011237.geojson")

    logger.info("All datasets loaded successfully")
    logger.info(f"Total POIs loaded: {len(restaurant_locations) + len(gym_locations) + len(luxury_hotel_locations)} amenities")

    return (
        real_estate_listings,
        housing_statistics,
        population_features,
        restaurant_locations,
        royal_house_locations,
        luxury_hotel_locations,
        gym_locations,
        luxurious_area_locations,
        dental_clinic_locations,
        electrician_service_locations,
        plumber_service_locations,
        police_station_locations,
        embassy_locations,
        university_locations,
    )


def get_geodataframes(
    real_estate_data,
    housing_data,
    population_data,
    restaurants_data,
    royal_houses,
    luxury_hotels,
    gyms,
    luxurious_areas,
    dental_clinic,
    electrician,
    plumber,
    police,
    embassy,
    university,
    city,
    is_training=True,
):
    """
    Convert raw data to GeoDataFrames and prepare for spatial analysis.
    
    This function performs critical data transformations:
    1. Converts point data to geometric objects
    2. Standardizes coordinate reference systems
    3. Extracts features from categorical data
    4. Filters data to city boundaries
    
    The grid_size parameter changes based on training vs prediction to balance
    computational efficiency with spatial resolution.
    
    Example scenarios:
    - Training mode: grid_size = 0.01° (≈1.1km at equator)
    - Prediction mode: adaptive grid based on population cell size
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Converting to GeoDataFrames for city: {city}, training mode: {is_training}")
    
    # Determine grid cell size for spatial aggregation
    if is_training:
        # Fixed small grid for detailed training
        grid_size = 0.01  # Approximately 1.1km x 1.1km at equator
        logger.info(f"Training mode: Using fixed grid size of {grid_size}° (≈{grid_size * 111:.1f}km)")
    else:
        # Adaptive grid based on population data resolution
        # The 2.5x multiplier creates coarser grids for faster prediction
        grid_size = np.round((population_data.geometry.area.max()) ** 0.5, 5) * 2.5
        logger.info(f"Prediction mode: Adaptive grid size of {grid_size}° based on population cell size")

    # Extract population centroids and prepare tabular data
    # Centroids represent the center point of each population grid cell
    points = population_data.geometry.map(lambda x: x.centroid)
    population_data["longitude"] = points.map(lambda x: x.x)
    population_data["latitude"] = points.map(lambda x: x.y)
    
    # Convert to regular DataFrame and standardize column names
    population_data = pd.DataFrame(
        population_data.drop("geometry", axis=1)
    ).rename(columns={"PCNT": "TotalPopulation", "GLEVEL": "zoom_level"})
    
    logger.info(f"Population data: {len(population_data)} cells, total population: {population_data['TotalPopulation'].sum():,}")

    # Extract building type and trade type from category string
    # Example: "villa_for_sale" → building_type="villa", trade_type="sale"
    x = real_estate_data.category.str.split("_for_")
    real_estate_data["building_type"] = x.map(lambda x: x[0])
    real_estate_data["trade_type"] = x.map(lambda x: x[1])
    
    # Log distribution of property types
    building_types = real_estate_data["building_type"].value_counts()
    logger.info(f"Property types: {building_types.to_dict()}")

    # Clean location names by removing inconsistent hyphens
    # Example: "Al-Riyadh" → "Riyadh" for consistency
    housing_data["Location"] = housing_data.Location.str.split("-").map(lambda x: x[-1])

    # Filter real estate data to specified cities
    initial_count = len(real_estate_data)
    real_estate_data = real_estate_data.loc[real_estate_data.city.isin(city)]
    logger.info(f"Filtered real estate data from {initial_count} to {len(real_estate_data)} listings for cities: {city}")

    # Convert to GeoDataFrame with point geometries
    real_estate_data = (
        gpd.GeoDataFrame(
            real_estate_data,
            geometry=gpd.points_from_xy(
                real_estate_data.longitude, real_estate_data.latitude
            ),
        )
        .set_crs(epsg=4326)  # WGS84 coordinate system
        .to_crs(epsg=4326)
    )

    # Create derived features for machine learning
    real_estate_data = real_estate_data.assign(
        # Binary feature for villa properties (typically more expensive)
        is_villa=lambda df: df.building_type == "villa",
        
        # Binary feature for apartments (different market segment)
        is_apartment=lambda df: df.building_type == "apartment",
        
        # Binary feature for above-median price (luxury indicator)
        is_above_average=lambda df: df.price > df.price.median(),
        
        # Separate features for sales vs rentals (different price scales)
        selling_price=lambda df: np.where(
            df.trade_type == "sale", df.price, np.nan
        ),
        
        # Normalize rental prices to monthly rate
        # Example: 12,000 SAR/year → 1,000 SAR/month
        renting_price=lambda df: np.where(
            df.trade_type == "rent", df.price / df.rent_period, np.nan
        ),
    )
    
    median_price = real_estate_data.price.median()
    logger.info(f"Real estate features created. Median price: {median_price:,.0f} SAR")
    logger.info(f"Villa percentage: {real_estate_data.is_villa.mean()*100:.1f}%")

    # Prepare census data - keep only essential columns
    population_data = population_data[["TotalPopulation", "longitude", "latitude"]]
    population_data = (
        gpd.GeoDataFrame(
            population_data,
            geometry=gpd.points_from_xy(
                population_data.longitude, population_data.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Prepare housing data with coordinate extraction
    # The Degree field contains "longitude latitude" as a string
    housing_data = housing_data.loc[housing_data.Location == city[-1]]
    degree_split = housing_data.Degree.str.split(" ")
    housing_data = housing_data.assign(
        latitude=degree_split.map(lambda x: float(x[1])),
        longitude=degree_split.map(lambda x: float(x[0])),
    )[["latitude", "longitude", "TotalDwellings"]]
    
    housing_data = (
        gpd.GeoDataFrame(
            housing_data,
            geometry=gpd.points_from_xy(
                housing_data.longitude, housing_data.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )
    
    logger.info(f"Housing data: {len(housing_data)} records, total dwellings: {housing_data['TotalDwellings'].sum():,}")

    # Prepare restaurant data with ratings as quality indicator
    restaurants_data = (
        gpd.GeoDataFrame(
            restaurants_data[["rating", "longitude", "latitude"]],
            geometry=gpd.points_from_xy(
                restaurants_data.longitude, restaurants_data.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )
    
    avg_rating = restaurants_data["rating"].mean()
    logger.info(f"Restaurant data: {len(restaurants_data)} locations, average rating: {avg_rating:.2f}")

    # Prepare luxury indicator datasets
    # These POIs serve as proxies for neighborhood affluence
    
    # Royal houses - direct indicator of ultra-high income areas
    royal_houses = royal_houses[["name", "longitude", "latitude"]]
    royal_houses = (
        gpd.GeoDataFrame(
            royal_houses,
            geometry=gpd.points_from_xy(
                royal_houses.longitude, royal_houses.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )
    logger.info(f"Royal properties: {len(royal_houses)} locations")

    # Luxury hotels - indicate tourist areas and business districts
    luxury_hotels = luxury_hotels[["name", "longitude", "latitude"]]
    luxury_hotels = (
        gpd.GeoDataFrame(
            luxury_hotels,
            geometry=gpd.points_from_xy(
                luxury_hotels.longitude, luxury_hotels.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Gyms - proxy for health-conscious, middle-to-upper income demographics
    gyms = gyms[["name", "longitude", "latitude"]]
    gyms = (
        gpd.GeoDataFrame(
            gyms, geometry=gpd.points_from_xy(gyms.longitude, gyms.latitude)
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Luxurious areas - curated list of high-end neighborhoods
    luxurious_areas = luxurious_areas[["name", "longitude", "latitude"]]
    luxurious_areas = (
        gpd.GeoDataFrame(
            luxurious_areas,
            geometry=gpd.points_from_xy(
                luxurious_areas.longitude, luxurious_areas.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Calculate city boundaries using convex hull of all real estate points
    # Convex hull creates the smallest polygon containing all points
    city_boundaries = real_estate_data.union_all().convex_hull
    bounds = city_boundaries.bounds  # (minx, miny, maxx, maxy)
    logger.info(f"City boundaries calculated: {bounds}")

    # Filter all datasets to city boundaries to remove outliers
    # This ensures all data is within the area of interest
    initial_counts = {
        "real_estate": len(real_estate_data),
        "population": len(population_data),
        "restaurants": len(restaurants_data)
    }
    
    real_estate_data = real_estate_data.loc[real_estate_data.within(city_boundaries)]
    population_data = population_data.loc[population_data.within(city_boundaries)]
    restaurants_data = restaurants_data.loc[restaurants_data.within(city_boundaries)]
    housing_data = housing_data.loc[housing_data.within(city_boundaries)]
    royal_houses = royal_houses.loc[royal_houses.within(city_boundaries)]
    luxurious_areas = luxurious_areas.loc[luxurious_areas.within(city_boundaries)]
    gyms = gyms.loc[gyms.within(city_boundaries)]
    luxurious_areas = luxurious_areas.loc[luxurious_areas.within(city_boundaries)]
    dental_clinic = dental_clinic.loc[dental_clinic.within(city_boundaries)]
    electrician = electrician.loc[electrician.within(city_boundaries)]
    plumber = plumber.loc[plumber.within(city_boundaries)]
    police = police.loc[police.within(city_boundaries)]
    embassy = embassy.loc[embassy.within(city_boundaries)]
    university = university.loc[university.within(city_boundaries)]

    # Log filtering results
    for name, initial in initial_counts.items():
        if name == "real_estate":
            final = len(real_estate_data)
        elif name == "population":
            final = len(population_data)
        else:
            final = len(restaurants_data)
        logger.info(f"{name}: filtered from {initial} to {final} records ({final/initial*100:.1f}% retained)")

    return (
        real_estate_data,
        housing_data,
        population_data,
        restaurants_data,
        royal_houses,
        luxury_hotels,
        gyms,
        luxurious_areas,
        dental_clinic,
        electrician,
        plumber,
        police,
        embassy,
        university,
        grid_size,
    )


def make_grids(
    real_estate_data,
    housing_data,
    population_data,
    restaurants_data,
    royal_houses,
    luxury_hotels,
    gyms,
    luxurious_areas,
    dental_clinic,
    electrician,
    plumber,
    police,
    embassy,
    university,
    grid_size,
):
    """
    Create spatial grid cells and aggregate all features within each cell.
    
    This is the core spatial aggregation function that creates a regular grid
    over the city and counts/averages features within each grid cell. This
    converts point data into area-based features suitable for ML models.
    
    The grid-based approach allows us to:
    1. Handle varying data densities uniformly
    2. Create neighborhood-level features from point data
    3. Smooth out individual property variations
    
    Example scenario for a 0.01° grid cell (≈1.1km²):
    - Input: 50 properties, 10 restaurants, 2 gyms within cell
    - Output: Cell with avg_price=500k, restaurant_count=10, gym_count=2
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Creating spatial grid with cell size: {grid_size}° (≈{grid_size * 111:.1f}km)")
    
    # Calculate total spatial extent from population data
    minx, miny, maxx, maxy = population_data.total_bounds
    logger.info(f"Spatial extent: lon=[{minx:.4f}, {maxx:.4f}], lat=[{miny:.4f}, {maxy:.4f}]")
    
    # Create regular grid of square cells covering the entire area
    # Each cell is a box with sides of length grid_size degrees
    grid_cells = [
        box(x, y, x + grid_size, y + grid_size)
        for x in np.arange(minx, maxx, grid_size)
        for y in np.arange(miny, maxy, grid_size)
    ]
    
    # Calculate grid dimensions for logging
    n_cols = len(np.arange(minx, maxx, grid_size))
    n_rows = len(np.arange(miny, maxy, grid_size))
    logger.info(f"Created {len(grid_cells)} grid cells ({n_cols} columns × {n_rows} rows)")
    
    grid = gpd.GeoDataFrame(geometry=grid_cells, crs=population_data.crs)

    # Perform spatial joins to assign each point to its containing grid cell
    # This is computationally intensive but enables efficient aggregation
    logger.info("Performing spatial joins...")
    
    # Join population data - demographic base layer
    joined_population = gpd.sjoin(
        population_data, grid, how="inner", predicate="within"
    )
    logger.info(f"Population join: {len(joined_population)} points assigned to grid cells")
    
    # Join real estate data - primary target variable source
    joined_real_estate = gpd.sjoin(
        real_estate_data, grid, how="inner", predicate="within"
    )
    logger.info(f"Real estate join: {len(joined_real_estate)} properties assigned to grid cells")
    
    # Join POI data - socioeconomic indicators
    joined_restaurants = gpd.sjoin(
        restaurants_data, grid, how="inner", predicate="within"
    )
    joined_housing = gpd.sjoin(
        housing_data, grid, how="inner", predicate="within"
    )
    joined_royal_houses = gpd.sjoin(
        royal_houses, grid, how="inner", predicate="within"
    )
    joined_luxury_hotels = gpd.sjoin(
        luxury_hotels, grid, how="inner", predicate="within"
    )
    joined_gyms = gpd.sjoin(gyms, grid, how="inner", predicate="within")
    joined_luxurious_areas = gpd.sjoin(
        luxurious_areas, grid, how="inner", predicate="within"
    )

    # Join infrastructure data - urban development indicators
    joined_dental_clinic = gpd.sjoin(
        dental_clinic, grid, how="inner", predicate="within"
    )
    joined_electrician = gpd.sjoin(
        electrician, grid, how="inner", predicate="within"
    )
    joined_plumber = gpd.sjoin(plumber, grid, how="inner", predicate="within")
    joined_police = gpd.sjoin(police, grid, how="inner", predicate="within")
    joined_embassy = gpd.sjoin(embassy, grid, how="inner", predicate="within")
    joined_university = gpd.sjoin(
        university, grid, how="inner", predicate="within"
    )

    logger.info("Aggregating features by grid cell...")
    
    # Aggregate data into grid cells using appropriate statistics
    # Population: sum (total people in cell)
    # Prices: mean (average property value)
    # Counts: sum (total number of features)
    grid = pd.concat(
        [
            grid,
            # Demographic features
            joined_population.groupby("index_right")["TotalPopulation"].sum(),
            
            # Real estate price features (mean for representative values)
            joined_real_estate.groupby("index_right")["selling_price"].mean(),
            joined_real_estate.groupby("index_right")["renting_price"].mean(),
            
            # Property type counts (indicators of neighborhood character)
            joined_real_estate.groupby("index_right")["is_villa"]
            .sum()
            .rename("villa_count"),
            joined_real_estate.groupby("index_right")["is_apartment"]
            .sum()
            .rename("apartment_count"),
            
            # Luxury indicator (properties above median price)
            joined_real_estate.groupby("index_right")["is_above_average"]
            .sum()
            .rename("number_of_properties_above_average_price"),
            
            # Commercial activity indicator
            joined_restaurants.groupby("index_right")["rating"]
            .count()
            .rename("restaurant_count"),
            
            # Housing density
            joined_housing.groupby("index_right")["TotalDwellings"].sum(),
            
            # Luxury POI counts (direct wealth indicators)
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
            
            # Service availability (urban development indicators)
            joined_dental_clinic.groupby("index_right")["name"]
            .count()
            .rename("joined_dental_clinic"),
            joined_electrician.groupby("index_right")["name"]
            .count()
            .rename("joined_electrician"),
            joined_plumber.groupby("index_right")["name"]
            .count()
            .rename("joined_plumber"),
            
            # Institutional presence (stability/development indicators)
            joined_police.groupby("index_right")["name"]
            .count()
            .rename("joined_police"),
            joined_embassy.groupby("index_right")["name"]
            .count()
            .rename("joined_embassy"),
            joined_university.groupby("index_right")["name"]
            .count()
            .rename("joined_university"),
        ],
        axis=1,
    )

    # Calculate derived features
    # Villa ratio: Indicates neighborhood character (0=all apartments, 1=all villas)
    # This ratio often correlates with income levels
    grid["villa_to_apartment_ratio"] = grid["villa_count"] / (
        grid["villa_count"] + grid["apartment_count"]
    )
    
    # Log summary statistics
    populated_cells = grid[~grid["TotalPopulation"].isna()]
    logger.info(f"Grid statistics:")
    logger.info(f"  - Populated cells: {len(populated_cells)} / {len(grid)} ({len(populated_cells)/len(grid)*100:.1f}%)")
    logger.info(f"  - Avg population per cell: {populated_cells['TotalPopulation'].mean():.0f}")
    logger.info(f"  - Avg selling price: {populated_cells['selling_price'].mean():,.0f} SAR")
    logger.info(f"  - Cells with restaurants: {(populated_cells['restaurant_count'] > 0).sum()}")
    logger.info(f"  - Cells with gyms: {(populated_cells['gym_count'] > 0).sum()}")
    
    # Example output for a typical grid cell:
    # Cell 1234: population=2500, selling_price=450000, restaurants=3, gyms=1, villa_ratio=0.7
    # This indicates a moderately populated, mixed residential area with good amenities
    
    return grid


def idw_interpolation(xy_points, values, xy_targets, k=6, power=2):
    """
    Inverse Distance Weighting (IDW) interpolation for spatial data.
    
    IDW is a deterministic spatial interpolation method that estimates unknown values
    at target locations based on known values at nearby points. The core principle:
    closer points have more influence than distant points.
    
    Mathematical formula:
    Z(x₀) = Σᵢ(wᵢ × zᵢ) / Σᵢ(wᵢ)
    where wᵢ = 1 / dᵢᵖ (weight inversely proportional to distance)
    
    Parameters:
    - xy_points: Known data locations (e.g., income survey points)
    - values: Known values at those points (e.g., average income)
    - xy_targets: Locations where we want to estimate values
    - k: Number of nearest neighbors to consider (default 6)
    - power: Distance decay parameter (default 2 for inverse square)
    
    Example scenario:
    - Input: 100 income measurements scattered across city
    - Target: 1000 grid cells needing income estimates
    - Output: Smoothly interpolated income values respecting spatial patterns
    
    Example values:
    - Point A: income=50,000 SAR, distance=0.5km → weight=4.0
    - Point B: income=30,000 SAR, distance=1.0km → weight=1.0
    - Result: (50000×4 + 30000×1) / (4+1) = 46,000 SAR
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Starting IDW interpolation: {len(xy_points)} known points → {len(xy_targets)} targets")
    logger.info(f"IDW parameters: k={k} neighbors, power={power}")
    
    # Build spatial index for efficient nearest neighbor queries
    # cKDTree creates a balanced k-dimensional tree for O(log n) searches
    tree = cKDTree(xy_points)
    
    # Find k nearest neighbors for each target point
    # Returns distances and indices of nearest points
    dists, idxs = tree.query(xy_targets, k=k)
    
    # Log distance statistics to understand spatial coverage
    mean_dist = np.mean(dists[:, 0])  # Mean distance to nearest neighbor
    max_dist = np.max(dists[:, -1])   # Max distance to kth neighbor
    logger.info(f"Nearest neighbor distances: mean={mean_dist:.4f}°, max k-th={max_dist:.4f}°")
    logger.info(f"In kilometers: mean={mean_dist*111:.1f}km, max k-th={max_dist*111:.1f}km")
    
    # Prevent division by zero for coincident points
    # Add small epsilon (1e-12) to zero distances
    dists = np.maximum(dists, 1e-12)
    
    # Calculate IDW weights: w = 1 / d^power
    # Higher power = sharper decay, more local influence
    # Power=1: linear decay, Power=2: quadratic decay (default)
    weights = 1 / (dists**power)
    
    # Normalize weights so they sum to 1 for each target
    # This ensures interpolated values stay within reasonable range
    weights /= weights.sum(axis=1, keepdims=True)
    
    # Calculate weighted average of neighboring values
    # Matrix multiplication: values[idxs] gets neighbor values
    # Element-wise multiplication with weights, then sum
    interpolated = np.sum(values[idxs] * weights, axis=1)
    
    # Log interpolation results
    logger.info(f"Interpolation complete:")
    logger.info(f"  - Input range: [{np.min(values):,.0f}, {np.max(values):,.0f}]")
    logger.info(f"  - Output range: [{np.min(interpolated):,.0f}, {np.max(interpolated):,.0f}]")
    logger.info(f"  - Mean change: {np.mean(np.abs(interpolated - np.mean(values))):,.0f}")
    
    # Quality check: large changes might indicate sparse data
    if max_dist * 111 > 5:  # If using neighbors >5km away
        logger.warning(f"Some interpolations use distant neighbors (>{max_dist*111:.1f}km) - results may be less reliable")
    
    return interpolated


def get_dataset(db_access_key, city):
    """
    Main dataset preparation function that orchestrates the entire data pipeline.
    
    This function:
    1. Loads all data sources
    2. Converts to spatial format
    3. Creates grid-based features
    4. Interpolates income data using IDW
    5. Adds distance features
    
    The income interpolation is crucial because actual income data is sparse
    but needed as the target variable for the ML model.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Starting dataset preparation for city: {city}")
    
    # Load all data sources
    all_data = load_data(db_access_key, city)
    logger.info("Data loading complete")

    # Convert to GeoDataFrames and filter to city
    all_data = get_geodataframes(*all_data, city)
    logger.info("GeoDataFrame conversion complete")

    # Create spatial grid and aggregate features
    grid = make_grids(*all_data)
    
    # Filter out cells without population (empty areas)
    mask = ~grid["TotalPopulation"].isna()
    initial_cells = len(grid)
    grid = grid.loc[mask]
    logger.info(f"Filtered grid: {initial_cells} → {len(grid)} cells (removed {initial_cells - len(grid)} empty cells)")

    # Load income survey data (sparse ground truth)
    logger.info("Loading income survey data...")
    income_data = gpd.GeoDataFrame.from_features(
        pd.read_json("cache/ignore_zad_Output_data.json").features
    )
    logger.info(f"Income survey data: {len(income_data)} points")

    # Create boundary from populated grid cells
    bounds = (
        grid[["geometry", "TotalPopulation"]].dropna().union_all().convex_hull
    )
    
    # Filter income data to city bounds
    mask = income_data[["geometry", "Average Male Income"]].within(bounds)
    income_data = income_data.loc[mask][["geometry", "Average Male Income"]]
    logger.info(f"Income data after filtering: {len(income_data)} points within city")

    # Filter grid to areas with income data coverage
    bounds = income_data.union_all().convex_hull
    mask = grid.within(bounds)
    grid = grid.loc[mask]
    logger.info(f"Grid cells within income data coverage: {len(grid)}")

    # Prepare for IDW interpolation
    # Convert income polygons to centroids for point-based interpolation
    income_data = income_data[["geometry", "Average Male Income"]].assign(
        geometry=lambda x: x.geometry.centroid
    )
    
    # Remove any remaining cells without population
    mask = ~grid[["geometry", "TotalPopulation"]].isna().any(axis=1)
    grid = grid.loc[mask]

    # Extract coordinates for interpolation
    # Source points: income survey locations
    xy_points = np.array([(point.x, point.y) for point in income_data.geometry])
    values = income_data["Average Male Income"].values
    
    # Target points: grid cell centroids
    xy_targets = np.array(
        [(poly.centroid.x, poly.centroid.y) for poly in grid.geometry]
    )
    
    logger.info(f"IDW interpolation: {len(xy_points)} income points → {len(xy_targets)} grid cells")
    
    # Perform IDW interpolation to estimate income for all grid cells
    interpolated_values = idw_interpolation(
        xy_points, values, xy_targets, k=6, power=2
    )
    
    # Add interpolated income to grid
    grid["income"] = interpolated_values
    
    # Log income statistics
    logger.info(f"Income statistics after interpolation:")
    logger.info(f"  - Mean: {grid['income'].mean():,.0f} SAR")
    logger.info(f"  - Median: {grid['income'].median():,.0f} SAR")
    logger.info(f"  - Std Dev: {grid['income'].std():,.0f} SAR")
    logger.info(f"  - Range: [{grid['income'].min():,.0f}, {grid['income'].max():,.0f}] SAR")

    # Create final GeoDataFrame with proper CRS
    income_data = gpd.GeoDataFrame(grid.reset_index(drop=True)).set_crs(
        epsg=4326
    )

    # Remove any cells where interpolation failed
    mask = ~income_data.income.isna()
    income_data = income_data.loc[mask]
    logger.info(f"Final dataset: {len(income_data)} grid cells with complete features")

    # Calculate distance from city center
    # Distance from CBD often correlates with property values and income
    city_center = income_data.union_all().convex_hull.centroid
    
    # Euclidean distance in degrees (will be scaled by ML model)
    income_data["euc_distance_from_center"] = income_data.geometry.map(
        lambda x: x.centroid.distance(city_center)
    )
    
    # Log distance statistics
    mean_dist = income_data["euc_distance_from_center"].mean()
    logger.info(f"Distance from center: mean={mean_dist:.4f}° (≈{mean_dist*111:.1f}km)")
    
    # Example final record:
    # Grid cell with: population=2500, restaurants=3, selling_price=450k,
    # income=65k (interpolated), distance_from_center=0.05° (5.5km)
    
    return income_data


def train_model(income_data):
    """
    Train ensemble model for income prediction using grid-based features.
    
    This function implements a sophisticated ensemble approach:
    1. Uses multiple base learners (XGBoost, CatBoost, RandomForest)
    2. Performs k-fold cross-validation for robust evaluation
    3. Creates a stacking ensemble for final predictions
    
    The ensemble approach combines strengths of different algorithms:
    - XGBoost: Gradient boosting, handles non-linear patterns well
    - CatBoost: Optimized for categorical features, robust to overfitting
    - RandomForest: Captures feature interactions, provides stability
    
    Example performance metrics:
    - MAE: 15,000 SAR (typical prediction error)
    - R²: 0.75 (explains 75% of income variance)
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger()
    logger.info("Starting model training pipeline...")
    
    # Prepare features and target
    X = income_data.drop("geometry", axis=1).sort_index(axis=1).fillna(0.0)
    logger.info(f"Feature matrix shape: {X.shape}")
    logger.info(f"Features: {list(X.columns)}")
    
    # Extract and prepare target variable (income)
    y = X.pop("income").copy()
    
    # Handle zero/negative incomes by imputing with mean
    # This prevents issues with log transforms and maintains data integrity
    mask = y > 0
    zero_income_count = (~mask).sum()
    if zero_income_count > 0:
        y.loc[~mask] = y.loc[mask].mean()
        logger.warning(f"Imputed {zero_income_count} zero/negative income values with mean: {y.loc[mask].mean():,.0f}")
    
    # Log target statistics
    logger.info(f"Target variable (income) statistics:")
    logger.info(f"  - Mean: {y.mean():,.0f} SAR")
    logger.info(f"  - Std Dev: {y.std():,.0f} SAR")
    logger.info(f"  - Range: [{y.min():,.0f}, {y.max():,.0f}] SAR")
    
    # Use RobustScaler for feature normalization
    # RobustScaler uses median/IQR instead of mean/std, making it robust to outliers
    scaler = RobustScaler().fit(X.values)
    logger.info("Fitted RobustScaler on features")

    # Configure cross-validation
    # RepeatedKFold provides more stable estimates than single k-fold
    kf = RepeatedKFold(n_splits=5, n_repeats=10, random_state=42)
    logger.info(f"Cross-validation: 5-fold × 10 repeats = 50 train/test splits")
    
    # Hyperparameters tuned for this specific problem
    n_estimators = 350  # Number of trees/boosting rounds
    depth = 8          # Tree depth (controls complexity)
    lr = 0.05         # Learning rate (controls boosting speed)
    
    logger.info(f"Model hyperparameters: n_estimators={n_estimators}, depth={depth}, lr={lr}")

    # Initialize base learners with tuned hyperparameters
    base_learners = {
        "xgb": XGBRegressor(
            objective="reg:squarederror",  # Squared error for regression
            learning_rate=lr,
            max_depth=depth,
            n_estimators=n_estimators,
            subsample=0.85,  # Row subsampling to prevent overfitting
            colsample_bytree=0.85,  # Column subsampling
            gamma=0.25,  # Minimum loss reduction for split
            reg_alpha=0.35,  # L1 regularization
            reg_lambda=0.65,  # L2 regularization
            tree_method="hist",  # Fast histogram-based algorithm
            verbosity=0,
        ),
        "cat": CatBoostRegressor(
            iterations=n_estimators,
            learning_rate=lr,
            depth=depth,
            l2_leaf_reg=6.5,  # L2 regularization
            subsample=0.85,
            verbose=0,
            random_seed=42,
        ),
        "rf": RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=None,  # No depth limit for RF
            min_samples_split=3,  # Minimum samples to split node
            bootstrap=True,  # Bootstrap sampling
            random_state=42,
        ),
    }

    # Initialize metrics storage
    metrics = {
        m: {"train_mae": [], "val_mae": [], "train_r2": [], "val_r2": []}
        for m in base_learners
    }

    # Create models directory
    os.makedirs("models", exist_ok=True)

    # Cross-validation loop
    for fold, (train_idx, val_idx) in enumerate(kf.split(X), start=1):
        logger.info(f"=== Fold {fold} ===")
        
        # Split data
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        logger.info(f"Train size: {len(X_train)}, Validation size: {len(X_val)}")

        # Scale features
        X_train_s = scaler.transform(X_train.values)
        X_val_s = scaler.transform(X_val.values)

        # Train and evaluate each base learner
        for name, model in base_learners.items():
            # Create fresh instance to avoid data leakage
            mdl = model.__class__(**model.get_params())
            
            # Train model
            mdl.fit(X_train_s, y_train.values)
            
            # Make predictions
            y_train_pred = mdl.predict(X_train_s)
            y_val_pred = mdl.predict(X_val_s)

            # Calculate metrics
            t_mae = mean_absolute_error(y_train, y_train_pred)
            v_mae = mean_absolute_error(y_val, y_val_pred)
            t_r2 = r2_score(y_train, y_train_pred)
            v_r2 = r2_score(y_val, y_val_pred)

            # Store metrics
            metrics[name]["train_mae"].append(t_mae)
            metrics[name]["val_mae"].append(v_mae)
            metrics[name]["train_r2"].append(t_r2)
            metrics[name]["val_r2"].append(v_r2)

            # Log performance
            logger.info(
                f"{name.upper():<5}  Train MAE: {t_mae:,.0f} SAR, R²: {t_r2:.3f} | "
                f"Val MAE: {v_mae:,.0f} SAR, R²: {v_r2:.3f}"
            )
            
            # Save model
            joblib.dump(mdl, f"models/{name}_fold{fold}.joblib")
            
        logger.info("")

    # Log cross-validation summary
    logger.info("=== CV Summary ===")
    for name in base_learners:
        mean_train_mae = np.mean(metrics[name]['train_mae'])
        mean_val_mae = np.mean(metrics[name]['val_mae'])
        mean_val_r2 = np.mean(metrics[name]['val_r2'])
        std_val_mae = np.std(metrics[name]['val_mae'])
        
        logger.info(
            f"{name.upper():<5} Mean Train MAE: {mean_train_mae:,.0f} SAR, "
            f"Mean Val MAE: {mean_val_mae:,.0f} ± {std_val_mae:,.0f} SAR, "
            f"Mean Val R²: {mean_val_r2:.3f}"
        )
        
        # Interpretation of metrics
        logger.info(f"  → On average, {name} predictions are off by {mean_val_mae:,.0f} SAR")
        logger.info(f"  → Model explains {mean_val_r2*100:.1f}% of income variance")

    # Train stacking ensemble on full dataset
    logger.info("\nTraining stacking ensemble on full dataset...")
    
    # Scale full dataset
    X_full_s = scaler.transform(X)
    
    # Create stacking regressor
    # This combines predictions from all base models using linear regression
    estimators = [(name, base_learners[name]) for name in base_learners]
    stack = StackingRegressor(
        estimators=estimators,
        final_estimator=LinearRegression(),  # Linear combination of base predictions
        passthrough=True,  # Include original features in final estimator
        n_jobs=-1,  # Parallel processing
    )
    
    # Train ensemble
    stack.fit(X_full_s, y)
    
    # Make final predictions for logging
    final_pred = stack.predict(X_full_s)
    final_mae = mean_absolute_error(y, final_pred)
    final_r2 = r2_score(y, final_pred)
    
    logger.info(f"Ensemble performance on full data:")
    logger.info(f"  - MAE: {final_mae:,.0f} SAR")
    logger.info(f"  - R²: {final_r2:.3f}")
    
    # Save ensemble model
    joblib.dump(stack, "models/stacking_ensemble.joblib")
    logger.info("Ensemble saved as models/stacking_ensemble.joblib")
    
    # Save scaler for prediction phase
    joblib.dump(scaler, "models/scaler.joblib")
    logger.info("Scaler saved as models/scaler.joblib")

    return metrics, base_learners, stack


def get_saved_models():
    """
    Load saved models from the 'models' directory.
    
    This function loads all saved model files, which includes:
    - Individual fold models (e.g., xgb_fold1.joblib)
    - The stacking ensemble model
    - The fitted scaler
    
    Using multiple models allows for uncertainty estimation through
    prediction variance.
    """
    logger = logging.getLogger(__name__)
    logger.info("Loading saved models...")
    
    models = []
    model_files = []
    
    for path in os.listdir("models"):
        if path.endswith(".joblib"):
            full_path = os.path.join("models", path)
            
            try:
                with open(full_path, "rb") as f:
                    model = joblib.load(f)
                    models.append(model)
                    model_files.append(path)
                    
            except Exception as e:
                logger.error(f"Failed to load {path}: {e}")
    
    logger.info(f"Loaded {len(models)} models:")
    for f in model_files:
        logger.info(f"  - {f}")
    
    # Log model types
    model_types = {}
    for model in models:
        model_type = type(model).__name__
        model_types[model_type] = model_types.get(model_type, 0) + 1
    
    logger.info(f"Model types: {model_types}")
    
    return models


def predict_income(income_data, models):
    """
    Predict income using the loaded models.
    
    This function:
    1. Prepares features in the same way as training
    2. Applies the same scaling transformation
    3. Gets predictions from all models
    4. Averages predictions for robustness
    
    The averaging of multiple models provides:
    - More stable predictions
    - Implicit uncertainty quantification
    - Reduced overfitting risk
    
    Example:
    - Model 1 predicts: 65,000 SAR
    - Model 2 predicts: 63,000 SAR  
    - Model 3 predicts: 67,000 SAR
    - Final prediction: 65,000 SAR (average)
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting income prediction...")
    
    # Prepare features (same as training)
    X = income_data.drop("geometry", axis=1).sort_index(axis=1).fillna(0.0)
    logger.info(f"Prediction feature matrix shape: {X.shape}")
    
    # Apply same scaling as training
    scaler = RobustScaler().fit(X)
    X_scaled = scaler.transform(X.values)
    
    logger.info(f"Making predictions with {len(models)} models...")
    
    # Collect predictions from all models
    predictions = []
    for i, model in enumerate(models):
        pred = model.predict(X_scaled)
        predictions.append(pred.squeeze())
        
        # Log each model's predictions
        logger.debug(f"Model {i}: mean={np.mean(pred):,.0f}, std={np.std(pred):,.0f}")

    # Stack predictions and calculate ensemble average
    predictions_array = np.stack(predictions, axis=0)
    
    # Calculate prediction statistics
    y_mean = np.mean(predictions_array, axis=0)
    y_std = np.std(predictions_array, axis=0)
    
    logger.info(f"Ensemble predictions:")
    logger.info(f"  - Mean income: {np.mean(y_mean):,.0f} SAR")
    logger.info(f"  - Std income: {np.mean(y_std):,.0f} SAR")
    logger.info(f"  - Income range: [{np.min(y_mean):,.0f}, {np.max(y_mean):,.0f}] SAR")
    logger.info(f"  - Average uncertainty (std): {np.mean(y_std):,.0f} SAR")
    
    # High uncertainty areas might need more data collection
    high_uncertainty_cells = (y_std > np.percentile(y_std, 90)).sum()
    logger.info(f"High uncertainty cells (top 10%): {high_uncertainty_cells}")
    
    return y_mean


def get_predicted_income(db_access_key, city, dir=""):
    """
    Main prediction pipeline that generates income predictions for a city.
    
    This function:
    1. Loads and prepares data (without target variable)
    2. Creates prediction grid at appropriate resolution
    3. Loads trained models
    4. Makes predictions
    5. Saves results as GeoJSON for visualization
    
    The two-pass approach (fine grid → coarse grid) allows for:
    - Detailed predictions where data is dense
    - Computational efficiency for large areas
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Starting income prediction pipeline for {city}")
    
    # Load all data sources
    data_ = load_data(db_access_key, city)

    # First pass: Create detailed features for prediction
    logger.info("Creating fine-grained feature grid...")
    data = get_geodataframes(*data_, city)
    grid = make_grids(*data)
    
    # Filter populated areas
    mask = ~grid["TotalPopulation"].isna()
    grid = grid.loc[mask]
    logger.info(f"Fine grid: {len(grid)} populated cells")

    # Prepare spatial data
    income_data = grid.set_crs(epsg=4326).to_crs(epsg=4326)
    
    # Calculate city center for distance feature
    city_center = income_data.union_all().convex_hull.centroid
    income_data["euc_distance_from_center"] = (
        income_data.geometry.centroid.distance(city_center)
    )
    
    # Log feature statistics
    logger.info("Feature statistics:")
    for col in ['TotalPopulation', 'restaurant_count', 'selling_price']:
        if col in income_data.columns:
            mean_val = income_data[col].mean()
            logger.info(f"  - {col}: mean={mean_val:.2f}")

    # Load models and make predictions
    models = get_saved_models()
    y = predict_income(income_data, models)
    income_data["income"] = y

    # Second pass: Create coarser grid for final output
    # This reduces file size and smooths predictions
    logger.info("Creating output grid at coarser resolution...")
    data = get_geodataframes(*data_, city, is_training=False)
    grid = make_grids(*data)
    mask = ~grid["TotalPopulation"].isna()
    grid = grid.loc[mask]
    logger.info(f"Output grid: {len(grid)} cells")

    # Aggregate predictions to coarser grid
    # Spatial join followed by averaging
    income_data = (
        gpd.sjoin(
            grid,
            income_data[["geometry", "income", "euc_distance_from_center"]],
            how="inner",
            predicate=None,  # Default: intersects
        )
        .groupby(by="geometry", observed=False)
        .mean()
        .reset_index()
        .drop("index_right", axis=1)
    )

    # Create final GeoDataFrame
    income_data = gpd.GeoDataFrame(income_data)
    
    # Save results as GeoJSON for GIS visualization
    output_path = os.path.join(dir, "income_data.geojson")
    income_data.set_crs(epsg=4326).to_crs(epsg=4326).to_file(
        output_path, driver="GeoJSON"
    )
    
    logger.info(f"Saved predictions to {output_path}")
    logger.info(f"Output contains {len(income_data)} grid cells with income predictions")
    
    # Log summary statistics for validation
    logger.info("Prediction summary:")
    logger.info(f"  - Mean predicted income: {income_data['income'].mean():,.0f} SAR")
    logger.info(f"  - Income range: [{income_data['income'].min():,.0f}, {income_data['income'].max():,.0f}] SAR")
    logger.info(f"  - Spatial coverage: {income_data.union_all().area * 111 * 111:.1f} km²")

    return income_data


def adapt(finner_data, coarser_grid):
    """
    Adapt fine-resolution data to a coarser grid through spatial aggregation.
    
    This function is useful for:
    1. Matching different data resolutions
    2. Reducing computational load
    3. Creating summary statistics at neighborhood/district level
    
    The aggregation preserves the mean values, which is appropriate
    for intensive properties like income (as opposed to extensive
    properties like population which would need sums).
    
    Example:
    - Input: 1000 cells at 100m resolution
    - Output: 100 cells at 1km resolution
    - Each output cell contains averaged values from ~10 input cells
    """
    logger = logging.getLogger(__name__)
    logger.info("Adapting fine data to coarse grid...")
    logger.info(f"Input: {len(finner_data)} fine cells → {len(coarser_grid)} coarse cells")
    
    # Ensure consistent CRS
    finner_data = finner_data.set_crs(epsg=4326).to_crs(epsg=4326)
    coarser_grid = coarser_grid.set_crs(epsg=4326).to_crs(epsg=4326)
    
    # Spatial join: find which fine cells fall within each coarse cell
    # 'right' join ensures we keep all coarse cells
    merged = gpd.sjoin(
        finner_data,
        coarser_grid,
        how="right",
        predicate=None,  # Default: intersects
    )
    
    # Count matches for logging
    matches_per_cell = merged.groupby('geometry').size()
    logger.info(f"Fine cells per coarse cell: mean={matches_per_cell.mean():.1f}, max={matches_per_cell.max()}")
    
    # Aggregate by taking mean of all fine cells within each coarse cell
    merged = (
        merged
        .groupby(by="geometry", observed=False)
        .mean()  # Mean preserves intensive properties
        .reset_index()
    )

    # Select relevant columns
    merged = gpd.GeoDataFrame(merged)[
        [
            "geometry",
            "income",
            "euc_distance_from_center",
            "x_distance_from_center",
            "y_distance_from_center",
        ]
    ]

    # Final spatial join to get coarse grid structure
    merged = gpd.sjoin(
        coarser_grid.set_crs(epsg=4326).to_crs(epsg=4326),
        merged,
        how="inner",
        predicate="within",
    ).drop("index_right", axis=1)
    
    logger.info(f"Adaptation complete: {len(merged)} cells with aggregated data")
    
    # Log aggregation effects
    if 'income' in merged.columns and 'income' in finner_data.columns:
        orig_mean = finner_data['income'].mean()
        new_mean = merged['income'].mean()
        logger.info(f"Income preservation: original mean={orig_mean:,.0f}, aggregated mean={new_mean:,.0f}")
        logger.info(f"Relative change: {abs(new_mean - orig_mean) / orig_mean * 100:.1f}%")

    return merged