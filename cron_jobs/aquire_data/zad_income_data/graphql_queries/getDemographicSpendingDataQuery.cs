{
  "operationName": "getDemographicSpendingDataQuery",
  "variables": {
    "areas": ["86cdd3cf-82dd-461a-8764-5778344f1666"]
  },
  "query": "..."
}

query getDemographicSpendingDataQuery($areas: [String]!) {
  spendingData(
    filters: { areas: $areas }
    orders: { id: "value", direction: "desc" }
  ) {
    facts {
      area {
        id
      }
      value
      subIndicator
    }
  }
}

#response

{"data":{"spendingData":{"facts":[]}}}