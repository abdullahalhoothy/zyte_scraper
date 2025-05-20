{
  "operationName": "getBreadcrumbs",
  "variables": {
    "minLat": 24.611954469013053,
    "maxLat": 24.75233471922736,
    "minLng": 46.767420507324225,
    "maxLng": 46.93015549267579,
    "zoom": 13
  },
  "query": "..."
}


query getBreadcrumbs(
  $minLat: Float!
  $maxLat: Float!
  $minLng: Float!
  $maxLng: Float!
  $zoom: Int!
) {
  breadcrumb(
    minimalLatitude: $minLat
    maximalLatitude: $maxLat
    minimalLongitude: $minLng
    maximalLongitude: $maxLng
    zoom: $zoom
  ) {
    emirate {
      area {
        id
        type
        name(language: "ar")
        boundingBox {
          minimalLatitude
          maximalLatitude
          minimalLongitude
          maximalLongitude
        }
      }
      score
    }
    governorate {
      area {
        id
        type
        name(language: "ar")
        boundingBox {
          minimalLatitude
          maximalLatitude
          minimalLongitude
          maximalLongitude
        }
      }
      score
    }
    city {
      area {
        id
        type
        name(language: "ar")
        boundingBox {
          minimalLatitude
          maximalLatitude
          minimalLongitude
          maximalLongitude
        }
      }
      score
    }
    district {
      area {
        id
        type
        name(language: "ar")
        boundingBox {
          minimalLatitude
          maximalLatitude
          minimalLongitude
          maximalLongitude
        }
      }
      score
    }
  }
}


# response

{
    "data": {
        "breadcrumb": {
            "emirate": null,
            "governorate": null,
            "city": {
                "area": {
                    "id": "city-3",
                    "type": "city",
                    "name": "\u0627\u0644\u0631\u064a\u0627\u0636",
                    "boundingBox": {
                        "minimalLatitude": 24.322529502133,
                        "maximalLatitude": 25.168237571295,
                        "minimalLongitude": 45.982203816547,
                        "maximalLongitude": 47.325657672319
                    }
                },
                "score": 1
            },
            "district": {
                "area": {
                    "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                    "type": "district",
                    "name": "\u0627\u0644\u0633\u0639\u0627\u062f\u0629",
                    "boundingBox": {
                        "minimalLatitude": 24.67762479217,
                        "maximalLatitude": 24.717741963468,
                        "minimalLongitude": 46.81679040253,
                        "maximalLongitude": 46.85671722661
                    }
                },
                "score": 0.8171025
            }
        }
    }
}