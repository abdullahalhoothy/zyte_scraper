{
  "operationName": "getBusinessFromAreaAndIsicsQuery",
  "variables": {
    "areas": ["86cdd3cf-82dd-461a-8764-5778344f1666"],
    "isics": ["G", "C", "F"]
  },
  "query": "..."
}

query getBusinessFromAreaAndIsicsQuery(
  $areas: [String]!
  $isics: [String]!
) {
  businesses {
    size(
      areas: $areas
      isics: $isics
    )
  }
}