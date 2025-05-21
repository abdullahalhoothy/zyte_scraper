{
  "operationName": "getBusinessesByBoundingBox",
  "variables": {
    "minLat": 24.611954469013053,
    "maxLat": 24.75233471922736,
    "minLng": 46.767420507324225,
    "maxLng": 46.93015549267579,
    "isics": []
  },
  "query": "..."
}

query getBusinessesByBoundingBox(
  $minLat: Float!
  $maxLat: Float!
  $minLng: Float!
  $maxLng: Float!
) {
  businesses {
    size(
      locationBoundingBox: {
        minimalLatitude: $minLat
        maximalLatitude: $maxLat
        minimalLongitude: $minLng
        maximalLongitude: $maxLng
      }
    )
  }
}

#response
{"data":{"businesses":{"size":29916}}}