import sys
import os
import json
from db_connection import DatabaseConnection
import importlib.util
import inspect
import logging
import argparse
import sys
parser = argparse.ArgumentParser()
parser.add_argument("--log-file", help="Path to shared log file", required=False)
args = parser.parse_args()


if(args.log_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    sys.path.append(grandparent_dir)
    from logging_utils import setup_logging
    setup_logging(args.log_file)
    
def get_module_functions(module_name: str, base_path: str = "cron_jobs/step5_raw_to_ops/transforms"):
    full_path = os.path.join(base_path, f"{module_name}.py")
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    functions = [
        obj for name, obj in inspect.getmembers(module)
        if inspect.isfunction(obj) and obj.__module__ == module.__name__
    ]
    
    return functions

def apply_transformation(db_conn, transform_name):
    """Apply a specific transformation"""
    try:
        # if transform_name not in AVAILABLE_TRANSFORMS:
        #     raise ValueError(f"Unknown transformation: {transform_name}")

        # transform_functions = AVAILABLE_TRANSFORMS[transform_name]
        functions = get_module_functions(transform_name)
        for func in functions:
            logging.info(f"beginning function: {func.__name__} ")
            query = func()
            db_conn.execute_query(query)
            logging.info(f"Successfully applied function: {func.__name__}")

        logging.info(f"Successfully applied transformation: {transform_name}")

    except Exception as e:
        logging.info(f"Error applying transformation {transform_name}: {e}")
        raise


def main():
    with open("cron_jobs/secrets_database.json", "r") as f:
        config = json.load(f)

    transfos = {
        "s-locator": ["dbo_operational@marketplace_slocator"],
        "dev-s-locator": ["dbo_operational@marketplace_slocator"]
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

                logging.info(f"\nApplying transformation: {transform}")
                apply_transformation(conn, transform_name)




if __name__ == "__main__":
    main()
