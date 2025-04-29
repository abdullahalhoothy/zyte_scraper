import os
import csv
import json
from pprint import pprint
import requests
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Prepare final output dictionary
outputData = []


total_male_income = 0
total_saudi_income = 0
total_female_income = 0
total_non_saudi_female = 0
total_non_saudi_income = 0
total_saudi_male_income = 0
total_non_saudi_male_income = 0
total_saudi_female_income = 0
try:
    url = "https://api.map.910ths.sa/api/graphql/"
    headers = {
        'Content-Type': 'application/json'
    }
    query1 = """
    query getIncomeQuery($areas: [String]!) {
      all: averageIncome(filters: {male: true, saudi: true, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
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
  
    # First region: Central
    payload_central = json.dumps({
        "operationName": "getIncomeQuery",
        "variables": {
            "areas": ["city-3"]
        },
        "query": query1
    })
    response = requests.post(url, headers=headers, data=payload_central, verify=False)
    areas = response.json()["data"]["all"]["facts"]
    males_income = response.json()["data"]["male"]["facts"]
    females_income = response.json()["data"]["female"]["facts"]

    saudi_income = response.json()["data"]["saudi"]["facts"]
    nonSaudi_income = response.json()["data"]["nonSaudi"]["facts"]
    saudiMale_income = response.json()["data"]["saudiMale"]["facts"]
    saudiFemale_income = response.json()["data"]["saudiFemale"]["facts"]
    nonSaudiMale_income = response.json()["data"]["nonSaudiMale"]["facts"]
    nonSaudiFemale_income = response.json()["data"]["nonSaudiFemale"]["facts"]

    # Second region: Eastern
    payload_eastern = json.dumps({
        "operationName": "getIncomeQuery",
        "variables": {
            "areas": ["emirate-1"]
        },
        "query": query1
    })
    response = requests.post(url, headers=headers, data=payload_eastern ,verify=False)
    areas += response.json()["data"]["all"]["facts"]
    males_income += response.json()["data"]["male"]["facts"]
    females_income += response.json()["data"]["female"]["facts"]

    saudi_income += response.json()["data"]["saudi"]["facts"]
    nonSaudi_income += response.json()["data"]["nonSaudi"]["facts"]
    saudiMale_income += response.json()["data"]["saudiMale"]["facts"]
    saudiFemale_income += response.json()["data"]["saudiFemale"]["facts"]
    nonSaudiMale_income += response.json()["data"]["nonSaudiMale"]["facts"]
    nonSaudiFemale_income += response.json()["data"]["nonSaudiFemale"]["facts"]

    print("Total Areas: {}".format(len(areas)))

    # Fetch demographic data per area
    for idx, data in enumerate(areas):
        
        outputJson = {
            "type": "FeatureCollection",
            "features": [
          {
          "type": "Feature",
          "properties": {
          "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
          "name": "صلاح الدين",
          "type": "district",

            "Area Name": "",
            "Total Population": "",
            "Total Males": "",
            "Total Females": "",
            "Total Saudis": "",
            "Total Non-saudis": "",
            "Saudis population (%)": "",
            "Male population (%)": "",
            "Female population (%)": "",

            # New Income Keys
            "Overall Average Income": "",
            "Average Male Income": "",
            "Average Female Income": "",
            "Average Saudi Income": "",
            "Average Non-Saudi Income": "",
            "Average Saudi Male Income": "",
            "Average Saudi Female Income": "",
            "Average Non-Saudi Male Income": "",
            "Average Non-Saudi Female Income": "",
            },
            "geometry": { 
              "type": "Polygon",
              "coordinates":[] 
        }
                     
            }],
        }
        area_id = data["area"]["id"]
        area_name = data["area"]["name"]
        total_income = data["value"]
        for idx, income in enumerate(response.json()["data"]):
            if len(males_income) >= idx and males_income[idx]["area"].get("id") == area_id:
                 total_male_income = males_income[idx].get("value", 0)
            if len(females_income) >= idx and females_income[idx]["area"].get("id") == area_id:
                 total_female_income = females_income[idx].get("value", 0)
            if len(saudi_income) >= idx and saudi_income[idx]["area"].get("id") == area_id:
                  total_saudi_income = saudi_income[idx].get("value", 0)

            if len(nonSaudi_income) >= idx and nonSaudi_income[idx]["area"].get("id") == area_id:
                total_non_saudi_income = nonSaudi_income[idx].get("value", 0)

        if len(saudiMale_income) >= idx and saudiMale_income[idx]["area"].get("id") == area_id:
           total_saudi_male_income = saudiMale_income[idx].get("value", 0)
        if len(saudiFemale_income) >= idx and saudiFemale_income[idx]["area"].get("id") == area_id:
           total_saudi_female_income = saudiFemale_income[idx].get("value", 0)
        if len(nonSaudiMale_income) >= idx and nonSaudiMale_income[idx]["area"].get("id") == area_id:
           total_non_saudi_male_income = nonSaudiMale_income[idx].get("value", 0)
        if len(nonSaudiFemale_income) >= idx and nonSaudiFemale_income[idx]["area"].get("id") == area_id:
           total_non_saudi_female = nonSaudiFemale_income[idx].get("value", 0)

        print(f"Processing Area: {area_name}")
        outputJson['features'][0]["properties"]["Area Name"]=area_name

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

        demo_response = requests.post(url, headers=headers, data=payload_demo,verify=False)
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

        if total > 0:
            average_income = round((total_income / total), 2)
            average_saudi_male_income = round((total_saudi_male_income / total), 2)
            average_saudi_female_income = round((total_saudi_female_income / total), 2)
            average_non_saudi_male_income = round((total_non_saudi_male_income / total), 2)
            average_non_saudi_female_income = round((total_non_saudi_female / total), 2)

        else:
            average_income = 0
            average_saudi_male_income = 0
            average_saudi_female_income = 0
            average_non_saudi_male_income = 0
            average_non_saudi_female_income = 0

        if males > 0:
            average_male_income = round((total_male_income / males), 2)
        else:
            average_male_income = 0

        if females > 0:
            average_female_income = round((total_female_income / females), 2)
        else:
            average_female_income = 0

        if saudis > 0:
           average_saudi_income = round((total_saudi_income / saudis), 2)
        else:
            average_saudi_income = 0

        if non_saudis > 0:
           average_non_saudi_income = round((total_non_saudi_income / non_saudis), 2)
        else:
            average_non_saudi_income = 0

 
        outputJson['features'][0]["properties"]["Total Population"]=total
        outputJson['features'][0]["properties"]["Total Males"]=males
        outputJson['features'][0]["properties"]["Total Females"]=females
        outputJson['features'][0]["properties"]["Total Saudis"]=saudis
        outputJson['features'][0]["properties"]["Total Non-saudis"]=non_saudis
        outputJson['features'][0]["properties"]["Male population (%)"]=f"{round((males / total) * 100, 2) if total else 0}%"
        outputJson['features'][0]["properties"]["Female population (%)"]=f"{round((females / total) * 100, 2) if total else 0}%"
        outputJson['features'][0]["properties"]["Saudis population (%)"]=f"{round((saudis / total) * 100, 2) if total else 0}%"
        outputJson['features'][0]["properties"]["Overall Average Income"]=average_income
        outputJson['features'][0]["properties"]["Average Male Income"]=average_male_income
        outputJson['features'][0]["properties"]["Average Female Income"]=average_female_income

        outputJson['features'][0]["properties"]["Average Saudi Income"]=average_saudi_income
        outputJson['features'][0]["properties"]["Average Non-Saudi Income"]=average_non_saudi_income
        outputJson['features'][0]["properties"]["Average Saudi Male Income"]=average_saudi_male_income
        outputJson['features'][0]["properties"]["Average Saudi Female Income"]=average_saudi_female_income
        outputJson['features'][0]["properties"]["Average Non-Saudi Male Income"]=average_non_saudi_male_income
        outputJson['features'][0]["properties"]["Average Non-Saudi Female Income"]=average_non_saudi_female_income

        for byGender in demo_data['byGenderAndAgeGroupPopulation']['facts']:
            
            outputJson['features'][0]["properties"][byGender["splits"][0]['id'] + "_" + byGender["splits"][1]['id']]=byGender["value"]
     

        for byNation in demo_data['byNationalityAndAgeGroupPopulation']['facts']:
            
             outputJson['features'][0]["properties"][byNation["splits"][0]['id'] + "_" + byNation["splits"][1]['id']]=byNation["value"]

        # Get Area Shape
        payload = json.dumps({
          "operationName": "getAreaShape",
          "variables": {
            "areaId": area_id,
            "epsilon": 0.00001
          },
          "query": "query getAreaShape($areaId: String!, $epsilon: Float!) {\n  area(id: $areaId) {\n    id\n    name(language: \"ar\")\n    type\n    simplifiedShape(epsilon: $epsilon)\n  }\n}\n"
        })
        headers = {
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload,verify=False)
        simplified_Shape = response.json()['data']['area']['simplifiedShape'][0]
        outputJson["features"][0]['geometry']['coordinates']=simplified_Shape

        coords =  outputJson["features"][0]['geometry']['coordinates']
          
        new_coords = []
        for ring in coords:
            new_ring = [[lat, lon] for lon, lat in ring]
            new_coords.append(new_ring)
        outputJson["features"][0]['geometry']['coordinates'] = new_coords

        outputData.append(outputJson)
        
except (Exception, ValueError) as e:
    print("Error", e)

finally:
   
    if outputData:
        os.makedirs("output_json_files", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_json = f"output_json_files/Output_data_{timestamp}.json"
        with open(filename_json, "w", encoding="utf-8") as f:
            json.dump(outputData, f, ensure_ascii=False, indent=4)
        print(f"\n📁 Saved collected Data to json file: {filename_json}")

