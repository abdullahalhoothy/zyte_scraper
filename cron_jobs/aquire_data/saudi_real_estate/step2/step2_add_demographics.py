import httpx
import json
from typing import Dict
import psycopg2
from psycopg2.extras import RealDictCursor
import os

def pct_above(age, avg_median_age):
    diff = age - avg_median_age
    if diff <= 0:
        return 50.0
    pct = 50.0 - (diff * 2.5)
    return max(pct, 0.0)


def generate_bbox(center_lat, center_lng, radius_km=1):
    delta = radius_km / 111
    return {
        "bottom_lng": center_lng - delta,
        "top_lng": center_lng + delta,
        "bottom_lat": center_lat - delta,
        "top_lat": center_lat + delta,
    }

def login_and_get_user():
    login_url = "http://37.27.195.216:8000/fastapi/login"
    login_payload = {
        "message": "login",
        "request_info": {},
        "request_body": {
            "email": "u_je_u2008@live.com",
            "password": "12351235"
        }
    }
    with httpx.Client() as client:
        response = client.post(login_url, json=login_payload)
        data = response.json()
    user_id = data.get("data", {}).get("localId")
    id_token = data.get("data", {}).get("idToken")
    return user_id, id_token

def fetch_demographics(center_lat, center_lng, user_id, id_token, radius_km=1):

    bbox = generate_bbox(center_lat, center_lng, radius_km)
    url = "http://37.27.195.216:8000/fastapi/fetch_population_by_viewport"
    headers = {"Authorization": f"Bearer {id_token}"} if id_token else {}
    with httpx.Client() as client:
        payload = {
            "message": "fetch population",
            "request_info": {},
            "request_body": {
                "top_lng": bbox["top_lng"],
                "top_lat": bbox["top_lat"],
                "bottom_lng": bbox["bottom_lng"],
                "bottom_lat": bbox["bottom_lat"],
                "zoom_level": 12,
                "user_id": user_id,
                "population": True,
                "income": True
            }
        }
        response = client.post(url, json=payload, headers=headers)
        data = response.json()

    features = data.get("data", {}).get("features", [])

    if not features:
        return {
            "total_population": 0,
            "avg_density": 0.0,
            "avg_median_age": 0.0,
            "avg_income": 0.0,
            "percentage_age_above_20": 0.0,
            "percentage_age_above_25": 0.0,
            "percentage_age_above_30": 0.0,
            "percentage_age_above_35": 0.0,
            "percentage_age_above_40": 0.0,
            "percentage_age_above_45": 0.0,
            "percentage_age_above_50": 0.0
        }

    total_population = 0
    pop_density_values = []
    age_values = []
    income_values = []
    for f in features:
        props = f.get("properties", {})
        total_population += props.get("Population_Count", 0)
        pop_density_values.append(props.get("Population_Density_KM2", 0))
        age_values.append(props.get("Median_Age_Total", 0))
        income_values.append(props.get("income", 0))

    processed = {
        "total_population": total_population,
        "avg_density": round((sum(pop_density_values) / len(pop_density_values)), 2) if pop_density_values else 0,
        "avg_median_age": round((sum(age_values) / len(age_values)), 2) if age_values else 0,
        "avg_income": round((sum(income_values) / len(income_values)), 2) if income_values else 0,
    }

    avg_median_age = processed.get("avg_median_age", 0)
    processed.update({
        "percentage_age_above_20": pct_above(20, avg_median_age),
        "percentage_age_above_25": pct_above(25, avg_median_age),
        "percentage_age_above_30": pct_above(30, avg_median_age),
        "percentage_age_above_35": pct_above(35, avg_median_age),
        "percentage_age_above_40": pct_above(40, avg_median_age),
        "percentage_age_above_45": pct_above(45, avg_median_age),
        "percentage_age_above_50": pct_above(50, avg_median_age),
    })

    return processed


if __name__ == "__main__":
    # latitude	longitude
    # 24.784202	46.747732
   user_id, id_token = login_and_get_user()
   demographics = fetch_demographics(24.784202, 46.747732, user_id, id_token)
   print(demographics)


def _read_db_config():
    """Read DB credentials from cron_jobs/secrets_database.json -> dev-s-locator."""
    secrets_path = r"cron_jobs\secrets_database.json"
    with open(secrets_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    # Use dev-s-locator by default (matches local/dev in repo)
    cfg = data.get("dev-s-locator", {}).get("db", {})
    return cfg


def fetch_household_from_db(center_lat: float, center_lng: float, radius_km: float = 1) -> Dict:
    """
    Query Postgres household_all_features_v12 for features within a square bbox around the center point.
    Returns aggregated household statistics compatible with demographics result shape.

    Returns dict with keys:
      total_households, avg_household_size, median_household_size, density_sum, features_count
    """
    cfg = _read_db_config()
    conn = None
    bbox = generate_bbox(center_lat, center_lng, radius_km)
    # Build simple bbox geometry query using ST_MakeEnvelope assuming geometry uses lon/lat
    sql = f"""
    SELECT "Household_Average_Size", "Household_Median_Size", density
    FROM schema_marketplace.household_all_features_v12
    WHERE geometry && ST_MakeEnvelope({bbox['bottom_lng']}, {bbox['bottom_lat']}, {bbox['top_lng']}, {bbox['top_lat']}, 4326)
    """
    results = []
    try:
        conn = psycopg2.connect(
            dbname=cfg.get("dbname"),
            user=cfg.get("user"),
            password=cfg.get("password"),
            host=cfg.get("host"),
            port=cfg.get("port"),
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            for r in rows:
                results.append(r)
    finally:
        if conn:
            conn.close()

    if not results:
        return {
            "total_households": 0,
            "avg_household_size": 0.0,
            "median_household_size": 0.0,
            "density_sum": 0.0,
            "features_count": 0,
        }

    # Aggregate
    total_households = len(results)
    avg_sizes = [r.get("Household_Average_Size") or 0 for r in results]
    median_sizes = [r.get("Household_Median_Size") or 0 for r in results]
    densities = [r.get("density") or 0 for r in results]

    aggregated = {
        "total_households": total_households,
        "avg_household_size": round(sum(avg_sizes) / len(avg_sizes), 2) if avg_sizes else 0.0,
        "median_household_size": round(sum(median_sizes) / len(median_sizes), 2) if median_sizes else 0.0,
        "density_sum": round(sum(densities), 2),
        "features_count": len(results),
    }
    return aggregated
