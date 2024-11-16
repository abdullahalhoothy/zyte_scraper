from . import marketplace_products
# Import other transforms here as they're added

AVAILABLE_TRANSFORMS = {
    'marketplace_products': {
        'create_table': marketplace_products.get_create_table_query,
        'transform': marketplace_products.get_transformation_query
    }
    # Add other transforms here as they're created
}