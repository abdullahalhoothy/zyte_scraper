import os
import csv
import json
import requests
from datetime import datetime
import logging
import argparse
import sys
parser = argparse.ArgumentParser()
parser.add_argument("--log-file", help="Path to shared log file", required=False)
args = parser.parse_args()


if(args.log_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    grandparent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
    sys.path.append(grandparent_dir)
    from logging_utils import setup_logging
    setup_logging(args.log_file)

def swap_coordinates(nested_coords):
    def recursive_swap(coords):
        if isinstance(coords[0], (float, int)) and isinstance(
            coords[1], (float, int)
        ):
            return [coords[1], coords[0]]  # Swap [lat, lon] -> [lon, lat]
        return [recursive_swap(inner) for inner in coords]

    return recursive_swap(nested_coords)


area_list = [
    # "emirate-1", #eastern region
    "city-3" #riyadh
]

# Change from lists to dictionary with area_id as key
area_data = {}  # This will store all data by area_id
geojson_features = []  # This will store the final GeoJSON features

url = "https://api.map.910ths.sa/api/graphql/"
headers = {"Content-Type": "application/json"}
query_all_areas_income = """
query getIncomeQuery($areas: [String]!) {
  all: averageIncome(filters: {male: null, saudi: null, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  male: averageIncome(filters: {male: true, saudi: null, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  female: averageIncome(filters: {male: false, saudi: null, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  saudi: averageIncome(filters: {male: null, saudi: true, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  nonSaudi: averageIncome(filters: {male: null, saudi: false, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  saudiMale: averageIncome(filters: {male: true, saudi: true, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  saudiFemale: averageIncome(filters: {male: false, saudi: true, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  nonSaudiMale: averageIncome(filters: {male: true, saudi: false, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  nonSaudiFemale: averageIncome(filters: {male: false, saudi: false, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
}
"""

payload = json.dumps(
    {
        "operationName": "getIncomeQuery",
        "variables": {"areas": area_list},
        "query": query_all_areas_income,
    }
)

response = requests.post(url, headers=headers, data=payload)
areas = response.json()["data"]["all"]["facts"]
overall_income = response.json()["data"]["all"]["facts"]
males_income = response.json()["data"]["male"]["facts"]
females_income = response.json()["data"]["female"]["facts"]
saudi_income = response.json()["data"]["saudi"]["facts"]
nonSaudi_income = response.json()["data"]["nonSaudi"]["facts"]
saudiMale_income = response.json()["data"]["saudiMale"]["facts"]
saudiFemale_income = response.json()["data"]["saudiFemale"]["facts"]
nonSaudiMale_income = response.json()["data"]["nonSaudiMale"]["facts"]
nonSaudiFemale_income = response.json()["data"]["nonSaudiFemale"]["facts"]

logging.info("Total Areas: {}".format(len(areas)))

# Convert income data to dictionaries for easier lookup by area name
income_data = {
    "all": {item["area"]["name"]: item["value"] for item in overall_income},
    "male": {item["area"]["name"]: item["value"] for item in males_income},
    "female": {item["area"]["name"]: item["value"] for item in females_income},
    "saudi": {item["area"]["name"]: item["value"] for item in saudi_income},
    "nonSaudi": {item["area"]["name"]: item["value"] for item in nonSaudi_income},
    "saudiMale": {item["area"]["name"]: item["value"] for item in saudiMale_income},
    "saudiFemale": {item["area"]["name"]: item["value"] for item in saudiFemale_income},
    "nonSaudiMale": {item["area"]["name"]: item["value"] for item in nonSaudiMale_income},
    "nonSaudiFemale": {item["area"]["name"]: item["value"] for item in nonSaudiFemale_income},
}

# Fetch demographic data per area
for idx, data in enumerate(areas):
    area_id = data["area"]["id"]
    area_name = data["area"]["name"]
    
    logging.info(f"Processing Area: {area_name}")

    # Initialize area data dictionary
    area_properties = {
        "id": area_id,
        "Area Name": area_name,
        "Overall Average Income": income_data["all"].get(area_name, 0),
        "Average Male Income": income_data["male"].get(area_name, 0),
        "Average Female Income": income_data["female"].get(area_name, 0),
        "Average Saudi Income": income_data["saudi"].get(area_name, 0),
        "Average Non-Saudi Income": income_data["nonSaudi"].get(area_name, 0),
        "Average Saudi Male Income": income_data["saudiMale"].get(area_name, 0),
        "Average Saudi Female Income": income_data["saudiFemale"].get(area_name, 0),
        "Average Non-Saudi Male Income": income_data["nonSaudiMale"].get(area_name, 0),
        "Average Non-Saudi Female Income": income_data["nonSaudiFemale"].get(area_name, 0),
    }

    # Get area coordinates and metadata
    get_area_shape = """
      query getAreaShape($areaId: String!, $epsilon: Float!) {
        area(id: $areaId) {
          id
          name(language: "ar")
          type
          simplifiedShape(epsilon: $epsilon)
        }
      }
      """

    payload_data = json.dumps(
        {
            "operationName": "getAreaShape",
            "variables": {"areaId": area_id, "epsilon": 0.0000025},
            "query": get_area_shape,
        }
    )

    response_data = requests.post(url, headers=headers, data=payload_data)
    json_data = response_data.json()["data"]
    # This checks if geometry exists or not
    if(json_data["area"]["simplifiedShape"]):
      # Get coordinates and swap them
      if len(json_data["area"].get("simplifiedShape", []))>2:
          # manually verify which shapes are being sent
          pause=1
      raw_coordinates = json_data["area"].get("simplifiedShape", [])[0]
      swapped_coordinates = swap_coordinates(raw_coordinates) if raw_coordinates else []
      
      area_properties["name"] = json_data["area"].get("name", "")
      area_properties["type"] = json_data["area"].get("type", "")

      # Get demographic data
      payload_demo = json.dumps(
          {
              "operationName": "getDemographicData",
              "variables": {"areas": [area_id]},
              "query": """
          query getDemographicData($areas: [String]!) {
              totalPopulation: population(filters: {areas: $areas}, splits: []) {
                  facts { value }
              }
              malePopulation: population(filters: {areas: $areas, sexes: ["male"]}, splits: []) {
                  facts { value }
              }
              femalePopulation: population(filters: {areas: $areas, sexes: ["female"]}, splits: []) {
                  facts { value }
              }
              saudiPopulation: population(filters: {areas: $areas, nationalities: ["saudi"]}, splits: []) {
                  facts { value }
              }
              nonSaudiPopulation: population(filters: {areas: $areas, nationalities: ["nonSaudi"]}, splits: []) {
                  facts { value }
              }

              byGenderAndAgeGroupPopulation: population(filters: {areas: $areas}, splits: ["sex", "ageGroup"]) {
                  facts {
                    splits {
                      id
                    }
                    value
                  }
              }
              byNationalityAndAgeGroupPopulation: population(filters: {areas: $areas}, splits: ["nationality", "ageGroup"]) {
                  facts {
                    splits {
                      id
                    }
                    value
                  }
              }
              male: averageIncome(filters: {male: true, saudi: null, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
              facts {
                area {
                  id
                  name(language: "ar")
                }
                value
              }
            }

          }
          """,
          }
      )

      demo_response = requests.post(url, headers=headers, data=payload_demo)
      demo_data = demo_response.json().get("data", {})
    else:
        logging.warning(f'Skipping feature: No geometry found for {json_data["area"]["name"]}')

    def extract_value(key):
        try:
            return demo_data.get(key, {}).get("facts", [{}])[0].get("value", 0)
        except (IndexError, TypeError):
            return 0

    total = extract_value("totalPopulation")
    males = extract_value("malePopulation")
    females = extract_value("femalePopulation")
    saudis = extract_value("saudiPopulation")
    non_saudis = extract_value("nonSaudiPopulation")

    # Add demographic data to properties
    area_properties.update({
        "Total Population": total,
        "Total Males": males,
        "Total Females": females,
        "Total Saudis": saudis,
        "Total Non-saudis": non_saudis,
        "Male population (%)": f"{round((males / total) * 100, 2) if total else 0}%",
        "Female population (%)": f"{round((females / total) * 100, 2) if total else 0}%",
        "Saudis population (%)": f"{round((saudis / total) * 100, 2) if total else 0}%",
    })

    # Add dynamic age group data
    for byGender in demo_data["byGenderAndAgeGroupPopulation"]["facts"]:
        key = byGender["splits"][0]["id"] + "_" + byGender["splits"][1]["id"]
        area_properties[key] = byGender["value"]

    for byNation in demo_data["byNationalityAndAgeGroupPopulation"]["facts"]:
        key = byNation["splits"][0]["id"] + "_" + byNation["splits"][1]["id"]
        area_properties[key] = byNation["value"]

    # Create GeoJSON feature directly
    if swapped_coordinates and area_id != "city-3":
        feature = {
            "type": "Feature",
            "properties": area_properties,
            "geometry": {
                "type": "Polygon",
                "coordinates": swapped_coordinates
            }
        }
        geojson_features.append(feature)

# Create final GeoJSON
final_geojson = {
    "type": "FeatureCollection",
    "features": geojson_features
}

# Save to file
if geojson_features:
    os.makedirs("zad_output_geo_json_files", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    census_path = r"F:\git\zyte_scraper\cron_jobs\aquire_data\saudi_income_data"
    # filename_json = os.path.join(
    #     census_path,
    #     "zad_output_geo_json_files",
    #     f"Output_data_{timestamp}.geojson",
    # )
    filename_json = os.path.join(
        census_path,
        "zad_output_geo_json_files",
        f"Output_data.geojson",
    )

    with open(filename_json, "w", encoding="utf-8") as f:
        json.dump(final_geojson, f, ensure_ascii=False, indent=4)
    logging.info(f"\n📁 Saved collected Data to Geo-json file: {filename_json}")