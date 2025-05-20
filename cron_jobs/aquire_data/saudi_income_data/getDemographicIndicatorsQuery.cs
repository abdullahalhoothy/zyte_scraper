{
  "operationName": "getDemographicIndicatorsQuery",
  "variables": {},
  "query": "..."
}

query getDemographicIndicatorsQuery {
  population_density: demographicIndicators(
    filters: {
      indicator: "population_density"
    }
    orders: {
      id: "value"
      direction: "desc"
    }
  ) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  population_growth_rate: demographicIndicators(
    filters: {
      indicator: "population_growth_rate"
    }
    orders: {
      id: "value"
      direction: "desc"
    }
  ) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  household_size: demographicIndicators(
    filters: {
      indicator: "household_size"
    }
    orders: {
      id: "value"
      direction: "desc"
    }
  ) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  household_growth_rate: demographicIndicators(
    filters: {
      indicator: "household_growth_rate"
    }
    orders: {
      id: "value"
      direction: "desc"
    }
  ) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  household_income: demographicIndicators(
    filters: {
      indicator: "household_income"
    }
    orders: {
      id: "value"
      direction: "desc"
    }
  ) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  household_savings: demographicIndicators(
    filters: {
      indicator: "household_savings"
    }
    orders: {
      id: "value"
      direction: "desc"
    }
  ) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  household_spending: demographicIndicators(
    filters: {
      indicator: "household_spending"
    }
    orders: {
      id: "value"
      direction: "desc"
    }
  ) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
}