{
  "operationName": "getSectorsQuery",
  "variables": {},
  "query": "..."
}


query getSectorsQuery {
  isics {
    sectors: items(
      types: ["sector"]
      orders: [
        { id: "name_ar", direction: "asc" }
        { id: "id", direction: "asc" }
      ]
    ) {
      id
      name(language: "ar")
      type
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