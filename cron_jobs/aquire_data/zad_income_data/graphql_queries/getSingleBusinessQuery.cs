{
  "operationName": "getSingleBusinessQuery",
  "variables": {
    "businessId": "business-12345-abcdef"
  },
  "query": "..."
}

query getSingleBusinessQuery($businessId: String!) {
  business(id: $businessId) {
    id
    location {
      latitude
      longitude
    }
    name: name(language: "ar")
    city {
      name(language: "ar")
    }
    governorate {
      name(language: "ar")
    }
    district {
      name(language: "ar")
    }
    zipCode {
      code
    }
    isic {
      id
      iconId
      singularName(language: "ar")
      type
      root {
        id
      }
    }
  }
}