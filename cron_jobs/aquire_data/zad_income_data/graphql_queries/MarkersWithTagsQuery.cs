{
  "operationName": "MarkersWithTagsQuery",
  "variables": {
    "minLat": 24.611,
    "maxLat": 24.752,
    "minLng": 46.767,
    "maxLng": 46.930,
    "areas": ["86cdd3cf-82dd-461a-8764-5778344f1666"],
    "isics": ["G", "C", "F"]
  },
  "query": "..."
}


query MarkersWithTagsQuery(
  $minLat: Float!
  $maxLat: Float!
  $minLng: Float!
  $maxLng: Float!
  $areas: [String]!
  $isics: [String]!
) {
  businesses {
    items(
      locationBoundingBox: {
        minimalLatitude: $minLat
        maximalLatitude: $maxLat
        minimalLongitude: $minLng
        maximalLongitude: $maxLng
      }
      isics: $isics
      limit: 1000
    ) {
      id
      location {
        latitude
        longitude
      }
      isic {
        id
        name(language: "ar")
        type
        root {
          id
        }
      }
    }
    size(
      areas: $areas
      isics: $isics
    )
  }
}