def create_table_real_estate():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS "schema-marketplace";
    
    -- Create table if it doesn't exist
    CREATE TABLE IF NOT EXISTS "schema-marketplace".real_estate (
        url TEXT NOT NULL,
        city TEXT NULL,
        price varchar(25) NULL
    );

    -- Truncate the table to ensure clean data
    TRUNCATE TABLE "schema-marketplace".real_estate;
    """


def transformation_real_estate():
    return """
    INSERT INTO "schema-marketplace".real_estate (url, city, price)
    SELECT url, city, price 
    FROM "raw_schema-marketplace".real_estate;
    """


def housing():
    return """
    CREATE SCHEMA IF NOT EXISTS "schema-marketplace";
    
    CREATE TABLE IF NOT EXISTS "schema-marketplace".housing (
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
    TRUNCATE TABLE "schema-marketplace".housing;

    INSERT INTO "schema-marketplace".housing (
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
    FROM "raw_schema-marketplace".housing;
    """

def household():
    return """
    CREATE SCHEMA IF NOT EXISTS "schema-marketplace";
    
    CREATE TABLE IF NOT EXISTS "schema-marketplace".household (
        "Location" TEXT NOT NULL,
        "Household Average Size" TEXT NULL,
        "Household Median Size" TEXT NULL,
        "Degree" TEXT NULL,
        "Zoom Level" TEXT NULL
    );
    TRUNCATE TABLE "schema-marketplace".household;

    INSERT INTO "schema-marketplace".household (
    "Location", "Household Average Size", "Household Median Size", 
    "Degree", "Zoom Level"
    )
    SELECT 
        "Location", "Household Average Size", "Household Median Size", 
        "Degree", "Zoom Level"
    FROM "raw_schema-marketplace".household;
    """
        
def population():
    return """
    CREATE SCHEMA IF NOT EXISTS "schema-marketplace";
    CREATE TABLE IF NOT EXISTS "schema-marketplace".population (
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
    TRUNCATE TABLE "schema-marketplace".population ;
    

    INSERT INTO "schema-marketplace".population ("Location", "Degree", "Male Population", "Female Population", "Median Age (Male)", "Median Age (Female)", "Total Population", "Population Density", "Zoom Level")
    SELECT "Location", "Degree", "Male Population", "Female Population", "Median Age (Male)", "Median Age (Female)", "Total Population", "Population Density", "Zoom Level"
    FROM "raw_schema-marketplace".population;
    """     
