import httpx

def generate_bbox(center_lat, center_lng, radius_km=1):
    delta = radius_km / 111
    return {
        "bottom_lng": center_lng - delta,
        "top_lng": center_lng + delta,
        "bottom_lat": center_lat - delta,
        "top_lat": center_lat + delta,
    }

async def fetch_demographics(center_lat, center_lng, radius_km=1):

    bbox = generate_bbox(center_lat, center_lng, radius_km)
    user_id = "JnaGDCKoSoWtj6NWEVW8MDMBCiA2"
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
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        data = response.json()

    features = data.get("features", [])
    ## Return zeros values in case of an empty dict
    if not features:
        return {
            "total_population": 0,
            "avg_density": 0.0,  # Half of MAX_DENSITY from scoring
            "avg_median_age": 0.0,
            "avg_income": 0.0,   # Half of MAX_INCOME from scoring
            "percentage_age_above_35": 0.0  # Half of max age percentage
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

    # Add derived percentages
    avg_median_age = processed.get("avg_median_age", 0)
    percentage_age_above_20 = avg_median_age - 20 + 50
    percentage_age_above_25 = avg_median_age - 25 + 50
    percentage_age_above_30 = avg_median_age - 30 + 50
    percentage_age_above_35 = avg_median_age - 35 + 50
    percentage_age_above_40 = avg_median_age - 40 + 50
    percentage_age_above_45 = avg_median_age - 45 + 50
    percentage_age_above_50 = avg_median_age - 50 + 50

    processed.update({
        "percentage_age_above_20": percentage_age_above_20,
        "percentage_age_above_25": percentage_age_above_25,
        "percentage_age_above_30": percentage_age_above_30,
        "percentage_age_above_35": percentage_age_above_35,
        "percentage_age_above_40": percentage_age_above_40,
        "percentage_age_above_45": percentage_age_above_45,
        "percentage_age_above_50": percentage_age_above_50,
    })

    return processed

