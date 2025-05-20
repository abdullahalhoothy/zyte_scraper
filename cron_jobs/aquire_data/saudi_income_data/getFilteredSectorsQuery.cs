{
  "operationName": "getFilteredSectorsQuery",
  "variables": {
    "searchPhrase": "تجارة",
    "ids": ["G", "C", "F"]
  },
  "query": "..."
}


query getFilteredSectorsQuery($searchPhrase: String!, $ids: [String]!) {
  isics {
    sectors: items(
      ids: $ids
      types: ["sector", "subsector"]
      searchInput: {
        locales: ["ar"]
        searchPhrase: $searchPhrase
        matchNames: true
        matchIds: true
      }
      orders: [
        { id: "name_ar", direction: "asc" }
        { id: "id", direction: "asc" }
      ]
    ) {
      id
      name(language: "ar")
      type
      root {
        id
        name(language: "ar")
        type
      }
      children {
        items(limit: 150) {
          id
          name(language: "ar")
          type
          root {
            id
            name(language: "ar")
          }
        }
      }
    }
  }
}