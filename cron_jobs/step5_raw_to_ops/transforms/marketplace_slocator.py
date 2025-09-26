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


def aqar_real_estate_historic():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;

    -- Create historic aqar real estate table with all columns and is_current flag
    CREATE TABLE IF NOT EXISTS schema_marketplace.aqar_real_estate_historic (
        listing_id BIGINT,  -- Extracted ID from URL (e.g., 6164188)
        url TEXT NOT NULL,  -- Keep the full URL
        price BIGINT,
        latitude REAL,
        longitude REAL,
        category_id INTEGER,
        city TEXT,
        city_id INTEGER,
        title TEXT,
        address TEXT,
        rent_period REAL,  -- Changed to REAL to match raw table
        listing_created_timestamp INTEGER,  -- Changed to INTEGER to match raw table
        extraction_timestamp INTEGER,  -- Changed to INTEGER to match raw table
        listing_created_date TEXT,  -- Changed to TEXT to match raw table
        extraction_date TEXT,  -- Changed to TEXT to match raw table, allow NULL
        category TEXT,
        price_description TEXT,
        data TEXT,  -- Changed to TEXT to match raw table (can convert to JSONB later if needed)
        is_current BOOLEAN DEFAULT FALSE,  -- Flag to mark latest records
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        record_id SERIAL PRIMARY KEY  -- Use auto-increment ID as primary key instead
    );

    -- Truncate table and insert all historic data
    TRUNCATE TABLE schema_marketplace.aqar_real_estate_historic RESTART IDENTITY;

    -- Insert all records from raw table
    INSERT INTO schema_marketplace.aqar_real_estate_historic (
        listing_id,
        url,
        price,
        latitude,
        longitude,
        category_id,
        city,
        city_id,
        title,
        address,
        rent_period,
        listing_created_timestamp,
        extraction_timestamp,
        listing_created_date,
        extraction_date,
        category,
        price_description,
        data,
        is_current,
        updated_at
    )
    SELECT 
        -- Extract the numeric ID from the end of the URL
        CASE 
            WHEN url ~ '-(\d+)$' 
            THEN (regexp_match(url, '-(\d+)$'))[1]::BIGINT 
            ELSE NULL 
        END as listing_id,
        url,
        price,
        latitude,
        longitude,
        category_id,
        city,
        city_id,
        title,
        address,
        rent_period,
        listing_created_timestamp,
        extraction_timestamp,
        listing_created_date,
        extraction_date,
        category,
        price_description,
        data,
        CASE 
            WHEN ROW_NUMBER() OVER (
                PARTITION BY url 
                ORDER BY 
                    CASE WHEN extraction_date IS NOT NULL AND extraction_date ~ '^\d{4}-\d{2}-\d{2}$' 
                         THEN extraction_date::DATE 
                         ELSE '1900-01-01'::DATE  -- Default old date for NULL/invalid dates
                    END DESC,
                    COALESCE(extraction_timestamp, 0) DESC
            ) = 1 
            THEN TRUE 
            ELSE FALSE 
        END as is_current,
        CURRENT_TIMESTAMP
    FROM raw_schema_marketplace.saudi_real_estate
    ORDER BY url, 
             CASE WHEN extraction_date IS NOT NULL AND extraction_date ~ '^\d{4}-\d{2}-\d{2}$' 
                  THEN extraction_date::DATE 
                  ELSE '1900-01-01'::DATE 
             END DESC, 
             COALESCE(extraction_timestamp, 0) DESC;
    """

def create_enriched_demographic_table():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;

    -- Create enriched demographics table if it doesn't exist
    CREATE TABLE IF NOT EXISTS schema_marketplace."saudi_real_estate_demographic_enriched" (
        listing_id BIGINT,
        direction_id TEXT,
        total_population BIGINT,
        avg_density REAL,
        avg_median_age REAL,
        avg_income REAL,
        percentage_age_above_20 REAL,
        percentage_age_above_25 REAL,
        percentage_age_above_30 REAL,
        percentage_age_above_35 REAL,
        percentage_age_above_40 REAL,
        percentage_age_above_45 REAL,
        percentage_age_above_50 REAL,
        demographics_analysis_date TEXT,
        is_current BOOLEAN
    );

    TRUNCATE TABLE schema_marketplace."saudi_real_estate_demographic_enriched";

    INSERT INTO schema_marketplace."saudi_real_estate_demographic_enriched" (
        listing_id, direction_id, total_population, avg_density, avg_median_age, avg_income,
        percentage_age_above_20, percentage_age_above_25, percentage_age_above_30, percentage_age_above_35,
        percentage_age_above_40, percentage_age_above_45, percentage_age_above_50, demographics_analysis_date,
        is_current
    )
    SELECT 
        red.listing_id, red.direction_id, red.total_population, red.avg_density,
        red.avg_median_age, red.avg_income, red.percentage_age_above_20, red.percentage_age_above_25,
        red.percentage_age_above_30, red.percentage_age_above_35, red.percentage_age_above_40,
        red.percentage_age_above_45, red.percentage_age_above_50, red.demographics_analysis_date
    -- mark latest per listing_id as is_current = true based on demographics_analysis_date
    , CASE WHEN ROW_NUMBER() OVER (
        PARTITION BY red.listing_id
        ORDER BY COALESCE(red.demographics_analysis_date, '1900-01-01') DESC
    ) = 1 THEN TRUE ELSE FALSE END AS is_current

    FROM raw_schema_marketplace."saudi_real_estate_الرياض_enriched_with_demographics" red
    where red.is_current = true
    """

def create_enriched_traffic_table():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;

    -- Create enriched traffic table if it doesn't exist
    CREATE TABLE IF NOT EXISTS schema_marketplace."saudi_real_estate_traffic_enriched" (
        listing_id BIGINT,
        url TEXT,
        latitude REAL,
        longitude REAL,
        city TEXT,
        direction_id TEXT,
        category TEXT,
        traffic_score REAL,
        traffic_storefront_score REAL,
        traffic_area_score REAL,
        traffic_screenshot_filename TEXT,
        traffic_analysis_date TEXT,
        is_current BOOLEAN
    );

    TRUNCATE TABLE schema_marketplace."saudi_real_estate_traffic_enriched";

    INSERT INTO schema_marketplace."saudi_real_estate_traffic_enriched" (
        listing_id, url, latitude, longitude, city, direction_id, category,
        traffic_score, traffic_storefront_score, traffic_area_score, traffic_screenshot_filename,
        traffic_analysis_date, is_current
    )
    SELECT 
        te.listing_id, te.url, te.latitude, te.longitude, te.city, te.direction_id, te.category,
        te.traffic_score, te.traffic_storefront_score, te.traffic_area_score, te.traffic_screenshot_filename,
        te.traffic_analysis_date,
    -- mark latest per listing_id as is_current = true based on traffic_analysis_date
    CASE WHEN ROW_NUMBER() OVER (
        PARTITION BY te.listing_id
        ORDER BY COALESCE(te.traffic_analysis_date, '1900-01-01') DESC
    ) = 1 THEN TRUE ELSE FALSE END AS is_current

    FROM raw_schema_marketplace."saudi_real_estate_الرياض_enriched_with_traffic" te
    where te.is_current = true
    """

def historic_to_saudi_real_estate():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;

    -- Create table if it doesn't exist (add demographic and traffic columns)
    CREATE TABLE IF NOT EXISTS schema_marketplace.saudi_real_estate (
        listing_id BIGINT,
        url TEXT NOT NULL,
        city TEXT NULL,
        price BIGINT NULL,
        latitude REAL,
        longitude REAL,
        category TEXT,
        direction_id TEXT,
        total_population BIGINT,
        avg_density REAL,
        avg_median_age REAL,
        avg_income REAL,
        percentage_age_above_20 REAL,
        percentage_age_above_25 REAL,
        percentage_age_above_30 REAL,
        percentage_age_above_35 REAL,
        percentage_age_above_40 REAL,
        percentage_age_above_45 REAL,
        percentage_age_above_50 REAL,
        demographics_analysis_date TEXT,
        traffic_score REAL,
        traffic_storefront_score REAL,
        traffic_area_score REAL,
        traffic_screenshot_filename TEXT,
        traffic_analysis_date TEXT
    );

    -- Truncate the table to ensure clean data
    TRUNCATE TABLE schema_marketplace.saudi_real_estate;

    WITH current_listings AS (
        SELECT listing_id, url, city, price, latitude, longitude, category
        FROM schema_marketplace.aqar_real_estate_historic
        WHERE is_current = true
    ),
    merged_enriched AS (
        SELECT 
            cl.listing_id, cl.url, cl.city, cl.price, cl.latitude, cl.longitude, cl.category,
            red.direction_id, red.total_population, red.avg_density,
            red.avg_median_age, red.avg_income, red.percentage_age_above_20, red.percentage_age_above_25,
            red.percentage_age_above_30, red.percentage_age_above_35, red.percentage_age_above_40,
            red.percentage_age_above_45, red.percentage_age_above_50, red.demographics_analysis_date,
            te.traffic_score, te.traffic_storefront_score, te.traffic_area_score, te.traffic_screenshot_filename,
            te.traffic_analysis_date
        FROM current_listings cl

        LEFT JOIN schema_marketplace.saudi_real_estate_demographic_enriched red
            ON cl.listing_id = red.listing_id
        LEFT JOIN schema_marketplace.saudi_real_estate_traffic_enriched te ON 
            cl.listing_id = te.listing_id
        
    )
    INSERT INTO schema_marketplace.saudi_real_estate (
        listing_id, url, city, price, latitude, longitude, category,
        direction_id, total_population, avg_density, avg_median_age, avg_income,
        percentage_age_above_20, percentage_age_above_25, percentage_age_above_30,
        percentage_age_above_35, percentage_age_above_40, percentage_age_above_45,
        percentage_age_above_50, demographics_analysis_date,
        traffic_score, traffic_storefront_score, traffic_area_score, traffic_screenshot_filename,
        traffic_analysis_date
    )
    SELECT 
        listing_id, url, city, price, latitude, longitude, category,
        direction_id, total_population, avg_density, avg_median_age, avg_income,
        percentage_age_above_20, percentage_age_above_25, percentage_age_above_30,
        percentage_age_above_35, percentage_age_above_40, percentage_age_above_45,
        percentage_age_above_50, demographics_analysis_date,
        traffic_score, traffic_storefront_score, traffic_area_score, traffic_screenshot_filename,
        traffic_analysis_date
    FROM merged_enriched;
    """