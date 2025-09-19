import httpx

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
            "income": False
        }
    }
    headers = {"Authorization": f"Bearer {id_token}"} if id_token else {}
    with httpx.Client() as client:
        response = client.post(url, json=payload, headers=headers)
        data = response.json()

    features = data.get("data", {}).get("features", [])
    # Return zeros values in case of an empty dict
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

    # Add derived percentages based on median age logic
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

