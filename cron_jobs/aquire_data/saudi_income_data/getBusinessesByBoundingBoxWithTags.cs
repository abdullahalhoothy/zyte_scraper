
{
  "operationName": "getBusinessesByBoundingBoxWithTags",
  "variables": {
    "minLat": 24.611,
    "maxLat": 24.752,
    "minLng": 46.767,
    "maxLng": 46.930,
    "isics": ["G", "C", "F"]
  },
  "query": "..."
}

query getBusinessesByBoundingBoxWithTags(
  $minLat: Float!
  $maxLat: Float!
  $minLng: Float!
  $maxLng: Float!
  $isics: [String]!
) {
  businesses {
    size(
      locationBoundingBox: {
        minimalLatitude: $minLat
        maximalLatitude: $maxLat
        minimalLongitude: $minLng
        maximalLongitude: $maxLng
      }
      isics: $isics
    )
  }
}