def datasets():
    return """
CREATE SCHEMA IF NOT EXISTS schema_marketplace;
CREATE TABLE IF NOT EXISTS schema_marketplace.datasets
(
    filename text COLLATE pg_catalog."default" NOT NULL,
    request_data jsonb,
    response_data jsonb,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT datasets_pkey PRIMARY KEY (filename)
)
    """


def saudi_real_estate():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    
    -- Create table if it doesn't exist
    CREATE TABLE IF NOT EXISTS schema_marketplace.saudi_real_estate (
        url TEXT NOT NULL,
        city TEXT NULL,
        price varchar(25) NULL,
        latitude REAL,
        longitude REAL,
        category TEXT
    );

    -- Truncate the table to ensure clean data
    TRUNCATE TABLE schema_marketplace.saudi_real_estate;

    
    INSERT INTO schema_marketplace.saudi_real_estate (url, city, price, latitude, longitude, category)
    SELECT url, city, price, latitude, longitude, category
    FROM raw_schema_marketplace.saudi_real_estate
    WHERE extraction_date = (
    SELECT MAX(extraction_date) 
    FROM raw_schema_marketplace.saudi_real_estate);
    """


def census():
    return """
CREATE SCHEMA IF NOT EXISTS schema_marketplace;
CREATE TABLE IF NOT EXISTS schema_marketplace.census (
    longitude DECIMAL(10,6),
    latitude DECIMAL(10,6),
    country TEXT,
    city TEXT,
    population REAL,
    population_density REAL,
    male_population REAL,
    female_population REAL,
    median_age_male REAL,
    median_age_female REAL,
    household_average_size REAL,
    household_median_size REAL,
    zoom_level REAL,
    PRIMARY KEY (longitude, latitude)
);

TRUNCATE TABLE schema_marketplace.census;

WITH combined_data AS (
    -- Saudi Arabia Census Data
    SELECT
        NULLIF(longitude, NULL)::DECIMAL(10,6) as longitude ,
        NULLIF(latitude, NULL)::DECIMAL(10,6) as latitude,
        'Saudi Arabia' as country,
        'Saudi City' as city,
        "TotalPopulation" as population,
        "PopulationDensity" as population_density,
        "MalePopulation" as male_population,
        "FemalePopulation" as female_population,
        "MedianAgeMale" as median_age_male,
        "MedianAgeFemale" as median_age_female,
        "HouseholdAverageSize" as household_average_size, 
        "HouseholdMedianSize" as household_median_size,
        "ZoomLevel" as zoom_level
    FROM raw_schema_marketplace.saudi_census

    UNION ALL

    -- Canada Census Data
    SELECT
        NULLIF(longitude, NULL)::DECIMAL(10,6) as longitude ,
        NULLIF(latitude, NULL)::DECIMAL(10,6) as latitude,
        'Canada' as country,
        CASE 
            WHEN latitude BETWEEN 43.4 AND 43.9 
                AND longitude BETWEEN -79.5 AND -79.2 THEN 'Toronto'
            WHEN latitude BETWEEN 45.4 AND 45.7 
                AND longitude BETWEEN -73.7 AND -73.4 THEN 'Montreal'
            ELSE 'Other'
        END as city,
        CAST(population_2021 AS REAL) as population,
        CAST(population_density_per_sq_km AS REAL) as population_density,
        NULL as male_population,
        NULL as female_population,
        NULL as median_age_male,
        NULL as median_age_female,
        NULL as household_average_size, 
        NULL as household_median_size,
        NULL as zoom_level
    FROM raw_schema_marketplace.canada_census
),
ranked_data AS (
    SELECT
        longitude,
        latitude,
        country,
        city,
        population,
        population_density,
        male_population,
        female_population,
        median_age_male,
        median_age_female,
        household_average_size,
        household_median_size,
        zoom_level,
        ROW_NUMBER() OVER (
            PARTITION BY longitude, latitude
            ORDER BY population DESC NULLS LAST
        ) as rn
    FROM combined_data
    WHERE longitude IS NOT NULL
    AND latitude IS NOT NULL
)

INSERT INTO schema_marketplace.census (
    longitude,
    latitude,
    country,
    city,
    population,
    population_density,
    male_population,
    female_population,
    median_age_male,
    median_age_female,
    household_average_size,
    household_median_size,
    zoom_level
)
SELECT DISTINCT
    longitude,
    latitude,
    country,
    city,
    population,
    population_density,
    male_population,
    female_population,
    median_age_male,
    median_age_female,
    household_average_size,
    household_median_size,
    zoom_level
FROM ranked_data
WHERE rn = 1;
    """


def canada_commercial_properties():
    return """
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    CREATE TABLE IF NOT EXISTS schema_marketplace.canada_commercial_properties (
        url TEXT NOT NULL,
        address TEXT,
        price TEXT,
        use_of_property TEXT,
        available_commercial_area TEXT,
        number_of_units TEXT,
        type_of_business TEXT,
        walk_score REAL,
        description TEXT,
        latitude DECIMAL(10,8),
        longitude DECIMAL(10,8),
        region_stats_summary TEXT,
        city_id INTEGER,
        city_name TEXT,
        walking_transport_score REAL,
        transit_transport_score REAL,
        cycling_transport_score REAL,
        driving_transport_score REAL,
        primary_schools_score REAL,
        high_schools_score REAL,
        daycares_score REAL,
        groceries_score REAL,
        restaurants_score REAL,
        shopping_score REAL,
        cafes_score REAL,
        quiet_score REAL,
        nightlife_score REAL,
        vibrant_score REAL,
        historic_score REAL,
        parks_score REAL,
        greenery_score REAL,
        age TEXT,
        incomes TEXT,
        household TEXT,
        family TEXT,
        occupation TEXT,
        construction TEXT,
        housing TEXT,
        schooling TEXT,
        immigration TEXT,
        language TEXT,
        price_description TEXT,
        property_type TEXT,
        city TEXT
    );

    TRUNCATE TABLE schema_marketplace.canada_commercial_properties;


    INSERT INTO schema_marketplace.canada_commercial_properties (
        url,
        address,
        price,
        use_of_property,
        available_commercial_area,
        number_of_units,
        type_of_business,
        walk_score,
        description,
        latitude,
        longitude,
        region_stats_summary,
        city_id,
        city_name,
        walking_transport_score,
        transit_transport_score,
        cycling_transport_score,
        driving_transport_score,
        primary_schools_score,
        high_schools_score,
        daycares_score,
        groceries_score,
        restaurants_score,
        shopping_score,
        cafes_score,
        quiet_score,
        nightlife_score,
        vibrant_score,
        historic_score,
        parks_score,
        greenery_score,
        age,
        incomes,
        household,
        family,
        occupation,
        construction,
        housing,
        schooling,
        immigration,
        language,
        price_description,
        property_type,
        city
    )
    SELECT 
        url,
        address,
        price,
        use_of_property,
        available_commercial_area,
        number_of_units,
        type_of_business,
        NULLIF(walk_score, NULL)::REAL,
        description,
        NULLIF(latitude, NULL)::DECIMAL(10,8),
        NULLIF(longitude, NULL)::DECIMAL(10,8),
        region_stats_summary,
        NULLIF(city_id, NULL)::INTEGER,
        city_name,
        NULLIF(walking_transport_score, NULL)::REAL,
        NULLIF(transit_transport_score, NULL)::REAL,
        NULLIF(cycling_transport_score, NULL)::REAL,
        NULLIF(driving_transport_score, NULL)::REAL,
        NULLIF(primary_schools_score, NULL)::REAL,
        NULLIF(high_schools_score, NULL)::REAL,
        NULLIF(daycares_score, NULL)::REAL,
        NULLIF(groceries_score, NULL)::REAL,
        NULLIF(restaurants_score, NULL)::REAL,
        NULLIF(shopping_score, NULL)::REAL,
        NULLIF(cafes_score, NULL)::REAL,
        NULLIF(quiet_score, NULL)::REAL,
        NULLIF(nightlife_score, NULL)::REAL,
        NULLIF(vibrant_score, NULL)::REAL,
        NULLIF(historic_score, NULL)::REAL,
        NULLIF(parks_score, NULL)::REAL,
        NULLIF(greenery_score, NULL)::REAL,
        age,
        incomes,
        household,
        family,
        occupation,
        construction,
        housing,
        schooling,
        immigration,
        language,
        price_description,
        property_type,
        city
    FROM raw_schema_marketplace.canada_commercial_properties;
    """


# def create_lat_lng_categories_all():
#     # get max and min lat lng of my current 6 tables
#     pass
