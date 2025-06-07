import logging
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import box
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as ctx
from sqlalchemy import create_engine
from bidi.algorithm import get_display
import arabic_reshaper

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeoIntelligence:
    """
    A comprehensive geospatial intelligence class for analyzing real estate markets in Saudi cities.

    This class combines multiple data sources (real estate, census, housing, amenities) to create
    grid-based scoring systems for two different analysis tasks:
    - Task 1: Luxury/high-value property analysis
    - Task 2: Market activity and property mix analysis

    Mathematical Approach:
    - Creates spatial grids overlaying city boundaries
    - Performs spatial joins to aggregate point data into grid cells
    - Applies weighted scoring algorithms with normalization
    - Uses convex hull for city boundary approximation
    """

    def __init__(
        self,
        db_access_key,
        cities,
        grid_size=0.05,  # Grid cell size in degrees (~5.5km at equator)
        zoom_level=6,  # Census data zoom level for detail control
    ):
        """
        Initialize the GeoIntelligence system with database connection and spatial parameters.

        Args:
            db_access_key: Database connection string
            cities: List of city tuples/lists (expects city[-1] to be the city name)
            grid_size: Spatial grid resolution in decimal degrees
            zoom_level: Census data resolution level

        Mathematical Logic:
        - Grid size determines spatial resolution of analysis
        - Smaller grid_size = higher resolution but more computation
        - Zoom level controls census data granularity
        """
        logger.info(
            f"Initializing GeoIntelligence for cities: {[city[-1] for city in cities]}"
        )

        self.cities = cities
        self.grid_size = grid_size
        self.zoom_level = zoom_level

        # Database connection and data loading
        logger.info("Establishing database connection...")
        engine = create_engine(db_access_key)

        # Load real estate data - core property listings with prices, locations, types
        logger.info("Loading real estate data from database...")
        self.real_estate_data = pd.read_sql(
            """
                  SELECT url, price, latitude, longitude, category_ar, category_id, city, city_id, title, address, rent_period, category, price_description
                  FROM raw_schema_marketplace.saudi_real_estate;
              """,
            engine,
        )
        logger.info(f"Loaded {len(self.real_estate_data)} real estate records")

        # Load census data - population demographics and statistics
        logger.info(f"Loading census data with zoom level {zoom_level}...")
        self.census_data = pd.read_sql(
            f"""
        SELECT "HouseholdAverageSize", "HouseholdMedianSize", "ZoomLevel", "MalePopulation", "FemalePopulation", "MedianAgeMale", "MedianAgeFemale", "TotalPopulation", "PopulationDensity", longitude, latitude
        FROM raw_schema_marketplace.saudi_census {f'WHERE "ZoomLevel" = {zoom_level}' if zoom_level is not None else ''};
              """,
            engine,
        )
        logger.info(f"Loaded {len(self.census_data)} census records")

        # Parse real estate categories to extract building and trade types
        # Expected format: "villa_for_sale", "apartment_for_rent"
        logger.info("Parsing real estate categories...")
        x = self.real_estate_data.category.str.split("_for_")
        self.real_estate_data["building_type"] = x.map(
            lambda x: x[0] if len(x) > 0 else "unknown"
        )
        self.real_estate_data["trade_type"] = x.map(
            lambda x: x[1] if len(x) > 1 else "unknown"
        )
        logger.info(
            f"Found building types: {self.real_estate_data.building_type.unique()}"
        )
        logger.info(
            f"Found trade types: {self.real_estate_data.trade_type.unique()}"
        )

        # Load housing data - dwelling statistics and housing types
        logger.info(f"Loading housing data with zoom level {zoom_level}...")
        self.housing_data = pd.read_sql(
            f"""
        SELECT "Location", "Selector", "Degree", "TotalDwellings", "ResidentialDwellings", "OwnedDwellings", "RentedDwellings", "ProvidedDwellings", "OtherResidentialDwellings", "Non-ResidentialDwellings", "PublicHousing", "WorkCamps", "CommercialDwellings", "OtherDwellings", "ZoomLevel", "TopLeftDegree", "BottomRightDegree", "ID", "Parent"
        FROM raw_schema_marketplace.housing {f'WHERE "ZoomLevel" = {zoom_level}' if zoom_level is not None else ''};
              """,
            engine,
        )

        # Parse location names (remove prefix parts, keep city name)
        # Expected format: "Region-Province-City"
        x = self.housing_data.Location.str.split("-").map(
            lambda x: x[-1] if len(x) > 0 else "unknown"
        )
        self.housing_data["Location"] = x
        logger.info(
            f"Processed housing data for locations: {self.housing_data.Location.unique()}"
        )

        # Load city-specific amenity data from CSV files
        # Each city has separate CSV files for different amenity types
        logger.info("Loading city-specific amenity data from CSV files...")
        self.city_data = {}
        for city in cities:
            city_name = city[-1]
            logger.info(f"Loading amenity data for {city_name}...")

            try:
                self.city_data[city_name] = {
                    # Restaurant data with ratings and locations
                    "google_data": pd.read_csv(
                        f"restaurants_{city_name.lower()}_full.csv"
                    ).rename(columns={"lat": "latitude", "lng": "longitude"}),
                    # High-end residential properties
                    "royal_houses": pd.read_csv(
                        f"{city_name.lower()}_royal_houses.csv"
                    ).rename(columns={"lat": "latitude", "lng": "longitude"}),
                    # Luxury hospitality venues
                    "luxury_hotels": pd.read_csv(
                        f"{city_name.lower()}_luxury hotel.csv"
                    ).rename(columns={"lat": "latitude", "lng": "longitude"}),
                    # Fitness and wellness facilities
                    "gyms": pd.read_csv(f"{city_name.lower()}_gym.csv").rename(
                        columns={"lat": "latitude", "lng": "longitude"}
                    ),
                    # Upscale neighborhoods and districts
                    "luxurious_areas": pd.read_csv(
                        f"{city_name.lower()}_luxurious_areas.csv"
                    ).rename(columns={"lat": "latitude", "lng": "longitude"}),
                }
                logger.info(f"Successfully loaded amenity data for {city_name}")
            except FileNotFoundError as e:
                logger.warning(
                    f"Could not load some amenity data for {city_name}: {e}"
                )

        # Calculate city boundaries using convex hull of real estate points
        # Mathematical approach: convex hull creates minimum bounding polygon
        logger.info("Calculating city boundaries using convex hull method...")
        self.city_boundaries = {}
        for city in cities:
            city_name = city[-1]
            logger.info(f"Creating boundary for {city_name}...")

            # Filter real estate data for current city
            x1 = self.real_estate_data.loc[
                self.real_estate_data.city.isin(city)
            ][["latitude", "longitude", "building_type", "price"]]

            # Create GeoDataFrame from coordinates
            x1 = gpd.GeoDataFrame(
                x1, geometry=gpd.points_from_xy(x1.longitude, x1.latitude)
            )

            # Calculate convex hull - minimum polygon containing all points
            # This approximates city boundary based on property distribution
            self.city_boundaries[city_name] = x1.unary_union.convex_hull
            logger.info(
                f"Created boundary for {city_name} from {len(x1)} property points"
            )

        # Utility functions
        # Normalization function: scales values to 0-1 range for comparable scoring
        # Formula: (x - min(x)) / (max(x) - min(x))
        self.norm = lambda x: (x - x.min()) / (x.max() - x.min())

        # Storage for computed grids
        self.grids = {"task_1": {}, "task_2": {}}

        # Color maps for visualization
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

        logger.info("GeoIntelligence initialization complete")

    def plot_city_map(self, city):
        """
        Display interactive map centered on city boundary.

        Mathematical approach:
        - Uses city boundary bounds to calculate center point
        - Centers map on geometric centroid of city area
        """
        logger.info(f"Creating interactive map for {city[-1]}...")

        # Calculate city center from boundary bounds
        west, south, east, north = self.city_boundaries[city[-1]].bounds
        coords = [
            (north + south) / 2.0,
            (west + east) / 2.0,
        ]  # Centroid calculation

        # Create Folium map
        m = folium.Map(location=coords, zoom_start=10, tiles="CartoDB positron")
        logger.info(f"Map created centered at {coords}")

    def calculate_city_scores_task_1(self, city):
        """
        TASK 1: Luxury Property Investment Analysis

        Mathematical Model:
        This function creates a comprehensive scoring system for identifying premium investment zones
        by combining real estate values, demographics, and luxury amenities.

        Core Algorithm:
        1. Spatial Grid Creation: Divides city into regular grid cells for uniform analysis
        2. Multi-source Data Integration: Joins 8 different data sources spatially
        3. Weighted Scoring System: Applies domain-specific weights to create composite indices
        4. Consistency Validation: Cross-validates scores against manual luxury area ratings

        Scoring Formula:
        - Real Estate Index (40%): 0.33×price_avg + 0.33×villa_ratio + 0.33×royal_properties
        - Population Index (30%): 0.6×population_density + 0.4×age_profile
        - Amenity Index (30%): 0.3×restaurants + 0.3×dwellings + 0.3×luxury_hotels + 0.1×gyms
        - Final Score: base_score × (1 + consistency_score^0.2)

        Expected Use Cases:
        - Luxury real estate investment targeting
        - High-net-worth client residential recommendations
        - Premium development site selection
        - Wealth concentration mapping
        """
        logger.info(
            f"Starting Task 1 (Luxury Analysis) calculation for {city[-1]}..."
        )

        # Get the city boundary for spatial filtering
        city_boundary = self.city_boundaries[city[-1]]
        logger.info(
            f"Using city boundary with area: {city_boundary.area:.6f} square degrees"
        )

        # STEP 1: Prepare real estate data with luxury indicators
        logger.info("Processing real estate data for luxury indicators...")
        sale_properties = self.real_estate_data.loc[
            self.real_estate_data.city.isin(city)
        ].assign(
            # Luxury building type indicators
            is_villa=lambda df: df.building_type
            == "villa",  # Villas typically indicate wealth
            is_apartment=lambda df: df.building_type == "apartment",
            # Price premium indicators
            is_above_average=lambda df: df.price
            > df.price.median(),  # Above-median pricing
            # Separate sale and rental markets
            selling_price=lambda df: np.where(
                df.trade_type == "sale", df.price, np.nan
            ),
            renting_price=lambda df: np.where(
                df.trade_type == "rent", df.price / df.rent_period, np.nan
            ),  # Normalize to monthly
        )

        # Convert to GeoDataFrame for spatial operations
        sale_properties_gdf = gpd.GeoDataFrame(
            sale_properties,
            geometry=gpd.points_from_xy(
                sale_properties.longitude, sale_properties.latitude
            ),
        )
        logger.info(f"Processed {len(sale_properties_gdf)} real estate records")

        # STEP 2: Prepare census data with demographic indicators
        logger.info("Processing census data for demographic analysis...")
        census_data = self.census_data.assign(
            # Average age calculation (weighted by gender)
            age=lambda df: df.MedianAgeMale * 0.5
            + df.MedianAgeFemale * 0.5  # Simple average
        )[["TotalPopulation", "age", "longitude", "latitude"]]

        census_gdf = gpd.GeoDataFrame(
            census_data,
            geometry=gpd.points_from_xy(
                census_data.longitude, census_data.latitude
            ),
        )
        logger.info(f"Processed {len(census_gdf)} census records")

        # STEP 3: Prepare amenity datasets
        # Each amenity type contributes to luxury scoring differently

        # Restaurant data (dining quality indicator)
        restaurants = self.city_data[city[-1]]["google_data"][
            ["rating", "longitude", "latitude"]
        ]
        restaurants_gdf = gpd.GeoDataFrame(
            restaurants,
            geometry=gpd.points_from_xy(
                restaurants.longitude, restaurants.latitude
            ),
        )
        logger.info(f"Loaded {len(restaurants_gdf)} restaurant locations")

        # Housing diversity data
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

        # Luxury amenity datasets
        royal_houses = self.city_data[city[-1]]["royal_houses"][
            ["name", "longitude", "latitude"]
        ]
        royal_houses_gdf = gpd.GeoDataFrame(
            royal_houses,
            geometry=gpd.points_from_xy(
                royal_houses.longitude, royal_houses.latitude
            ),
        )
        logger.info(f"Loaded {len(royal_houses_gdf)} royal house locations")

        luxury_hotels = self.city_data[city[-1]]["luxury_hotels"][
            ["name", "longitude", "latitude"]
        ]
        luxury_hotels_gdf = gpd.GeoDataFrame(
            luxury_hotels,
            geometry=gpd.points_from_xy(
                luxury_hotels.longitude, luxury_hotels.latitude
            ),
        )
        logger.info(f"Loaded {len(luxury_hotels_gdf)} luxury hotel locations")

        gyms = self.city_data[city[-1]]["gyms"][
            ["name", "longitude", "latitude"]
        ]
        gyms_gdf = gpd.GeoDataFrame(
            gyms, geometry=gpd.points_from_xy(gyms.longitude, gyms.latitude)
        )

        luxurious_areas = self.city_data[city[-1]]["luxurious_areas"][
            ["name", "longitude", "latitude"]
        ]
        luxurious_areas_gdf = gpd.GeoDataFrame(
            luxurious_areas,
            geometry=gpd.points_from_xy(
                luxurious_areas.longitude, luxurious_areas.latitude
            ),
        )
        logger.info(
            f"Loaded {len(luxurious_areas_gdf)} known luxury area markers"
        )

        # STEP 4: Spatial filtering - keep only data within city boundaries
        logger.info("Applying spatial filters to city boundaries...")
        initial_counts = {
            "properties": len(sale_properties_gdf),
            "census": len(census_gdf),
            "restaurants": len(restaurants_gdf),
        }

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

        final_counts = {
            "properties": len(sale_properties_gdf),
            "census": len(census_gdf),
            "restaurants": len(restaurants_gdf),
        }
        logger.info(
            f"Spatial filtering results: {final_counts} (from {initial_counts})"
        )

        # STEP 5: Create spatial grid system
        # Grid approach allows systematic analysis across city area
        logger.info(
            f"Creating spatial grid with cell size {self.grid_size} degrees..."
        )
        minx, miny, maxx, maxy = census_gdf.total_bounds
        logger.info(
            f"City bounds: ({minx:.4f}, {miny:.4f}) to ({maxx:.4f}, {maxy:.4f})"
        )

        # Generate regular grid cells
        grid_cells = [
            box(x, y, x + self.grid_size, y + self.grid_size)
            for x in np.arange(minx, maxx, self.grid_size)
            for y in np.arange(miny, maxy, self.grid_size)
        ]
        grid = gpd.GeoDataFrame(geometry=grid_cells, crs=census_gdf.crs)
        logger.info(f"Created {len(grid)} grid cells for analysis")

        # STEP 6: Spatial joins - aggregate point data into grid cells (continued)
        logger.info(
            "Performing spatial joins to aggregate data into grid cells..."
        )

        # Each spatial join aggregates point data into the grid system
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

        logger.info(
            "Spatial joins completed - aggregating data by grid cell..."
        )

        # STEP 7: Aggregate data into the grid
        # This is the core data aggregation step - combines all data sources into unified grid
        logger.info(
            "Aggregating multi-source data into unified grid structure..."
        )

        grid = pd.concat(
            [
                grid,
                # Population metrics (demographic indicators)
                joined_population.groupby("index_right")[
                    "TotalPopulation"
                ].sum(),  # Population density per cell
                joined_population.groupby("index_right")[
                    "age"
                ].mean(),  # Average age profile
                # Real estate price indicators (market value signals)
                joined_real_estate.groupby("index_right")[
                    "selling_price"
                ].mean(),  # Average sale prices
                joined_real_estate.groupby("index_right")[
                    "renting_price"
                ].mean(),  # Average rental rates
                # Property type indicators (luxury building types)
                joined_real_estate.groupby("index_right")["is_villa"]
                .sum()
                .rename("villa_count"),  # Villa concentration
                joined_real_estate.groupby("index_right")["is_apartment"]
                .sum()
                .rename("apartment_count"),  # Apartment density
                joined_real_estate.groupby("index_right")["is_above_average"]
                .sum()
                .rename(
                    "number_of_properties_above_average_price"
                ),  # Premium pricing
                # Amenity indicators (lifestyle and convenience factors)
                joined_restaurants.groupby("index_right")["rating"]
                .count()
                .rename("restaurant_count"),  # Restaurant density
                joined_housing.groupby("index_right")[
                    "TotalDwellings"
                ].sum(),  # Housing supply
                # Luxury indicators (high-end amenity concentration)
                joined_royal_houses.groupby("index_right")["name"]
                .count()
                .rename("royal_property_count"),  # Royal/premium properties
                joined_luxury_hotels.groupby("index_right")["name"]
                .count()
                .rename("luxury_hotel_count"),  # Luxury hospitality
                joined_gyms.groupby("index_right")["name"]
                .count()
                .rename("gym_count"),  # Fitness facilities
                joined_luxurious_areas.groupby("index_right")["name"]
                .count()
                .rename("luxury_area_count"),  # Known luxury districts
            ],
            axis=1,
        )

        logger.info(
            f"Grid aggregation completed - {len(grid.columns)} features per cell"
        )

        # STEP 8: Calculate villa-to-apartment ratio (luxury indicator)
        # Higher ratios indicate more exclusive/luxury-oriented areas
        # Mathematical logic: villa_count / (villa_count + apartment_count)
        grid = grid.assign(
            villa_to_apartment_ratio=lambda df: df.villa_count
            / (df.villa_count + df.apartment_count)
        )
        logger.info("Calculated villa-to-apartment ratios as luxury indicator")

        # Create backup before scoring calculations
        grid_backup = grid.copy(deep=True)

        # STEP 9: Create composite scoring indices
        logger.info("Calculating composite luxury scoring indices...")

        # Identify cells with no data (for later masking)
        mask = grid.iloc[:, 1:].isna().all(axis=1)
        logger.info(f"Found {mask.sum()} empty grid cells (will be masked)")

        # Fill NaN values with 0 for calculations
        grid = grid.fillna(0.0)

        # TASK 1 SCORING ALGORITHM:
        grid = grid.assign(
            # Real Estate Index (40% weight in final score)
            # Combines price signals, property types, and luxury properties
            # Formula: 0.33×(avg_prices) + 0.33×villa_ratio + 0.33×royal_properties
            real_estate_index=lambda df: (
                0.33
                * (
                    (self.norm(df.selling_price) + self.norm(df.renting_price))
                    / 2.0
                )  # Average normalized prices
                + 0.33
                * df.villa_to_apartment_ratio  # Villa concentration (luxury indicator)
                + 0.33
                * self.norm(
                    df.royal_property_count
                )  # Royal/premium property presence
            ),
            # Population Index (30% weight in final score)
            # Balances population density with age demographics
            # Formula: 0.6×population_density + 0.4×age_profile
            population_index=lambda df: (
                0.6
                * self.norm(
                    df.TotalPopulation
                )  # Population density (activity level)
                + 0.4
                * self.norm(
                    df.age
                )  # Age profile (maturity/stability indicator)
            ),
            # Amenity Index (30% weight in final score)
            # Comprehensive lifestyle and convenience scoring
            # Formula: 0.3×restaurants + 0.3×housing + 0.3×luxury_hotels + 0.1×gyms
            amenity_index=lambda df: (
                0.3 * self.norm(df.restaurant_count)  # Dining options
                + 0.3 * self.norm(df.TotalDwellings)  # Housing availability
                + 0.3 * self.norm(df.luxury_hotel_count)  # Luxury hospitality
                + 0.1 * self.norm(df.gym_count)  # Fitness facilities
            ),
        )

        logger.info("Composite indices calculated - computing base scores...")

        # Calculate base score (weighted combination of indices)
        # Mathematical Model: 40% real estate + 30% population + 30% amenities
        grid = grid.assign(
            base_score=lambda df: (
                0.4
                * df.real_estate_index  # Real estate dominates (investment focus)
                + 0.3 * df.population_index  # Demographics matter
                + 0.3 * df.amenity_index  # Lifestyle factors
            ),
            # Manual rating for validation (known luxury areas)
            manual_rating=lambda df: self.norm(df.luxury_area_count),
        )

        logger.info(
            "Base scores calculated - applying consistency validation..."
        )

        # STEP 10: Consistency validation and final scoring
        # Cross-validates algorithmic scores against manual luxury area ratings
        # This ensures the model aligns with domain expert knowledge
        grid = grid.assign(
            # Consistency Score: measures alignment between base_score and manual ratings
            # Higher consistency = better model-expert agreement
            # Formula: max_deviation - |base_score - manual_rating|
            consistency_score=lambda df: (
                (df.base_score - df.manual_rating).abs().max()
                - (df.base_score - df.manual_rating).abs()
            ),
            # Final Score: base score enhanced by consistency
            # Formula: base_score × (1 + consistency_score^0.2)
            # The power of 0.2 provides gentle boost (not too aggressive)
            final_score=lambda df: df.base_score
            * (1 + df.consistency_score**0.2),
        )

        logger.info("Final luxury scores calculated")

        # STEP 11: Finalize results
        # Combine original grid with calculated scores
        grid = pd.concat(
            [grid_backup, grid.iloc[:, -7:]], axis=1
        )  # Last 7 columns are the calculated scores

        # Sort by base score for ranking
        grid = grid.sort_values(by="base_score", ascending=False)

        # Apply mask to remove empty cells (restore NaN for visualization)
        grid.loc[mask, grid.columns[1:]] = np.nan

        # Store results
        self.grids["task_1"][city[-1]] = grid.copy(deep=True)

        logger.info(
            f"Task 1 calculation completed for {city[-1]} - stored {len(grid)} grid cells"
        )
        logger.info(
            f"Score distribution - Mean: {grid.base_score.mean():.3f}, Std: {grid.base_score.std():.3f}"
        )

    def calculate_city_scores_task_2(self, city):
        """
        TASK 2: Real Estate Market Activity Analysis

        Mathematical Model:
        This function analyzes real estate market dynamics, focusing on market liquidity,
        property diversity, and housing market health indicators.

        Core Algorithm:
        1. Market Activity Index: Trading volume, price levels, rental market strength
        2. Property Mix Index: Diversity of property types and development patterns
        3. Occupancy Index: Ownership vs rental ratios, public housing presence
        4. Population Index: Demographic factors affecting housing demand

        Scoring Formula:
        - Market Activity (30%): 0.4×listing_volume + 0.3×price_levels + 0.3×rental_activity
        - Property Mix (30%): 0.4×residential_density + 0.3×commercial_presence + 0.3×diversity
        - Occupancy Index (20%): 0.5×ownership_ratio + 0.5×public_housing_ratio
        - Population Index (20%): 0.4×population + 0.3×household_size + 0.3×age

        Expected Use Cases:
        - Real estate market health assessment
        - Investment opportunity identification
        - Development planning and zoning analysis
        - Market liquidity evaluation
        """
        logger.info(
            f"Starting Task 2 (Market Activity Analysis) calculation for {city[-1]}..."
        )

        # Get the city boundary for spatial filtering
        city_boundary = self.city_boundaries[city[-1]]
        logger.info(f"Using city boundary for market analysis")

        # STEP 1: Prepare real estate market data
        logger.info(
            "Processing real estate data for market activity analysis..."
        )
        real_estate_data = self.real_estate_data.loc[
            self.real_estate_data.city.isin(city)
        ].assign(
            # Separate market segments for analysis
            selling_price=lambda df: np.where(
                df.trade_type == "sale", df.price, np.nan
            ),
            renting_price=lambda df: np.where(
                df.trade_type == "rent", df.price / df.rent_period, np.nan
            ),  # Monthly rental rates
        )
        real_estate_gdf = gpd.GeoDataFrame(
            real_estate_data,
            geometry=gpd.points_from_xy(
                real_estate_data.longitude, real_estate_data.latitude
            ),
        )
        logger.info(
            f"Processed {len(real_estate_gdf)} real estate records for market analysis"
        )

        # STEP 2: Prepare enhanced census data
        logger.info("Processing census data with demographic indicators...")
        census_data = self.census_data.assign(
            # Average age calculation (demographic indicator)
            age=lambda df: df.MedianAgeMale * 0.5
            + df.MedianAgeFemale * 0.5
        )
        census_gdf = gpd.GeoDataFrame(
            census_data,
            geometry=gpd.points_from_xy(
                census_data.longitude, census_data.latitude
            ),
        )
        logger.info(f"Enhanced census data with {len(census_gdf)} records")

        # STEP 3: Prepare housing market data with diversity indicators
        logger.info(
            "Processing housing data for market composition analysis..."
        )
        housing_data = self.housing_data.loc[
            self.housing_data.Location == city[-1]
        ]
        degree_split = housing_data.Degree.str.split(" ")
        housing_data = housing_data.assign(
            latitude=degree_split.map(lambda x: float(x[1])),
            longitude=degree_split.map(lambda x: float(x[0])),
        )
        housing_gdf = gpd.GeoDataFrame(
            housing_data,
            geometry=gpd.points_from_xy(
                housing_data.longitude, housing_data.latitude
            ),
        )
        logger.info(f"Processed {len(housing_gdf)} housing market records")

        # STEP 4: Apply spatial filtering
        logger.info("Applying spatial filters for market boundary...")
        real_estate_gdf = real_estate_gdf.loc[
            real_estate_gdf.within(city_boundary)
        ]
        census_gdf = census_gdf.loc[census_gdf.within(city_boundary)]
        housing_gdf = housing_gdf.loc[housing_gdf.within(city_boundary)]

        logger.info(
            f"Spatial filtering complete - retained {len(real_estate_gdf)} properties, {len(census_gdf)} census points"
        )

        # STEP 5: Create spatial grid for market analysis
        logger.info(
            f"Creating market analysis grid with {self.grid_size} degree resolution..."
        )
        minx, miny, maxx, maxy = census_gdf.total_bounds
        grid_cells = [
            box(x, y, x + self.grid_size, y + self.grid_size)
            for x in np.arange(minx, maxx, self.grid_size)
            for y in np.arange(miny, maxy, self.grid_size)
        ]
        grid = gpd.GeoDataFrame(geometry=grid_cells, crs=census_gdf.crs)
        logger.info(f"Created {len(grid)} grid cells for market analysis")

        # STEP 6: Perform spatial joins for market data aggregation
        logger.info("Aggregating market data into spatial grid...")
        joined_real_estate = gpd.sjoin(
            real_estate_gdf, grid, how="inner", predicate="within"
        )
        joined_census = gpd.sjoin(
            census_gdf, grid, how="inner", predicate="within"
        )
        joined_housing = gpd.sjoin(
            housing_gdf, grid, how="inner", predicate="within"
        )

        # STEP 7: Calculate property diversity indicator
        # Property diversity measures market sophistication and development maturity
        logger.info("Calculating property diversity indicators...")
        dwelling_columns = joined_housing.columns[
            joined_housing.columns.str.contains("Dwellings")
        ]
        logger.info(f"Found dwelling types: {list(dwelling_columns)}")

        # Diversity score: count of different dwelling types present
        # Higher diversity indicates more mature, mixed-use development
        joined_housing["property_diversity"] = (
            joined_housing[dwelling_columns] > 0
        ).sum(axis=1)
        logger.info(
            f"Property diversity calculated - range: {joined_housing.property_diversity.min()}-{joined_housing.property_diversity.max()}"
        )

        # STEP 8: Aggregate market data into grid
        logger.info("Performing comprehensive market data aggregation...")

        grid = pd.concat(
            [
                grid,
                # Price indicators (market value signals)
                joined_real_estate.groupby("index_right")[
                    "selling_price"
                ].mean(),  # Average sale prices
                joined_real_estate.groupby("index_right")[
                    "renting_price"
                ].mean(),  # Average rental rates
                # Market activity indicators (trading volume and liquidity)
                joined_real_estate.groupby(["index_right", "trade_type"])[
                    "price"
                ]
                .count()
                .loc[(slice(None), "rent")]
                .rename("rental_listings_count"),  # Rental market activity
                joined_real_estate.groupby(["index_right", "trade_type"])[
                    "price"
                ]
                .count()
                .loc[(slice(None), "sale")]
                .rename("sale_listings_count"),  # Sales market activity
                # Demographic indicators (demand drivers)
                joined_census.groupby("index_right")[
                    "TotalPopulation"
                ].sum(),  # Population density
                joined_census.groupby("index_right")[
                    "HouseholdAverageSize"
                ].mean(),  # Household characteristics
                joined_census.groupby("index_right")[
                    "age"
                ].mean(),  # Age demographics
                # Housing market structure indicators
                joined_housing.groupby("index_right")[
                    "TotalDwellings"
                ].sum(),  # Total housing supply
                joined_housing.groupby("index_right")[
                    "OwnedDwellings"
                ].sum(),  # Ownership market
                joined_housing.groupby("index_right")[
                    "RentedDwellings"
                ].sum(),  # Rental market
                joined_housing.groupby("index_right")[
                    "PublicHousing"
                ].sum(),  # Public/social housing
                joined_housing.groupby("index_right")[
                    "CommercialDwellings"
                ].sum(),  # Commercial properties
                joined_housing.groupby("index_right")[
                    "ResidentialDwellings"
                ].sum(),  # Residential stock
                joined_housing.groupby("index_right")[
                    "property_diversity"
                ].mean(),  # Development diversity
            ],
            axis=1,
        )

        logger.info(
            f"Market data aggregation completed - {len(grid.columns)} market indicators per cell"
        )

        # Create backup before scoring calculations
        grid_backup = grid.copy(deep=True)

        # STEP 9: Calculate market activity indices
        logger.info("Calculating comprehensive market activity scoring...")

        # Identify empty cells for masking
        mask = grid.iloc[:, 1:].isna().all(axis=1)
        logger.info(f"Identified {mask.sum()} empty grid cells for masking")

        # Fill NaN values for calculations
        grid = grid.fillna(0.0)

        # TASK 2 MARKET ANALYSIS SCORING ALGORITHM:
        grid = grid.assign(
            # Market Activity Index (30% weight)
            # Measures market liquidity, pricing, and rental activity
            # Formula: 0.4×total_listings + 0.3×price_levels + 0.3×rental_focus
            market_activity=lambda df: (
                0.4
                * self.norm(
                    df.rental_listings_count + df.sale_listings_count
                )  # Total market volume
                + 0.3
                * (
                    (self.norm(df.selling_price) + self.norm(df.renting_price))
                    / 2.0
                )  # Average price levels
                + 0.3
                * self.norm(df.rental_listings_count)  # Rental market strength
            ),
            # Property Mix Index (30% weight)
            # Assesses development diversity and market sophistication
            # Formula: 0.4×residential + 0.3×commercial + 0.3×diversity
            property_mix=lambda df: (
                0.4
                * self.norm(df.ResidentialDwellings)  # Residential development
                + 0.3 * self.norm(df.CommercialDwellings)  # Commercial presence
                + 0.3
                * self.norm(df.property_diversity)  # Property type diversity
            ),
            # Occupancy Index (20% weight)
            # Analyzes ownership patterns and housing market structure
            # Formula: 0.5×ownership_ratio + 0.5×public_housing_ratio
            occupancy_index=lambda df: (
                0.5
                * self.norm(
                    df.OwnedDwellings / df.RentedDwellings
                )  # Ownership vs rental ratio
                + 0.5
                * self.norm(
                    df.PublicHousing / (df.TotalDwellings - df.PublicHousing)
                )  # Public housing presence
            ),
            # Population Index (20% weight)
            # Demographic factors driving housing demand
            # Formula: 0.4×population + 0.3×household_size + 0.3×age
            population_index=lambda df: (
                0.4 * self.norm(df.TotalPopulation)  # Population density
                + 0.3
                * self.norm(df.HouseholdAverageSize)  # Household size patterns
                + 0.3 * self.norm(df.age)  # Age demographics
            ),
        )

        logger.info(
            "Market indices calculated - computing final market scores..."
        )

        # Calculate final base score (weighted combination of market indices)
        # Mathematical Model: Balanced approach across market dimensions
        # 30% market activity + 30% property mix + 20% occupancy + 20% population
        grid = grid.assign(
            base_score=lambda df: (
                0.3 * df.market_activity  # Market liquidity and activity
                + 0.3 * df.property_mix  # Development diversity
                + 0.2 * df.occupancy_index  # Housing market structure
                + 0.2 * df.population_index  # Demographic demand factors
            )
        )

        logger.info("Market activity base scores calculated")

        # STEP 10: Finalize market analysis results
        # Combine original grid with calculated market scores
        grid = pd.concat(
            [grid_backup, grid.iloc[:, -5:]], axis=1
        )  # Last 5 columns are the market scores

        # Sort by market activity score for ranking
        grid = grid.sort_values(by="base_score", ascending=False)

        # Apply mask to restore NaN values for empty cells
        grid.loc[mask, grid.columns[1:]] = np.nan

        # Store market analysis results
        self.grids["task_2"][city[-1]] = grid.copy(deep=True)

        logger.info(
            f"Task 2 market analysis completed for {city[-1]} - stored {len(grid)} grid cells"
        )
        logger.info(
            f"Market score distribution - Mean: {grid.base_score.mean():.3f}, Std: {grid.base_score.std():.3f}"
        )

    def plot_results(self, city, task):
        """
        Comprehensive geospatial visualization of analysis results.

        Mathematical Approach:
        - Log transformation: log(x+1) handles zero values and wide ranges
        - Quantile-based scaling: 1st-99th percentile removes outliers
        - Multiple colormaps: randomly selected for visual distinction

        Visualization Strategy:
        - Each feature gets its own subplot for detailed analysis
        - Basemap provides geographic context
        - Consistent scaling allows cross-feature comparison

        Expected Usage:
        - Pattern identification across different metrics
        - Spatial correlation analysis
        - Quality control and validation
        - Stakeholder presentation and reporting
        """
        logger.info(
            f"Creating comprehensive visualization for {city[-1]} - {task}..."
        )

        # Get analysis results
        grid = self.grids[task][city[-1]].copy(deep=True)
        logger.info(
            f"Plotting {len(grid.columns)-1} features across {len(grid)} grid cells"
        )

        # Calculate subplot layout
        n_feats = grid.shape[1] - 1  # Exclude geometry column
        n_cols = 5  # Fixed column count for layout
        n_rows = int(n_feats / n_cols)
        if n_rows * n_cols < n_feats:
            n_rows += 1

        logger.info(
            f"Creating {n_rows}x{n_cols} subplot layout for {n_feats} features"
        )

        # Figure sizing for comprehensive display
        single_fig_width = 8
        single_fig_height = 8
        fig = plt.figure(
            figsize=(
                single_fig_width * n_cols + n_cols,
                single_fig_height * n_rows + n_rows,
            )
        )

        # Plot each feature with geographic context
        for i, column in enumerate(grid.columns[1:], 1):  # Skip geometry column
            logger.info(f"Plotting feature {i}: {column}")

            ax = plt.subplot(n_rows, n_cols, i)

            # Apply log transformation for better visualization
            # log(x+1) transformation handles zero values and compresses wide ranges
            grid[f"log_{column}"] = np.log1p(grid[column])

            # Use quantile-based scaling to handle outliers
            # 1st and 99th percentiles provide robust range estimation
            vmax = grid[f"log_{column}"].quantile(0.99)
            vmin = grid[f"log_{column}"].quantile(0.01)
            logger.info(
                f"Feature {column} - log scale range: {vmin:.3f} to {vmax:.3f}"
            )

            # Ensure proper coordinate reference system
            grid.set_crs(
                epsg=4326, inplace=True
            )  # WGS84 geographic coordinates

            # Create choropleth map with basemap
            grid.to_crs(
                epsg=3857
            ).plot(  # Convert to Web Mercator for basemap compatibility
                column=f"log_{column}",
                legend=True,  # Include color scale legend
                cmap=np.random.choice(
                    self.cmaps
                ),  # Random colormap for distinction
                edgecolor="white",  # Grid cell boundaries
                linewidth=0.1,  # Thin boundaries
                vmin=vmin,
                vmax=vmax,  # Consistent scaling
                ax=ax,
            )

            # Add geographic basemap for context
            ctx.add_basemap(
                ax, source=ctx.providers.CartoDB.Positron
            )  # Clean, minimal basemap

            # Clean up axes and add title
            ax.axis("off")  # Remove coordinate axes
            ax.set_title(
                f"{column} per Grid Cell of {city[-1]} (Log scaled)",
                fontsize=14,
            )

        logger.info(f"Visualization completed for {city[-1]} - {task}")
        plt.show()

