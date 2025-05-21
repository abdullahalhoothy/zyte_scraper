{
  "operationName": "getMapPlacesPredictions",
  "variables": {
    "searchPhrase": "الرياض",
    "areas": ["86cdd3cf-82dd-461a-8764-5778344f1666"],
    "elasticAreaTypes": ["city", "district"]
  },
  "query": "..."
}


query getMapPlacesPredictions(
  $searchPhrase: String!
  $areas: [String!]!
  $elasticAreaTypes: [String!]
) {
  globalSearchResults(
    searchInput: {
      locales: ["ar"]
      searchPhrase: $searchPhrase
      matchNames: true
      matchIds: true
    }
    elasticAreaTypes: $elasticAreaTypes
    areas: $areas
    elasticEntityIndices: ["area"]
    googlePlaceAutocompleteTypes: []
    limit: 10
  ) {
    results: items {
      id
      name(language: "ar")
      type
      source
      parentName(language: "ar")
      boundingBox {
        minimalLatitude
        maximalLatitude
        minimalLongitude
        maximalLongitude
      }
      location {
        latitude
        longitude
      }
    }
  }
}