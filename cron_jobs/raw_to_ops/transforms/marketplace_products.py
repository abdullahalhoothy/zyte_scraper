
def get_create_table_query():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS schema_marketplace;
    
    -- Create table if it doesn't exist
    CREATE TABLE IF NOT EXISTS schema_marketplace.products (
        id TEXT PRIMARY KEY NOT NULL,
        name varchar(500) NOT NULL,
        description text NULL,
        tagline text NULL,
        producturl varchar(500) NULL,
        imageurl varchar(500) NULL,
        averagerating varchar(25) NULL,
        totalratings varchar(25) NULL,
        discountedPrice varchar(25) NULL,
        discountPercentage varchar(25) NULL,
        originalPrice varchar(25) NULL,
        city varchar(30) NULL,
        country varchar(30) NULL,
        userRating JSONB NULL
    );

    -- Truncate the table to ensure clean data
    TRUNCATE TABLE schema_marketplace.products;
    """

def get_transformation_query():
    return """
WITH product_data AS (
    SELECT
        md5(random()::text || clock_timestamp()::text)::text as id,
        COALESCE("Product Name", '') as name,
        NULLIF("Product Description", '') as description,
        NULLIF("Product Details", '') as tagline,
        NULLIF("Image 1 Link", '') as producturl,
        NULLIF("Image 2 Link", '') as imageurl,
        '4.2' as averagerating,
        '500' as totalratings,
        NULLIF("After Sale", 0) as discountedPrice,
        '32%' as discountPercentage,
        NULLIF("Original Price", 0) as originalPrice,
        'Barolo' as city,
        'Italy' as country,
        '{
            "description": "Clear deep ruby in color with medium intensity",
            "rating": "4.0",
            "review": "Good product",
            "username": "Default Reviewer",
            "userimageurl": "default_image_url"
        }'::jsonb as userRating
    FROM raw_schema_marketplace.products
    )
    INSERT INTO schema_marketplace.products
    SELECT 
        id,
        name,
        description,
        tagline,
        producturl,
        imageurl,
        averagerating,
        totalratings,
        COALESCE(discountedPrice, originalPrice * 0.85) as discountedPrice,
        CASE 
            WHEN discountedPrice IS NULL THEN '15%'
            ELSE discountPercentage
        END as discountPercentage,
        originalPrice,
        city,
        country,
        userRating
    FROM product_data;
        """


def create_table_banners():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS schema_app_generic;
    
    -- Create table if it doesn't exist
    CREATE TABLE IF NOT EXISTS schema_app_generic.banners (
        id TEXT PRIMARY KEY NOT NULL,
        file_name varchar(500) NOT NULL,
        url varchar(500) NULL
    );

    -- Truncate the table to ensure clean data
    TRUNCATE TABLE schema_app_generic.banners;
    """

def transformation_banners():
    return """
    INSERT INTO schema_app_generic.banners
    SELECT * FROM raw_schema_app_generic.banners;
    """