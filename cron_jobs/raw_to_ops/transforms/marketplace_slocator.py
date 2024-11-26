def create_table_real_estate():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS "schema-marketplace";
    
    -- Create table if it doesn't exist
    CREATE TABLE IF NOT EXISTS "schema-marketplace".real_estate (
        url TEXT PRIMARY KEY NOT NULL,
        price varchar(25) NULL
    );

    -- Truncate the table to ensure clean data
    TRUNCATE TABLE "schema-marketplace".real_estate ;
    """

def transformation_real_estate():
    return """
    INSERT INTO "schema-marketplace".real_estate 
    SELECT url, price FROM "raw_schema-marketplace".real_estate ;
    """