import sys
from db_connection import DatabaseConnection
from transforms import AVAILABLE_TRANSFORMS

def apply_transformation(db_conn, transform_name):
    """Apply a specific transformation"""
    try:
        if transform_name not in AVAILABLE_TRANSFORMS:
            raise ValueError(f"Unknown transformation: {transform_name}")

        transform_functions = AVAILABLE_TRANSFORMS[transform_name]
        
        # Create table
        create_table_query = transform_functions['create_table']()
        db_conn.execute_query(create_table_query)
        
        # Apply transformation
        transform_query = transform_functions['transform']()
        db_conn.execute_query(transform_query)
        
        print(f"Successfully applied transformation: {transform_name}")
        
    except Exception as e:
        print(f"Error applying transformation {transform_name}: {e}")
        raise

def main():
    try:
        # Initialize database connection
        with DatabaseConnection("cron_jobs/raw_to_ops/secrets_database.json") as db_conn:
            # List of transformations to apply
            transformations_to_apply = [
                'marketplace_products',
                # Add other transformations here as needed
            ]

            # Apply each transformation
            for transform_name in transformations_to_apply:
                print(f"\nApplying transformation: {transform_name}")
                apply_transformation(db_conn, transform_name)

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()