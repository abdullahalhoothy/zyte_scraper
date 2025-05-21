{
  "operationName": "getDemographicData",
  "variables": {
    "areas": ["86cdd3cf-82dd-461a-8764-5778344f1666"],
    "regionIdArr": ["city-3"]
  },
  "query": "..."
}

query getDemographicData($areas: [String]!, $regionIdArr: [String]!) {
  totalPopulation: population(
    filters: { areas: $areas }
    splits: []
  ) {
    facts {
      value
    }
  }
  malePopulation: population(
    filters: { areas: $areas, sexes: ["male"] }
    splits: []
  ) {
    facts {
      value
    }
  }
  femalePopulation: population(
    filters: { areas: $areas, sexes: ["female"] }
    splits: []
  ) {
    facts {
      value
    }
  }
  saudiPopulation: population(
    filters: { areas: $areas, nationalities: ["saudi"] }
    splits: []
  ) {
    facts {
      value
    }
  }
  nonSaudiPopulation: population(
    filters: { areas: $areas, nationalities: ["nonSaudi"] }
    splits: []
  ) {
    facts {
      value
    }
  }
  byGenderAndAgeGroupPopulation: population(
    filters: { areas: $areas }
    splits: ["sex", "ageGroup"]
  ) {
    facts {
      splits {
        id
        label(language: "ar")
      }
      value
    }
  }
  byNationalityAndAgeGroupPopulation: population(
    filters: { areas: $areas }
    splits: ["nationality", "ageGroup"]
  ) {
    facts {
      splits {
        id
        label(language: "ar")
      }
      value
    }
  }
  ageGroupLabels: population(
    filters: { areas: $regionIdArr }
    splits: ["ageGroup"]
  ) {
    facts {
      splits {
        id
        label(language: "ar")
      }
    }
  }
}

#response

{
    "data": {
        "totalPopulation": {
            "facts": [
                {
                    "value": 68177
                }
            ]
        },
        "malePopulation": {
            "facts": [
                {
                    "value": 34561
                }
            ]
        },
        "femalePopulation": {
            "facts": [
                {
                    "value": 33616
                }
            ]
        },
        "saudiPopulation": {
            "facts": [
                {
                    "value": 51301
                }
            ]
        },
        "nonSaudiPopulation": {
            "facts": [
                {
                    "value": 16876
                }
            ]
        },
        "byGenderAndAgeGroupPopulation": {
            "facts": [
                {
                    "splits": [
                        {
                            "id": "female",
                            "label": "\u0625\u0646\u0627\u062b"
                        },
                        {
                            "id": "0-9",
                            "label": "0-9"
                        }
                    ],
                    "value": 7007
                },
                {
                    "splits": [
                        {
                            "id": "female",
                            "label": "\u0625\u0646\u0627\u062b"
                        },
                        {
                            "id": "10-19",
                            "label": "10-19"
                        }
                    ],
                    "value": 8863
                },
                {
                    "splits": [
                        {
                            "id": "female",
                            "label": "\u0625\u0646\u0627\u062b"
                        },
                        {
                            "id": "20-29",
                            "label": "20-29"
                        }
                    ],
                    "value": 6544
                },
                {
                    "splits": [
                        {
                            "id": "female",
                            "label": "\u0625\u0646\u0627\u062b"
                        },
                        {
                            "id": "30-39",
                            "label": "30-39"
                        }
                    ],
                    "value": 4768
                },
                {
                    "splits": [
                        {
                            "id": "female",
                            "label": "\u0625\u0646\u0627\u062b"
                        },
                        {
                            "id": "40-49",
                            "label": "40-49"
                        }
                    ],
                    "value": 3873
                },
                {
                    "splits": [
                        {
                            "id": "female",
                            "label": "\u0625\u0646\u0627\u062b"
                        },
                        {
                            "id": "50-59",
                            "label": "50-59"
                        }
                    ],
                    "value": 1926
                },
                {
                    "splits": [
                        {
                            "id": "female",
                            "label": "\u0625\u0646\u0627\u062b"
                        },
                        {
                            "id": "60-69",
                            "label": "60-69"
                        }
                    ],
                    "value": 419
                },
                {
                    "splits": [
                        {
                            "id": "female",
                            "label": "\u0625\u0646\u0627\u062b"
                        },
                        {
                            "id": "70-79",
                            "label": "70-79"
                        }
                    ],
                    "value": 216
                },
                {
                    "splits": [
                        {
                            "id": "female",
                            "label": "\u0625\u0646\u0627\u062b"
                        },
                        {
                            "id": "80+",
                            "label": "80+"
                        }
                    ],
                    "value": 0
                },
                {
                    "splits": [
                        {
                            "id": "male",
                            "label": "\u0630\u0643\u0648\u0631"
                        },
                        {
                            "id": "0-9",
                            "label": "0-9"
                        }
                    ],
                    "value": 6339
                },
                {
                    "splits": [
                        {
                            "id": "male",
                            "label": "\u0630\u0643\u0648\u0631"
                        },
                        {
                            "id": "10-19",
                            "label": "10-19"
                        }
                    ],
                    "value": 8627
                },
                {
                    "splits": [
                        {
                            "id": "male",
                            "label": "\u0630\u0643\u0648\u0631"
                        },
                        {
                            "id": "20-29",
                            "label": "20-29"
                        }
                    ],
                    "value": 7085
                },
                {
                    "splits": [
                        {
                            "id": "male",
                            "label": "\u0630\u0643\u0648\u0631"
                        },
                        {
                            "id": "30-39",
                            "label": "30-39"
                        }
                    ],
                    "value": 4276
                },
                {
                    "splits": [
                        {
                            "id": "male",
                            "label": "\u0630\u0643\u0648\u0631"
                        },
                        {
                            "id": "40-49",
                            "label": "40-49"
                        }
                    ],
                    "value": 4012
                },
                {
                    "splits": [
                        {
                            "id": "male",
                            "label": "\u0630\u0643\u0648\u0631"
                        },
                        {
                            "id": "50-59",
                            "label": "50-59"
                        }
                    ],
                    "value": 2945
                },
                {
                    "splits": [
                        {
                            "id": "male",
                            "label": "\u0630\u0643\u0648\u0631"
                        },
                        {
                            "id": "60-69",
                            "label": "60-69"
                        }
                    ],
                    "value": 1007
                },
                {
                    "splits": [
                        {
                            "id": "male",
                            "label": "\u0630\u0643\u0648\u0631"
                        },
                        {
                            "id": "70-79",
                            "label": "70-79"
                        }
                    ],
                    "value": 162
                },
                {
                    "splits": [
                        {
                            "id": "male",
                            "label": "\u0630\u0643\u0648\u0631"
                        },
                        {
                            "id": "80+",
                            "label": "80+"
                        }
                    ],
                    "value": 108
                }
            ]
        },
        "byNationalityAndAgeGroupPopulation": {
            "facts": [
                {
                    "splits": [
                        {
                            "id": "nonSaudi",
                            "label": "\u063a\u064a\u0631 \u0633\u0639\u0648\u062f\u064a\u064a\u0646"
                        },
                        {
                            "id": "0-9",
                            "label": "0-9"
                        }
                    ],
                    "value": 3911
                },
                {
                    "splits": [
                        {
                            "id": "nonSaudi",
                            "label": "\u063a\u064a\u0631 \u0633\u0639\u0648\u062f\u064a\u064a\u0646"
                        },
                        {
                            "id": "10-19",
                            "label": "10-19"
                        }
                    ],
                    "value": 3395
                },
                {
                    "splits": [
                        {
                            "id": "nonSaudi",
                            "label": "\u063a\u064a\u0631 \u0633\u0639\u0648\u062f\u064a\u064a\u0646"
                        },
                        {
                            "id": "20-29",
                            "label": "20-29"
                        }
                    ],
                    "value": 2193
                },
                {
                    "splits": [
                        {
                            "id": "nonSaudi",
                            "label": "\u063a\u064a\u0631 \u0633\u0639\u0648\u062f\u064a\u064a\u0646"
                        },
                        {
                            "id": "30-39",
                            "label": "30-39"
                        }
                    ],
                    "value": 4193
                },
                {
                    "splits": [
                        {
                            "id": "nonSaudi",
                            "label": "\u063a\u064a\u0631 \u0633\u0639\u0648\u062f\u064a\u064a\u0646"
                        },
                        {
                            "id": "40-49",
                            "label": "40-49"
                        }
                    ],
                    "value": 2758
                },
                {
                    "splits": [
                        {
                            "id": "nonSaudi",
                            "label": "\u063a\u064a\u0631 \u0633\u0639\u0648\u062f\u064a\u064a\u0646"
                        },
                        {
                            "id": "50-59",
                            "label": "50-59"
                        }
                    ],
                    "value": 372
                },
                {
                    "splits": [
                        {
                            "id": "nonSaudi",
                            "label": "\u063a\u064a\u0631 \u0633\u0639\u0648\u062f\u064a\u064a\u0646"
                        },
                        {
                            "id": "60-69",
                            "label": "60-69"
                        }
                    ],
                    "value": 0
                },
                {
                    "splits": [
                        {
                            "id": "nonSaudi",
                            "label": "\u063a\u064a\u0631 \u0633\u0639\u0648\u062f\u064a\u064a\u0646"
                        },
                        {
                            "id": "70-79",
                            "label": "70-79"
                        }
                    ],
                    "value": 54
                },
                {
                    "splits": [
                        {
                            "id": "nonSaudi",
                            "label": "\u063a\u064a\u0631 \u0633\u0639\u0648\u062f\u064a\u064a\u0646"
                        },
                        {
                            "id": "80+",
                            "label": "80+"
                        }
                    ],
                    "value": 0
                },
                {
                    "splits": [
                        {
                            "id": "saudi",
                            "label": "\u0633\u0639\u0648\u062f\u064a\u0648\u0646"
                        },
                        {
                            "id": "0-9",
                            "label": "0-9"
                        }
                    ],
                    "value": 9435
                },
                {
                    "splits": [
                        {
                            "id": "saudi",
                            "label": "\u0633\u0639\u0648\u062f\u064a\u0648\u0646"
                        },
                        {
                            "id": "10-19",
                            "label": "10-19"
                        }
                    ],
                    "value": 14095
                },
                {
                    "splits": [
                        {
                            "id": "saudi",
                            "label": "\u0633\u0639\u0648\u062f\u064a\u0648\u0646"
                        },
                        {
                            "id": "20-29",
                            "label": "20-29"
                        }
                    ],
                    "value": 11436
                },
                {
                    "splits": [
                        {
                            "id": "saudi",
                            "label": "\u0633\u0639\u0648\u062f\u064a\u0648\u0646"
                        },
                        {
                            "id": "30-39",
                            "label": "30-39"
                        }
                    ],
                    "value": 4851
                },
                {
                    "splits": [
                        {
                            "id": "saudi",
                            "label": "\u0633\u0639\u0648\u062f\u064a\u0648\u0646"
                        },
                        {
                            "id": "40-49",
                            "label": "40-49"
                        }
                    ],
                    "value": 5127
                },
                {
                    "splits": [
                        {
                            "id": "saudi",
                            "label": "\u0633\u0639\u0648\u062f\u064a\u0648\u0646"
                        },
                        {
                            "id": "50-59",
                            "label": "50-59"
                        }
                    ],
                    "value": 4499
                },
                {
                    "splits": [
                        {
                            "id": "saudi",
                            "label": "\u0633\u0639\u0648\u062f\u064a\u0648\u0646"
                        },
                        {
                            "id": "60-69",
                            "label": "60-69"
                        }
                    ],
                    "value": 1426
                },
                {
                    "splits": [
                        {
                            "id": "saudi",
                            "label": "\u0633\u0639\u0648\u062f\u064a\u0648\u0646"
                        },
                        {
                            "id": "70-79",
                            "label": "70-79"
                        }
                    ],
                    "value": 324
                },
                {
                    "splits": [
                        {
                            "id": "saudi",
                            "label": "\u0633\u0639\u0648\u062f\u064a\u0648\u0646"
                        },
                        {
                            "id": "80+",
                            "label": "80+"
                        }
                    ],
                    "value": 108
                }
            ]
        },
        "ageGroupLabels": {
            "facts": [
                {
                    "splits": [
                        {
                            "id": "0-9",
                            "label": "0-9"
                        }
                    ]
                },
                {
                    "splits": [
                        {
                            "id": "10-19",
                            "label": "10-19"
                        }
                    ]
                },
                {
                    "splits": [
                        {
                            "id": "20-29",
                            "label": "20-29"
                        }
                    ]
                },
                {
                    "splits": [
                        {
                            "id": "30-39",
                            "label": "30-39"
                        }
                    ]
                },
                {
                    "splits": [
                        {
                            "id": "40-49",
                            "label": "40-49"
                        }
                    ]
                },
                {
                    "splits": [
                        {
                            "id": "50-59",
                            "label": "50-59"
                        }
                    ]
                },
                {
                    "splits": [
                        {
                            "id": "60-69",
                            "label": "60-69"
                        }
                    ]
                },
                {
                    "splits": [
                        {
                            "id": "70-79",
                            "label": "70-79"
                        }
                    ]
                },
                {
                    "splits": [
                        {
                            "id": "80+",
                            "label": "80+"
                        }
                    ]
                }
            ]
        }
    }
}