from . import marketplace_products
from . import marketplace_slocator

# Import other transforms here as they're added

AVAILABLE_TRANSFORMS = {
    "marketplace_products": {
        "create_table": marketplace_products.get_create_table_query,
        "transform": marketplace_products.get_transformation_query,
    },
    "marketplace_slocator": {
        "create_table": marketplace_slocator.create_table_real_estate,
        "transform": marketplace_slocator.transformation_real_estate,
    },
    # Add other transforms here as they're created
}
