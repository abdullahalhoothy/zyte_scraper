import os
import csv
import json
import requests
from datetime import datetime


def swap_coordinates(nested_coords):
    def recursive_swap(coords):
        if isinstance(coords[0], (float, int)) and isinstance(coords[1], (float, int)):
            return [coords[1], coords[0]]  # Swap [lat, lon] -> [lon, lat]
        return [recursive_swap(inner) for inner in coords]

    return recursive_swap(nested_coords)

def convert_columnar_to_geojson(data, coordinates_list):
    area_names = data["Area Name"]
    num_rows = len(area_names)

    # Resulting feature collection
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # Iterate row-wise
    for i in range(num_rows):
        properties = {}
        for key, value_list in data.items():
            val = value_list[i] if i < len(value_list) else None
            # Convert "" to None or 0 as appropriate
            if val == "":
                val = 0
            # Try to convert numeric strings
            if isinstance(val, str):
                try:
                    if "%" in val:
                        val = val  # Keep as percentage string
                    else:
                        val = float(val)
                except:
                    pass

            properties[key] = val

        # Add required fields (customize as needed)
        feature = {
            "type": "Feature",
            "properties": {
                "id": properties["id"],  # unique ID
                "name": properties["name"],
                "type": properties["type"],
                "Area Name": properties["Area Name"],
                **properties
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": coordinates_list[i]
            }
        }
        geojson["features"].append(feature)

    return geojson


# Prepare final output dictionary
outputJson = {
    "Area Name": [],
    "Total Population": [],
    "Total Males": [],
    "Total Females": [],
    "Total Saudis": [],
    "Total Non-saudis": [],
    "Saudis population (%)": [],
    "Male population (%)": [],
    "Female population (%)": [],

    # New Income Keys
    "Overall Average Income": [],
    "Average Male Income": [],
    "Average Female Income": [],
    "Average Saudi Income": [],
    "Average Non-Saudi Income": [],
    "Average Saudi Male Income": [],
    "Average Saudi Female Income": [],
    "Average Non-Saudi Male Income": [],
    "Average Non-Saudi Female Income": [],
}

area_list = ['emirate-1', 'city-3']
area_ids = []
coordinates = []
name = []
area_type = []



try:
    url = "https://api.map.910ths.sa/api/graphql/"
    headers = {
        'Content-Type': 'application/json'
    }
    query = """
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

    payload = json.dumps({
        "operationName": "getIncomeQuery",
        "variables": {
            "areas": area_list
        },
        "query": query
    })
    
    response = requests.post(url, headers=headers, data=payload)
    areas = response.json()["data"]["all"]["facts"]
    overall_income =  response.json()["data"]["all"]["facts"]
    males_income = response.json()["data"]["male"]["facts"]
    females_income = response.json()["data"]["female"]["facts"]
    saudi_income = response.json()["data"]["saudi"]["facts"]
    nonSaudi_income = response.json()["data"]["nonSaudi"]["facts"]
    saudiMale_income = response.json()["data"]["saudiMale"]["facts"]
    saudiFemale_income = response.json()["data"]["saudiFemale"]["facts"]
    nonSaudiMale_income = response.json()["data"]["nonSaudiMale"]["facts"]
    nonSaudiFemale_income = response.json()["data"]["nonSaudiFemale"]["facts"]

    print("Total Areas: {}".format(len(areas)))

    # Fetch demographic data per area
    for idx, data in enumerate(areas):
        all_average_income = 0
        average_male_income = 0
        average_female_income = 0
        average_saudi_income = 0
        average_non_saudi_income = 0
        average_saudi_male_income = 0
        average_saudi_female_income = 0
        average_non_saudi_male_income = 0
        average_non_saudi_female_income = 0

        area_id = data["area"]["id"]
        area_name = data["area"]["name"]
        total_income = data["value"]

        ## geting area codinates

        query2 = """
          query getAreaShape($areaId: String!, $epsilon: Float!) {
            area(id: $areaId) {
              id
              name(language: "ar")
              type
              simplifiedShape(epsilon: $epsilon)
            }
          }
          """

        payload_data = json.dumps({
              "operationName": "getAreaShape",
              "variables": {
                  "areaId": area_id,
                  "epsilon": 0.0000025
              },
              "query": query2
          })

        response_data = requests.post(url, headers=headers, data=payload_data)
        json_data = response_data.json()['data']
        coordinates.extend(json_data['area'].get("simplifiedShape", []))
        name.append(json_data['area'].get("name", " "))
        area_type.append(json_data['area'].get("type", " "))
        area_ids.append(area_id)


        for all_avg_income in overall_income:
            if area_name == all_avg_income.get("area", []).get('name'):
                all_average_income = all_avg_income.get('value', 0)

        for avg_male_income in males_income:
            if area_name == avg_male_income.get("area", []).get('name'):
                average_male_income = avg_male_income.get('value', 0)
        for avg_female_income in females_income:
            if area_name == avg_female_income.get("area", []).get('name'):
                average_female_income = avg_female_income.get('value', 0)

        for avg_saudi_income in saudi_income:
            if area_name == avg_saudi_income.get("area", []).get('name'):
                average_saudi_income = avg_saudi_income.get('value', 0)
        for avg_nonSaudi_income in nonSaudi_income:
            if area_name == avg_nonSaudi_income.get("area", []).get('name'):
                average_non_saudi_income  = avg_nonSaudi_income.get('value', 0)


        for avg_saudi_male_income in saudiMale_income:
            if area_name == avg_saudi_male_income.get("area", []).get('name'):
                average_saudi_male_income  = avg_saudi_male_income.get('value', 0)
        for avg_saudi_female_income in saudiFemale_income:
            if area_name == avg_saudi_female_income.get("area", []).get('name'):
                average_saudi_female_income  = avg_saudi_female_income.get('value', 0)

        for avg_nonSaudiMale_income in nonSaudiMale_income:
            if area_name == avg_nonSaudiMale_income.get("area", []).get('name'):
                average_non_saudi_male_income = avg_nonSaudiMale_income.get('value', 0)
        for avg_nonSaudiFemale_income in nonSaudiFemale_income:
            if area_name == avg_nonSaudiFemale_income.get("area", []).get('name'):
                average_non_saudi_female_income  = avg_nonSaudiFemale_income.get('value', 0)

        print(f"Processing Area: {area_name}")
        outputJson["Area Name"].append(area_name)

        payload_demo = json.dumps({
            "operationName": "getDemographicData",
            "variables": {
                "areas": [area_id]
            },
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
            """
        })

        demo_response = requests.post(url, headers=headers, data=payload_demo)
        demo_data = demo_response.json().get("data", {})


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

        outputJson["Total Population"].append(total)
        outputJson["Total Males"].append(males)
        outputJson["Total Females"].append(females)
        outputJson["Total Saudis"].append(saudis)
        outputJson["Total Non-saudis"].append(non_saudis)
        outputJson["Male population (%)"].append(f"{round((males / total) * 100, 2) if total else 0}%")
        outputJson["Female population (%)"].append(f"{round((females / total) * 100, 2) if total else 0}%")
        outputJson["Saudis population (%)"].append(f"{round((saudis / total) * 100, 2) if total else 0}%")
        outputJson["Overall Average Income"].append(all_average_income)
        outputJson["Average Male Income"].append(average_male_income)
        outputJson["Average Female Income"].append(average_female_income)

        outputJson["Average Saudi Income"].append(average_saudi_income)
        outputJson["Average Non-Saudi Income"].append(average_non_saudi_income)
        outputJson["Average Saudi Male Income"].append(average_saudi_male_income)
        outputJson["Average Saudi Female Income"].append(average_saudi_female_income)
        outputJson["Average Non-Saudi Male Income"].append(average_non_saudi_male_income)
        outputJson["Average Non-Saudi Female Income"].append(average_non_saudi_female_income)

        for byGender in demo_data['byGenderAndAgeGroupPopulation']['facts']:
            if (byGender["splits"][0]['id'] + "_" + byGender["splits"][1]['id'] in outputJson.keys()):
                outputJson[byGender["splits"][0]['id'] + "_" + byGender["splits"][1]['id']].append(byGender["value"])
            else:
                outputJson[byGender["splits"][0]['id'] + "_" + byGender["splits"][1]['id']] = []
                outputJson[byGender["splits"][0]['id'] + "_" + byGender["splits"][1]['id']].append(byGender["value"])

        for byNation in demo_data['byNationalityAndAgeGroupPopulation']['facts']:
            if (byNation["splits"][0]['id'] + "_" + byNation["splits"][1]['id'] in outputJson.keys()):
                outputJson[byNation["splits"][0]['id'] + "_" + byNation["splits"][1]['id']].append(byNation["value"])
            else:
                outputJson[byNation["splits"][0]['id'] + "_" + byNation["splits"][1]['id']] = []
                outputJson[byNation["splits"][0]['id'] + "_" + byNation["splits"][1]['id']].append(byNation["value"])

except (Exception, ValueError) as e:
    print("Error", e)

finally:
    if outputJson:
        os.makedirs("output_csv_files", exist_ok=True)
        os.makedirs("output_geo_json_files", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_csv = f"output_csv_files/demographic_data_{timestamp}.csv"
        filename_json = f"output_geo_json_files/Output_data_{timestamp}.json"

        # Dynamically collect all keys (including dynamically added ones)
        all_keys = list(outputJson.keys())

        # Ensure all value lists have the same length
        max_len = max(len(v) for v in outputJson.values())
        for key in all_keys:
            while len(outputJson[key]) < max_len:
                outputJson[key].append('')  # Fill missing data with empty strings

        # Write to CSV
        with open(filename_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([key.capitalize().replace("_", " ") for key in all_keys])
            rows = zip(*[outputJson[key] for key in all_keys])
            writer.writerows(rows)
        print(f"\n📁 Saved collected Data to: {filename_csv}")

        outputJson['id'] = area_ids
        outputJson['name'] = name
        outputJson['type'] = area_type
        swapped_coords = swap_coordinates(coordinates)
        geo_Json_data = convert_columnar_to_geojson(outputJson, swapped_coords)

        with open(filename_json, "w", encoding="utf-8") as f:
            json.dump(geo_Json_data, f, ensure_ascii=False, indent=4)
        print(f"\n📁 Saved collected Data to Geo-json file: {filename_json}")



