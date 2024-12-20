def create_table_real_estate():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    
    -- Create table if it doesn't exist
    CREATE TABLE IF NOT EXISTS schema_marketplace.real_estate (
        url TEXT NOT NULL,
        city TEXT NULL,
        price varchar(25) NULL
    );

    -- Truncate the table to ensure clean data
    TRUNCATE TABLE schema_marketplace.real_estate;
    """


def transformation_real_estate():
    return """
    INSERT INTO schema_marketplace.real_estate (url, city, price)
    SELECT url, city, price 
    FROM raw_schema_marketplace.real_estate;
    """



def economic():
    return """
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    CREATE TABLE IF NOT EXISTS schema_marketplace.economic (
        longitude DECIMAL(10,6),
        latitude DECIMAL(10,6),
        city TEXT,
        working_age_population TEXT,
        employed_population TEXT,
        unemployed_population TEXT,
        employment_rate TEXT,
        avg_annual_income TEXT,
        median_annual_income TEXT,
        PRIMARY KEY (longitude, latitude)
    );

    TRUNCATE TABLE schema_marketplace.economic;

    WITH parsed_data AS (
        SELECT 
            NULLIF(SPLIT_PART(geo_location, ',', 2), '')::DECIMAL(10,6) as longitude,
            NULLIF(SPLIT_PART(geo_location, ',', 1), '')::DECIMAL(10,6) as latitude,
            city,
            CAST(working_age_population AS TEXT),
            CAST(employed_population AS TEXT),
            CAST(unemployed_population AS TEXT),
            CAST(employment_rate AS TEXT),
            CAST(avg_annual_income AS TEXT),
            CAST(median_annual_income AS TEXT)
        FROM raw_schema_marketplace.generate_economic_slocator_data
        WHERE geo_location IS NOT NULL
    )
    INSERT INTO schema_marketplace.economic
    SELECT 
        longitude,
        latitude,
        city,
        working_age_population,
        employed_population,
        unemployed_population,
        employment_rate,
        avg_annual_income,
        median_annual_income
    FROM parsed_data
    WHERE longitude IS NOT NULL
    AND latitude IS NOT NULL;
    """

def household():
    return """
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    CREATE TABLE IF NOT EXISTS schema_marketplace.household (
        longitude DECIMAL(10,6),
        latitude DECIMAL(10,6),
        country TEXT,
        "Household Average Size" TEXT,
        "Household Median Size" TEXT,
        "Degree" TEXT,
        PRIMARY KEY (longitude, latitude)
    );

    TRUNCATE TABLE schema_marketplace.household;

    WITH combined_data AS (
        -- Saudi Arabia Household Data
        SELECT 
            NULLIF(SPLIT_PART("Location", ',', 2), '')::DECIMAL(10,6) as longitude,
            NULLIF(SPLIT_PART("Location", ',', 1), '')::DECIMAL(10,6) as latitude,
            'Saudi Arabia' as country,
            CAST("Household Average Size" AS TEXT) as "Household Average Size",
            CAST("Household Median Size" AS TEXT) as "Household Median Size",
            "Degree"
        FROM raw_schema_marketplace.household

        UNION ALL

        -- Canada Household Data
        SELECT
            NULLIF(SPLIT_PART(geo_location, ',', 2), '')::DECIMAL(10,6) as longitude,
            NULLIF(SPLIT_PART(geo_location, ',', 1), '')::DECIMAL(10,6) as latitude,
            'Canada' as country,
            CAST("Household Average Size" AS TEXT) as "Household Average Size",
            CAST("Household Median Size" AS TEXT) as "Household Median Size",
            "Degree"
        FROM raw_schema_marketplace.generate_household_slocator_data
    ),
    ranked_data AS (
        SELECT 
            longitude,
            latitude,
            country,
            "Household Average Size",
            "Household Median Size",
            "Degree",
            ROW_NUMBER() OVER (
                PARTITION BY longitude, latitude
                ORDER BY "Household Average Size" DESC NULLS LAST
            ) as rn
        FROM combined_data
        WHERE longitude IS NOT NULL
        AND latitude IS NOT NULL
    )
    INSERT INTO schema_marketplace.household (
        longitude,
        latitude,
        country,
        "Household Average Size",
        "Household Median Size",
        "Degree"
    )
    SELECT 
        longitude,
        latitude,
        country,
        "Household Average Size",
        "Household Median Size",
        "Degree"
    FROM ranked_data
    WHERE rn = 1;
    """

def housing():
   return """
   CREATE SCHEMA IF NOT EXISTS schema_marketplace;
   CREATE TABLE IF NOT EXISTS schema_marketplace.housing (
       longitude DECIMAL(10,6),
       latitude DECIMAL(10,6),
       country TEXT,
       "Total Dwellings" TEXT,
       "Residential Dwellings" TEXT,
       "Owned Dwellings" TEXT,
       "Rented Dwellings" TEXT,
       "Provided Dwellings" TEXT,
       "Other Residential Dwellings" TEXT,
       "Non-Residential Dwellings" TEXT,
       "Public Housing" TEXT,
       "Work Camps" TEXT,
       "Commercial Dwellings" TEXT,
       "Other Dwellings" TEXT,
       PRIMARY KEY (longitude, latitude)
   );

   TRUNCATE TABLE schema_marketplace.housing;

   WITH combined_data AS (
       -- Saudi Arabia Housing Data
       SELECT 
           NULLIF(SPLIT_PART("Location", ',', 2), '')::DECIMAL(10,6) as longitude,
           NULLIF(SPLIT_PART("Location", ',', 1), '')::DECIMAL(10,6) as latitude,
           'Saudi Arabia' as country,
           CAST("Total Dwellings" AS TEXT),
           CAST("Residential Dwellings" AS TEXT),
           CAST("Owned Dwellings" AS TEXT),
           CAST("Rented Dwellings" AS TEXT),
           CAST("Provided Dwellings" AS TEXT),
           CAST("Other Residential Dwellings" AS TEXT),
           CAST("Non-Residential Dwellings" AS TEXT),
           CAST("Public Housing" AS TEXT),
           CAST("Work Camps" AS TEXT),
           CAST("Commercial Dwellings" AS TEXT),
           CAST("Other Dwellings" AS TEXT)
       FROM raw_schema_marketplace.housing

       UNION ALL

       -- Canada Housing Data
       SELECT
           NULLIF(SPLIT_PART(geo_location, ',', 2), '')::DECIMAL(10,6) as longitude,
           NULLIF(SPLIT_PART(geo_location, ',', 1), '')::DECIMAL(10,6) as latitude,
           'Canada' as country,
           CAST("Total Dwellings" AS TEXT),
           CAST("Residential Dwellings" AS TEXT),
           CAST("Owned Dwellings" AS TEXT),
           CAST("Rented Dwellings" AS TEXT),
           CAST("Provided Dwellings" AS TEXT),
           CAST("Other Residential Dwellings" AS TEXT),
           CAST("Non-Residential Dwellings" AS TEXT),
           CAST("Public Housing" AS TEXT),
           CAST("Work Camps" AS TEXT),
           CAST("Commercial Dwellings" AS TEXT),
           CAST("Other Dwellings" AS TEXT)
       FROM raw_schema_marketplace.generate_housing_slocator_data
   ),
   ranked_data AS (
       SELECT 
           longitude,
           latitude,
           country,
           "Total Dwellings",
           "Residential Dwellings",
           "Owned Dwellings",
           "Rented Dwellings",
           "Provided Dwellings",
           "Other Residential Dwellings",
           "Non-Residential Dwellings",
           "Public Housing",
           "Work Camps",
           "Commercial Dwellings",
           "Other Dwellings",
           ROW_NUMBER() OVER (
               PARTITION BY longitude, latitude
               ORDER BY "Total Dwellings" DESC NULLS LAST
           ) as rn
       FROM combined_data
       WHERE longitude IS NOT NULL
       AND latitude IS NOT NULL
   )
   INSERT INTO schema_marketplace.housing
   SELECT 
       longitude,
       latitude,
       country,
       "Total Dwellings",
       "Residential Dwellings",
       "Owned Dwellings",
       "Rented Dwellings",
       "Provided Dwellings",
       "Other Residential Dwellings",
       "Non-Residential Dwellings",
       "Public Housing",
       "Work Camps",
       "Commercial Dwellings",
       "Other Dwellings"
   FROM ranked_data
   WHERE rn = 1;
   """

def population():
    return """
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    CREATE TABLE IF NOT EXISTS schema_marketplace.population (
        longitude DECIMAL(10,6),
        latitude DECIMAL(10,6),
        country TEXT,
        population TEXT,
        population_density TEXT,
        male_population TEXT,
        female_population TEXT,
        median_age_male TEXT,
        median_age_female TEXT,
        PRIMARY KEY (longitude, latitude)
    );
    
    TRUNCATE TABLE schema_marketplace.population;
    
    WITH combined_data AS (
        -- Saudi Arabia Census Data
        SELECT 
            NULLIF(SPLIT_PART("Location", ',', 2), '')::DECIMAL(10,6) as longitude,
            NULLIF(SPLIT_PART("Location", ',', 1), '')::DECIMAL(10,6) as latitude,
            'Saudi Arabia' as country,
            "Total Population" as population,
            "Population Density" as population_density,
            "Male Population" as male_population,
            "Female Population" as female_population,
            "Median Age (Male)" as median_age_male,
            "Median Age (Female)" as median_age_female
        FROM raw_schema_marketplace.population
        
        UNION ALL
        
        -- Canada Census Data
        SELECT 
            NULLIF(longitude, '')::DECIMAL(10,6),
            NULLIF(latitude, '')::DECIMAL(10,6),
            'Canada' as country,
            CAST(population_2021 AS TEXT) as population,
            CAST(population_density_per_square_kilometre_2021 AS TEXT) as population_density,
            NULL as male_population,
            NULL as female_population,
            NULL as median_age_male,
            NULL as median_age_female
        FROM raw_schema_marketplace.canada_census
    ),
    ranked_data AS (
        SELECT 
            longitude,
            latitude,
            country,
            population,
            population_density,
            male_population,
            female_population,
            median_age_male,
            median_age_female,
            ROW_NUMBER() OVER (
                PARTITION BY longitude, latitude
                ORDER BY population DESC NULLS LAST
            ) as rn
        FROM combined_data
        WHERE longitude IS NOT NULL 
        AND latitude IS NOT NULL
    )
    INSERT INTO schema_marketplace.population (
        longitude,
        latitude,
        country,
        population,
        population_density,
        male_population,
        female_population,
        median_age_male,
        median_age_female
    )
    SELECT 
        longitude,
        latitude,
        country,
        population,
        population_density,
        male_population,
        female_population,
        median_age_male,
        median_age_female
    FROM ranked_data
    WHERE rn = 1;
    """
