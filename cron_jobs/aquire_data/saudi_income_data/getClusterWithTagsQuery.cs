{
  "operationName": "getClusterWithTagsQuery",
  "variables": {
    "minLat": 24.611,
    "maxLat": 24.752,
    "minLng": 46.767,
    "maxLng": 46.930,
    "clusterType": "district",
    "areas": ["86cdd3cf-82dd-461a-8764-5778344f1666"],
    "isics": ["G", "C"]
  },
  "query": "..."
}



query getClusterWithTagsQuery(
  $minLat: Float!
  $maxLat: Float!
  $minLng: Float!
  $maxLng: Float!
  $clusterType: String!
  $areas: [String]!
  $isics: [String]!
) {
  businesses {
    aggregationByAreaAndIsic(
      locationBoundingBox: {
        minimalLatitude: $minLat
        maximalLatitude: $maxLat
        minimalLongitude: $minLng
        maximalLongitude: $maxLng
      }
      areaAggregation: {
        areaClusterTypes: [$clusterType]
      }
      isics: $isics
    ) {
      areaBuckets {
        area {
          id
          location {
            latitude
            longitude
          }
        }
        isicBuckets {
          size
          isic {
            id
            root {
              id
            }
          }
        }
        size
      }
    }
    size(
      areas: $areas
      isics: $isics
    )
  }
}