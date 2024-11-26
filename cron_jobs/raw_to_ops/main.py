import sys
import os
import json
from db_connection import DatabaseConnection
from transforms import AVAILABLE_TRANSFORMS


def apply_transformation(db_conn, transform_name):
    """Apply a specific transformation"""
    try:
        if transform_name not in AVAILABLE_TRANSFORMS:
            raise ValueError(f"Unknown transformation: {transform_name}")

        transform_functions = AVAILABLE_TRANSFORMS[transform_name]

        # Create table
        create_table_query = transform_functions["create_table"]()
        db_conn.execute_query(create_table_query)

        # Apply transformation
        transform_query = transform_functions["transform"]()
        db_conn.execute_query(transform_query)

        print(f"Successfully applied transformation: {transform_name}")

    except Exception as e:
        print(f"Error applying transformation {transform_name}: {e}")
        raise


def main():
    try:
        with open("cron_jobs/secrets_database.json", "r") as f:
            config = json.load(f)

        transfos = {
            "s-locator": ["dbo_opertional@marketplace_slocator"],
            "vivi_app": [
                "dbo-coffee@marketplace_products",
                # Add other transformations here as needed
            ],
        }

        connections = {}
        for server in transfos.keys():
            conn_info = config[server]["db"]

            # List of transformations to apply
            transformations_to_apply = transfos[server]

            if transformations_to_apply:
                # Apply each transformation
                for transform in transformations_to_apply:
                    db_name, transform_name = transform.split("@")
                    conn_info["dbname"] = db_name

                    if server + db_name not in connections:
                        connections[server + db_name] = DatabaseConnection(conn_info)

                    conn = connections[server + db_name]

                    print(f"\nApplying transformation: {transform}")
                    apply_transformation(conn, transform_name)

    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
