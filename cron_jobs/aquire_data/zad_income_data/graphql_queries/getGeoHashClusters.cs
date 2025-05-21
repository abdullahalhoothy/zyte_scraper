{
  "operationName": "getGeoHashClusters",
  "variables": {
    "minLat": 24.611954116265036,
    "maxLat": 24.7523343668763,
    "minLng": 46.767420507324225,
    "maxLng": 46.93015549267579,
    "areas": ["0f92057c-dd62-4975-83bb-7e5ebd897727"],
    "precision": 13
  },
  "query": "..."
}


query getGeoHashClusters(
  $minLat: Float!
  $maxLat: Float!
  $minLng: Float!
  $maxLng: Float!
  $areas: [String]!
  $precision: Int!
) {
  businesses {
    otherClusters: aggregationByGeohashGrid(
      locationBoundingBox: {
        minimalLatitude: $minLat
        maximalLatitude: $maxLat
        minimalLongitude: $minLng
        maximalLongitude: $maxLng
      }
      excludedAreas: $areas
      precision: $precision
    ) {
      geohashGridBuckets {
        id: geohash
        location {
          latitude
          longitude
        }
        size
      }
    }
    selectedClusters: aggregationByGeohashGrid(
      areas: $areas
      locationBoundingBox: {
        minimalLatitude: $minLat
        maximalLatitude: $maxLat
        minimalLongitude: $minLng
        maximalLongitude: $maxLng
      }
      precision: $precision
    ) {
      geohashGridBuckets {
        id: geohash
        location {
          latitude
          longitude
        }
        size
      }
    }
    size(areas: $areas)
  }
}



#response
{
    "data": {
        "businesses": {
            "otherClusters": {
                "geohashGridBuckets": [
                    {
                        "id": "13\/5161\/3514",
                        "location": {
                            "latitude": 24.73852537572384,
                            "longitude": 46.82688399218023
                        },
                        "size": 3746
                    },
                    {
                        "id": "13\/5160\/3517",
                        "location": {
                            "latitude": 24.63420068845153,
                            "longitude": 46.78040466271341
                        },
                        "size": 3532
                    },
                    {
                        "id": "13\/5161\/3516",
                        "location": {
                            "latitude": 24.66417307499796,
                            "longitude": 46.82219515554607
                        },
                        "size": 3119
                    },
                    {
                        "id": "13\/5161\/3515",
                        "location": {
                            "latitude": 24.71324459183961,
                            "longitude": 46.82225223630667
                        },
                        "size": 3063
                    },
                    {
                        "id": "13\/5161\/3517",
                        "location": {
                            "latitude": 24.631099803373218,
                            "longitude": 46.81878891773522
                        },
                        "size": 2767
                    },
                    {
                        "id": "13\/5160\/3515",
                        "location": {
                            "latitude": 24.70467149745673,
                            "longitude": 46.7847825307399
                        },
                        "size": 2552
                    },
                    {
                        "id": "13\/5160\/3514",
                        "location": {
                            "latitude": 24.740644195117056,
                            "longitude": 46.782697197049856
                        },
                        "size": 1975
                    },
                    {
                        "id": "13\/5162\/3517",
                        "location": {
                            "latitude": 24.620964573696256,
                            "longitude": 46.858849888667464
                        },
                        "size": 1941
                    },
                    {
                        "id": "13\/5160\/3516",
                        "location": {
                            "latitude": 24.666901845484972,
                            "longitude": 46.78430979140103
                        },
                        "size": 1746
                    },
                    {
                        "id": "13\/5162\/3515",
                        "location": {
                            "latitude": 24.718408095650375,
                            "longitude": 46.85486353933811
                        },
                        "size": 1148
                    },
                    {
                        "id": "13\/5162\/3516",
                        "location": {
                            "latitude": 24.671895280480385,
                            "longitude": 46.85132034122944
                        },
                        "size": 721
                    },
                    {
                        "id": "13\/5162\/3514",
                        "location": {
                            "latitude": 24.73413116298616,
                            "longitude": 46.85510686598718
                        },
                        "size": 452
                    },
                    {
                        "id": "13\/5163\/3516",
                        "location": {
                            "latitude": 24.65999054722488,
                            "longitude": 46.90074507147074
                        },
                        "size": 125
                    },
                    {
                        "id": "13\/5163\/3515",
                        "location": {
                            "latitude": 24.699806263670325,
                            "longitude": 46.90483854152262
                        },
                        "size": 123
                    },
                    {
                        "id": "13\/5163\/3517",
                        "location": {
                            "latitude": 24.63738878723234,
                            "longitude": 46.89911118708551
                        },
                        "size": 29
                    },
                    {
                        "id": "13\/5163\/3514",
                        "location": {
                            "latitude": 24.745347280986607,
                            "longitude": 46.898568542674184
                        },
                        "size": 10
                    }
                ]
            },
            "selectedClusters": {
                "geohashGridBuckets": [
                    {
                        "id": "13\/5162\/3515",
                        "location": {
                            "latitude": 24.702610094100237,
                            "longitude": 46.8520166259259
                        },
                        "size": 1941
                    },
                    {
                        "id": "13\/5161\/3515",
                        "location": {
                            "latitude": 24.69604769255966,
                            "longitude": 46.83720337226987
                        },
                        "size": 688
                    },
                    {
                        "id": "13\/5161\/3516",
                        "location": {
                            "latitude": 24.685491984710097,
                            "longitude": 46.83410785160959
                        },
                        "size": 236
                    },
                    {
                        "id": "13\/5162\/3516",
                        "location": {
                            "latitude": 24.686906095594168,
                            "longitude": 46.84584100730717
                        },
                        "size": 2
                    }
                ]
            },
            "size": 2867
        }
    }
}