def get_transformation_query():
    return """
    INSERT INTO "schema-marketplace".products
    SELECT 
        md5(random()::text || clock_timestamp()::text)::text as id,
        COALESCE("Product Name", '') as name,
        NULLIF("Product Description", '') as description,
        NULLIF("Product Details", '') as tagline,
        NULLIF("Image 1 Link", '') as producturl, 
        NULLIF("Image 2 Link", '') as imageurl,
        '4.3' as ratingtext,
        '4.1' as ratingvalue, 
        '4.2' as averagerating,
        '500' as totalratings,
        NULLIF("After Sale", 0) as discountedPrice,
        '32%' as discountPercentage,
        NULLIF("Original Price", 0) as originalPrice,
        'Barolo' as city,
        'Italy' as country, 
        'https://imageicon' as countryflagurl,
        '{
            "description": "Clear deep ruby in color with medium intensity",
            "rating": "4.0",
            "review": "Good product",
            "username": "Default Reviewer", 
            "userimageurl": "default_image_url"
        }'::jsonb as userRating
    FROM "raw_schema-marketplace".products;
    """

def get_create_table_query():
    return """
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS "schema-marketplace";
    
    -- Create table if it doesn't exist
    CREATE TABLE IF NOT EXISTS "schema-marketplace".products (
        id TEXT PRIMARY KEY NOT NULL,
        name varchar(500) NOT NULL,
        description text NULL,
        tagline text NULL,
        producturl varchar(500) NULL,
        imageurl varchar(500) NULL,
        ratingtext varchar(10) NULL,
        ratingvalue varchar(10) NULL,
        averagerating varchar(10) NULL,
        totalratings varchar(10) NULL,
        discountedPrice varchar(10) NULL,
        discountPercentage varchar(10) NULL,
        originalPrice varchar(10) NULL,
        city varchar(30) NULL,
        country varchar(30) NULL,
        countryflagurl varchar(500) NULL,
        userRating JSONB NULL
    );

    -- Truncate the table to ensure clean data
    TRUNCATE TABLE "schema-marketplace".products;
    """