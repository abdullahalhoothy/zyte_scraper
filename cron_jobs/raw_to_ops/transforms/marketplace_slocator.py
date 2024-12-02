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


def housing():
    return """
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    
    CREATE TABLE IF NOT EXISTS schema_marketplace.housing (
        "Location" TEXT NOT NULL,
        "Degree" TEXT NULL,
        "Total Dwellings" TEXT NULL,
        "Residential Dwellings" TEXT NULL,
        "Owned Dwellings" TEXT NULL,
        "Rented Dwellings" TEXT NULL,
        "Provided Dwellings" TEXT NULL,
        "Other Residential Dwellings" TEXT NULL,
        "Non-Residential Dwellings" TEXT NULL,
        "Public Housing" TEXT NULL,
        "Work Camps" TEXT NULL,
        "Commercial Dwellings" TEXT NULL,
        "Other Dwellings" TEXT NULL,
        "Zoom Level" TEXT NULL
    );
    TRUNCATE TABLE schema_marketplace.housing;

    INSERT INTO schema_marketplace.housing (
    "Location", "Degree", "Total Dwellings", "Residential Dwellings", 
    "Owned Dwellings", "Rented Dwellings", "Provided Dwellings", 
    "Other Residential Dwellings", "Non-Residential Dwellings", "Public Housing",
    "Work Camps", "Commercial Dwellings", "Other Dwellings", "Zoom Level"
    )
    SELECT 
        "Location","Degree", "Total Dwellings", "Residential Dwellings", 
        "Owned Dwellings", "Rented Dwellings", "Provided Dwellings", 
        "Other Residential Dwellings", "Non-Residential Dwellings", "Public Housing",
        "Work Camps", "Commercial Dwellings", "Other Dwellings", "Zoom Level"
    FROM raw_schema_marketplace.housing;
    """

def household():
    return """
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    
    CREATE TABLE IF NOT EXISTS schema_marketplace.household (
        "Location" TEXT NOT NULL,
        "Household Average Size" TEXT NULL,
        "Household Median Size" TEXT NULL,
        "Degree" TEXT NULL,
        "Zoom Level" TEXT NULL
    );
    TRUNCATE TABLE schema_marketplace.household;

    INSERT INTO schema_marketplace.household (
    "Location", "Household Average Size", "Household Median Size", 
    "Degree", "Zoom Level"
    )
    SELECT 
        "Location", "Household Average Size", "Household Median Size", 
        "Degree", "Zoom Level"
    FROM raw_schema_marketplace.household;
    """
        
def population():
    return """
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    CREATE TABLE IF NOT EXISTS schema_marketplace.population (
        "Location" TEXT NOT NULL,
        "Degree" TEXT NULL,
        "Male Population" TEXT NULL,
        "Female Population" TEXT NULL,
        "Median Age (Male)" TEXT NULL,
        "Median Age (Female)" TEXT NULL,
        "Total Population" TEXT NULL,
        "Population Density" TEXT NULL,
        "Zoom Level" TEXT NULL
    );
    TRUNCATE TABLE schema_marketplace.population;
   
    WITH ranked_data AS (
        SELECT 
            "Location",
            "Degree",
            "Male Population",
            "Female Population",
            "Median Age (Male)",
            "Median Age (Female)",
            "Total Population",
            "Population Density",
            "Zoom Level",
            ROW_NUMBER() OVER (
                PARTITION BY 
                    "Male Population",
                    "Female Population",
                    "Median Age (Male)",
                    "Median Age (Female)",
                    "Total Population",
                    "Population Density"
                ORDER BY "Location"
            ) as rn
        FROM raw_schema_marketplace.population
    )
    INSERT INTO schema_marketplace.population (
        "Location",
        "Degree",
        "Male Population",
        "Female Population",
        "Median Age (Male)",
        "Median Age (Female)",
        "Total Population",
        "Population Density",
        "Zoom Level"
    )
    SELECT 
        "Location",
        "Degree",
        "Male Population",
        "Female Population",
        "Median Age (Male)",
        "Median Age (Female)",
        "Total Population",
        "Population Density",
        "Zoom Level"
    FROM ranked_data
    WHERE rn = 1;
    """   

def canada_census():
    return """
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    
    CREATE TABLE IF NOT EXISTS schema_marketplace.canada_census (
        da_id TEXT NOT NULL,
        population_2021 NUMERIC NULL,
        total_private_dwellings_2021 NUMERIC NULL,
        private_dwellings_occupied_by_usual_residents_2021 NUMERIC NULL,
        land_area_in_square_kilometres_2021 NUMERIC NULL,
        population_density_per_square_kilometre_2021 NUMERIC NULL,
        province TEXT NULL,
        longitude NUMERIC NULL,
        latitude NUMERIC NULL
    );
    
    TRUNCATE TABLE schema_marketplace.canada_census;
    
    INSERT INTO schema_marketplace.canada_census (
        da_id,
        population_2021,
        total_private_dwellings_2021,
        private_dwellings_occupied_by_usual_residents_2021,
        land_area_in_square_kilometres_2021,
        population_density_per_square_kilometre_2021,
        province,
        longitude,
        latitude
    )
    SELECT
        da_id,
        population_2021,
        total_private_dwellings_2021,
        private_dwellings_occupied_by_usual_residents_2021,
        land_area_in_square_kilometres_2021,
        population_density_per_square_kilometre_2021,
        province,
        longitude,
        latitude
    FROM raw_schema_marketplace.canada_census;
    """