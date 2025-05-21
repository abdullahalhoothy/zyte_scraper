{
  "operationName": "getBusinessFromAreaQuery",
  "variables": {
    "areas": ["86cdd3cf-82dd-461a-8764-5778344f1666"]
  },
  "query": "..."
}

query getBusinessFromAreaQuery($areas: [String]!) {
  businesses {
    size(areas: $areas)
  }
}

# response
{"data":{"businesses":{"size":897}}}