{
        "operationName": "getIncomeQuery",
        "variables": {
            "areas": ['emirate-1', 'city-3']
        },
        "query": query
    }


query getIncomeQuery($areas: [String]!) {
  all: averageIncome(filters: {male: null, saudi: null, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  male: averageIncome(filters: {male: true, saudi: null, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  female: averageIncome(filters: {male: false, saudi: null, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  saudi: averageIncome(filters: {male: null, saudi: true, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  nonSaudi: averageIncome(filters: {male: null, saudi: false, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  saudiMale: averageIncome(filters: {male: true, saudi: true, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  saudiFemale: averageIncome(filters: {male: false, saudi: true, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  nonSaudiMale: averageIncome(filters: {male: true, saudi: false, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
  nonSaudiFemale: averageIncome(filters: {male: false, saudi: false, parentAreas: $areas}, orders: {id: "value", direction: "desc"}) {
    facts {
      area {
        id
        name(language: "ar")
      }
      value
    }
  }
}


# response
{
    "data": {
        "all": {
            "facts": [
                {
                    "area": {
                        "id": "aa21340b-3580-4a62-8a43-3d12f6b00501",
                        "name": "السفارات"
                    },
                    "value": 33738
                },
                {
                    "area": {
                        "id": "228ef43a-9e3e-48cb-bf5e-893d71a6554a",
                        "name": "الرائد"
                    },
                    "value": 20720
                },
                {
                    "area": {
                        "id": "fde48b0e-8c5f-4683-8cec-c29e7284ebf5",
                        "name": "المعذر"
                    },
                    "value": 18250
                },
                {
                    "area": {
                        "id": "e59fe6ef-9353-440d-b502-dc8ff67b99fb",
                        "name": "عريض"
                    },
                    "value": 16667
                },
                {
                    "area": {
                        "id": "e8c5f0cc-8565-4a1e-b40d-f1727489f6aa",
                        "name": "الخزامى"
                    },
                    "value": 15689
                },
                {
                    "area": {
                        "id": "47e60f73-b741-4d9e-87e4-a4e613d37cde",
                        "name": "الملك عبد العزيز"
                    },
                    "value": 15516
                },
                {
                    "area": {
                        "id": "a29b89a8-30fd-4d75-9945-ecfec789c7cc",
                        "name": "المهدية"
                    },
                    "value": 15167
                },
                {
                    "area": {
                        "id": "843fce03-4fe4-4981-a161-b2284321d375",
                        "name": "النموذجية"
                    },
                    "value": 14711
                },
                {
                    "area": {
                        "id": "7566b077-f54c-444e-b41f-fb9ba8bbd8dd",
                        "name": "جامعة الملك سعود"
                    },
                    "value": 14189
                },
                {
                    "area": {
                        "id": "d6d2d11e-2744-418e-904a-dc8ba194998e",
                        "name": "خشم العان"
                    },
                    "value": 12475
                },
                {
                    "area": {
                        "id": "da870943-28b0-48ef-a7e4-3237b6a3908c",
                        "name": "المحمدية"
                    },
                    "value": 12453
                },
                {
                    "area": {
                        "id": "5cf83942-e014-4a10-968d-408e1937b82e",
                        "name": "الورود"
                    },
                    "value": 12357
                },
                {
                    "area": {
                        "id": "8dbab168-3b00-4a12-bc76-dc9d95373cac",
                        "name": "أشبيلية"
                    },
                    "value": 11897
                },
                {
                    "area": {
                        "id": "3f6854d2-c64c-4718-98bb-00c9c1ff6cd3",
                        "name": "الغدير"
                    },
                    "value": 11692
                },
                {
                    "area": {
                        "id": "07310269-69f4-4e5a-a093-3b0686e6f92a",
                        "name": "الحمراء"
                    },
                    "value": 11650
                },
                {
                    "area": {
                        "id": "f2724a71-ad73-4765-8462-f299eff48fec",
                        "name": "القدس"
                    },
                    "value": 11527
                },
                {
                    "area": {
                        "id": "7c07ad55-b15f-48f6-9aed-ebc1e67eff45",
                        "name": "الرمال"
                    },
                    "value": 11025
                },
                {
                    "area": {
                        "id": "1d18118a-09f4-46a3-a7fe-9f8a4aba9058",
                        "name": "غرناطة"
                    },
                    "value": 10736
                },
                {
                    "area": {
                        "id": "c82315c6-3142-41f8-96ff-bc8329391522",
                        "name": "السليمانية - الملز والبطحاء"
                    },
                    "value": 10723
                },
                {
                    "area": {
                        "id": "2ff065d6-764e-40b8-91fd-8210fad92c44",
                        "name": "الملك عبدالله"
                    },
                    "value": 10674
                },
                {
                    "area": {
                        "id": "a86339c7-1a18-4384-8800-76f1573c04a9",
                        "name": "الواحة"
                    },
                    "value": 10614
                },
                {
                    "area": {
                        "id": "cf8c586f-e220-4ca5-b3d2-c68a2c39df91",
                        "name": "الندي"
                    },
                    "value": 10573
                },
                {
                    "area": {
                        "id": "900a8735-f91e-45b7-9702-c556cc4863bc",
                        "name": "الريان"
                    },
                    "value": 10524
                },
                {
                    "area": {
                        "id": "3b880a15-edb7-459d-817b-bbb4e5212ab9",
                        "name": "عكاظ"
                    },
                    "value": 10513
                },
                {
                    "area": {
                        "id": "d8229af8-3a8a-421b-8e4f-74969f448e47",
                        "name": "الملقا"
                    },
                    "value": 10362
                },
                {
                    "area": {
                        "id": "ce4632d7-923a-409e-864a-b9c0e25775b6",
                        "name": "العارض"
                    },
                    "value": 10197
                },
                {
                    "area": {
                        "id": "5b05c230-55c9-499b-a012-887d53d66800",
                        "name": "المربع"
                    },
                    "value": 10039
                },
                {
                    "area": {
                        "id": "8dba8acc-a41e-4473-8a52-10622bee365b",
                        "name": "الدريهمية"
                    },
                    "value": 10007
                },
                {
                    "area": {
                        "id": "2f57568c-1f9d-4659-9d1b-70e720b0a45c",
                        "name": "التعاون"
                    },
                    "value": 9981
                },
                {
                    "area": {
                        "id": "c59c5455-500a-4d2b-a7b4-6802fb3f170c",
                        "name": "الرمال"
                    },
                    "value": 9980
                },
                {
                    "area": {
                        "id": "aa3edb6a-2aaa-4f34-891b-32fd7a64014e",
                        "name": "الربيع"
                    },
                    "value": 9886
                },
                {
                    "area": {
                        "id": "72b24564-20c8-4d3a-9d53-dd559786164d",
                        "name": "الفلاح"
                    },
                    "value": 9875
                },
                {
                    "area": {
                        "id": "38434635-316c-4696-bf6e-0d350cf2e76a",
                        "name": "عليشة"
                    },
                    "value": 9768
                },
                {
                    "area": {
                        "id": "c7750a62-e42d-42eb-9e83-aa44bf10a777",
                        "name": "النخيل"
                    },
                    "value": 9765
                },
                {
                    "area": {
                        "id": "ea03b9a1-d5f3-469f-a9fb-cfb72df61d7f",
                        "name": "المعذر الشمالي"
                    },
                    "value": 9732
                },
                {
                    "area": {
                        "id": "edd4c9b9-7053-48cf-983e-81c681aab6f8",
                        "name": "حطين"
                    },
                    "value": 9730
                },
                {
                    "area": {
                        "id": "c8f985cb-9b86-4d57-957f-b09b2ae78ab9",
                        "name": "المروج"
                    },
                    "value": 9723
                },
                {
                    "area": {
                        "id": "6720febf-8019-40cf-9446-5b2c8474d04d",
                        "name": "الرماية"
                    },
                    "value": 9685
                },
                {
                    "area": {
                        "id": "48539b17-54d3-4f28-968c-025684a0ceab",
                        "name": "الملك فيصل"
                    },
                    "value": 9669
                },
                {
                    "area": {
                        "id": "ca70401b-2dbf-4153-afcf-35969ce14bfd",
                        "name": "الصحافة"
                    },
                    "value": 9665
                },
                {
                    "area": {
                        "id": "f659dd2c-ba77-464d-8a3d-70771ceda67c",
                        "name": "الصفاء"
                    },
                    "value": 9618
                },
                {
                    "area": {
                        "id": "ec66cc90-a1c0-4cb5-873d-7c4757b69971",
                        "name": "الأندلس"
                    },
                    "value": 9617
                },
                {
                    "area": {
                        "id": "b1a6d8da-05c8-40fd-87e3-6b99a97079d2",
                        "name": "المنار"
                    },
                    "value": 9610
                },
                {
                    "area": {
                        "id": "206645fd-79d5-44fb-bcc7-4bdafd602a9b",
                        "name": "النفل"
                    },
                    "value": 9581
                },
                {
                    "area": {
                        "id": "d3e1ad91-49ce-4b0c-bb5d-1fffecd8fafa",
                        "name": "اليرموك"
                    },
                    "value": 9508
                },
                {
                    "area": {
                        "id": "7bc70bab-8ac6-42d1-9d55-922d0df681d2",
                        "name": "الربوة"
                    },
                    "value": 9507
                },
                {
                    "area": {
                        "id": "d36380e7-28b8-4926-a30f-8fc9327abfb1",
                        "name": "النزهه"
                    },
                    "value": 9419
                },
                {
                    "area": {
                        "id": "4731263b-77e7-4938-adc7-a7c5f81b3900",
                        "name": "القيروان"
                    },
                    "value": 9392
                },
                {
                    "area": {
                        "id": "ed69f3e8-523c-4ce7-a493-e92f4f9f1986",
                        "name": "أم الحمام الغربي"
                    },
                    "value": 9330
                },
                {
                    "area": {
                        "id": "68b0afd0-e462-4930-936b-20532c79f1ad",
                        "name": "قرطبة"
                    },
                    "value": 9257
                },
                {
                    "area": {
                        "id": "c1b851a6-029c-42bc-97f5-bd72af99b3ed",
                        "name": "الروابي"
                    },
                    "value": 9233
                },
                {
                    "area": {
                        "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
                        "name": "صلاح الدين"
                    },
                    "value": 9216
                },
                {
                    "area": {
                        "id": "86cdd3cf-82dd-461a-8764-5778344f1666",
                        "name": "الفيحاء"
                    },
                    "value": 9201
                },
                {
                    "area": {
                        "id": "d0759107-5d0c-4fb3-8ac2-745dbe717ed0",
                        "name": "المصيف"
                    },
                    "value": 9198
                },
                {
                    "area": {
                        "id": "d8f9c2f5-91d2-4806-be75-b4d5e229e084",
                        "name": "المرسلات"
                    },
                    "value": 9170
                },
                {
                    "area": {
                        "id": "0d7ff18e-c7e2-4607-a063-8b7c73b99838",
                        "name": "العليا - المعذر"
                    },
                    "value": 9145
                },
                {
                    "area": {
                        "id": "cfa2d353-9107-4b34-bccf-533aac553ab4",
                        "name": "الزهراء"
                    },
                    "value": 9116
                },
                {
                    "area": {
                        "id": "009e646e-bb16-4a74-adda-4791c4cbc9c1",
                        "name": "السليمانية - العليا"
                    },
                    "value": 9056
                },
                {
                    "area": {
                        "id": "c37bc305-4ffc-4489-a6e3-9269b32edb1a",
                        "name": "الإسكان"
                    },
                    "value": 9043
                },
                {
                    "area": {
                        "id": "a7e5ebed-efe6-4956-a53a-19f21c4a2cf9",
                        "name": "المونسية"
                    },
                    "value": 8996
                },
                {
                    "area": {
                        "id": "2c51be33-11eb-4645-a407-92d9acd33c9c",
                        "name": "عرقة"
                    },
                    "value": 8817
                },
                {
                    "area": {
                        "id": "d7a56eca-bec8-49e9-ab68-bfa73a314faa",
                        "name": "السلام"
                    },
                    "value": 8776
                },
                {
                    "area": {
                        "id": "cbb041b7-f87c-4878-821c-16ca4f34e10b",
                        "name": "الياسمين"
                    },
                    "value": 8770
                },
                {
                    "area": {
                        "id": "67ebb7a3-cd3d-480c-ba20-20e8c55c8332",
                        "name": "الرحمانية"
                    },
                    "value": 8763
                },
                {
                    "area": {
                        "id": "5e21ce61-1c87-4d44-bb79-62c105b36cc4",
                        "name": "المغرزات"
                    },
                    "value": 8738
                },
                {
                    "area": {
                        "id": "1f8ff56c-ade7-476d-9a18-ebf538ec1767",
                        "name": "الوادي"
                    },
                    "value": 8716
                },
                {
                    "area": {
                        "id": "52d2e2cd-fbb4-4830-84cc-58ae92d267a6",
                        "name": "الإزدهار"
                    },
                    "value": 8688
                },
                {
                    "area": {
                        "id": "d096152a-b6d5-49c8-84b9-b9ca4a46fd2d",
                        "name": "العليا - العليا"
                    },
                    "value": 8688
                },
                {
                    "area": {
                        "id": "98f7f0d1-438f-4c87-a98f-e0fda41b84bd",
                        "name": "ظهرة نمار"
                    },
                    "value": 8681
                },
                {
                    "area": {
                        "id": "4ed2e10c-2b71-4414-a8f3-9b8a3f30e560",
                        "name": "العقيق"
                    },
                    "value": 8637
                },
                {
                    "area": {
                        "id": "2b62095b-102f-441f-ac00-34602cd48536",
                        "name": "الجزيرة"
                    },
                    "value": 8633
                },
                {
                    "area": {
                        "id": "a01d452c-3a36-4f1b-9ede-2eeb934405a8",
                        "name": "الرفيعة"
                    },
                    "value": 8630
                },
                {
                    "area": {
                        "id": "62a893fc-9ec9-4e13-a01e-7191f976e312",
                        "name": "الروضة"
                    },
                    "value": 8541
                },
                {
                    "area": {
                        "id": "aa140531-ded7-47f4-b7d5-591930d0316b",
                        "name": "النهضة"
                    },
                    "value": 8508
                },
                {
                    "area": {
                        "id": "febe47f1-831b-472c-a068-339a65069dd3",
                        "name": "المعزيلة"
                    },
                    "value": 8425
                },
                {
                    "area": {
                        "id": "8014f925-e0b7-4af1-9d9b-20c75afca882",
                        "name": "العليا - الملز والبطحاء"
                    },
                    "value": 8370
                },
                {
                    "area": {
                        "id": "f96795fc-dd23-4de7-9d54-f9050c0f8e9d",
                        "name": "النرجس"
                    },
                    "value": 8332
                },
                {
                    "area": {
                        "id": "b7aeff04-e705-4a9b-ae9f-0da2ac5b3d9e",
                        "name": "القادسية"
                    },
                    "value": 8314
                },
                {
                    "area": {
                        "id": "471d8f88-5a0b-4890-8026-a63a835bf52a",
                        "name": "العوالي"
                    },
                    "value": 8266
                },
                {
                    "area": {
                        "id": "e443160a-e66b-4369-a4bf-95f26060eccd",
                        "name": "الحزم"
                    },
                    "value": 8188
                },
                {
                    "area": {
                        "id": "d85bc333-4975-421c-9d03-df228e6ae9ea",
                        "name": "الضباط"
                    },
                    "value": 8178
                },
                {
                    "area": {
                        "id": "b4aed3f7-045a-443e-b340-81043580d7b9",
                        "name": "هجرة وادي لبن"
                    },
                    "value": 8121
                },
                {
                    "area": {
                        "id": "c0c6513b-13b9-45e1-848a-a4959f95971a",
                        "name": "الملك فهد"
                    },
                    "value": 8114
                },
                {
                    "area": {
                        "id": "aff3e994-cc0a-4e88-912d-0690a9983b27",
                        "name": "السويدي الغربي"
                    },
                    "value": 8079
                },
                {
                    "area": {
                        "id": "c7f18c78-aae4-4895-a83c-57ce0c761cd1",
                        "name": "جرير"
                    },
                    "value": 8069
                },
                {
                    "area": {
                        "id": "cd6e3719-5fb9-497a-91b9-e2668e2e75a6",
                        "name": "الهدا - الديرة"
                    },
                    "value": 8028
                },
                {
                    "area": {
                        "id": "43f724c9-8295-46e4-b80d-af74e659b872",
                        "name": "العريجاء الغربية"
                    },
                    "value": 8024
                },
                {
                    "area": {
                        "id": "e9de74de-e178-4d06-856f-1689820e2c5a",
                        "name": "شبرا"
                    },
                    "value": 8007
                },
                {
                    "area": {
                        "id": "1460a408-4989-4c5e-9e97-494e36c3497a",
                        "name": "ضاحية نمار"
                    },
                    "value": 7992
                },
                {
                    "area": {
                        "id": "30db56d8-31f6-4a21-81fa-f135163359b1",
                        "name": "الخليج"
                    },
                    "value": 7973
                },
                {
                    "area": {
                        "id": "bf723f44-607f-4114-91b9-db8cd0c77a91",
                        "name": "الشفاء"
                    },
                    "value": 7965
                },
                {
                    "area": {
                        "id": "2fa38d65-6151-493e-98aa-c14c06a28197",
                        "name": "الفاخرية"
                    },
                    "value": 7952
                },
                {
                    "area": {
                        "id": "842383e2-3091-4283-b65c-f4a62cd18784",
                        "name": "ظهرة لبن"
                    },
                    "value": 7889
                },
                {
                    "area": {
                        "id": "0442bf29-e3f1-4dfa-8afd-b11e063b015a",
                        "name": "العريجاء الوسطى"
                    },
                    "value": 7807
                },
                {
                    "area": {
                        "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                        "name": "السعادة"
                    },
                    "value": 7662
                },
                {
                    "area": {
                        "id": "b65ac3ce-46ab-419d-be64-7aa2761f4c28",
                        "name": "الجنادرية"
                    },
                    "value": 7562
                },
                {
                    "area": {
                        "id": "1297bd50-a138-4c61-9898-97d18963331a",
                        "name": "النسيم الشرقي"
                    },
                    "value": 7556
                },
                {
                    "area": {
                        "id": "2be8f71f-bb94-4702-87d6-a258a14df452",
                        "name": "الزهرة"
                    },
                    "value": 7548
                },
                {
                    "area": {
                        "id": "7a9f08b6-502e-4300-87ac-3dc37a27e74c",
                        "name": "النظيم"
                    },
                    "value": 7542
                },
                {
                    "area": {
                        "id": "c35d1f60-d5ff-4885-91c6-85a519c80dcf",
                        "name": "الهدا - المعذر"
                    },
                    "value": 7500
                },
                {
                    "area": {
                        "id": "city-3",
                        "name": "الرياض"
                    },
                    "value": 7454
                },
                {
                    "area": {
                        "id": "7b5f813e-a731-40ef-b3a0-afac81467277",
                        "name": "نمار"
                    },
                    "value": 7260
                },
                {
                    "area": {
                        "id": "c1df54b0-feac-4290-9e75-8afd9e313efb",
                        "name": "طويق - عتيقة"
                    },
                    "value": 7169
                },
                {
                    "area": {
                        "id": "40772979-0127-4648-b641-dee43ee6b96b",
                        "name": "السويدي"
                    },
                    "value": 7125
                },
                {
                    "area": {
                        "id": "c9fe42ca-2797-466e-b1d1-cb90c69a5605",
                        "name": "المروه"
                    },
                    "value": 7077
                },
                {
                    "area": {
                        "id": "39ac02a1-c044-4620-9169-b472154e3768",
                        "name": "ظهرة البديعة"
                    },
                    "value": 7053
                },
                {
                    "area": {
                        "id": "61ab70a4-3d37-47bd-a9ee-124bdc0fb670",
                        "name": "المنصورة"
                    },
                    "value": 7014
                },
                {
                    "area": {
                        "id": "1f314e74-fac1-4ebf-b83a-830ba70c09c3",
                        "name": "الدرعية"
                    },
                    "value": 6945
                },
                {
                    "area": {
                        "id": "751de8ea-eab5-45f3-801f-6a969a57b4e7",
                        "name": "الفاروق"
                    },
                    "value": 6876
                },
                {
                    "area": {
                        "id": "4f6a0751-1320-4e27-913b-2dfec0d8aa2f",
                        "name": "الدار البيضاء"
                    },
                    "value": 6866
                },
                {
                    "area": {
                        "id": "13d2af17-de45-4e53-9dcc-17f1f18ba0a1",
                        "name": "المؤتمرات"
                    },
                    "value": 6842
                },
                {
                    "area": {
                        "id": "0434eb81-4f04-4007-92cc-b0c5410bea7c",
                        "name": "الفوطة"
                    },
                    "value": 6830
                },
                {
                    "area": {
                        "id": "b91c2ee4-5fc7-4632-ac89-07e6fc008363",
                        "name": "الملز"
                    },
                    "value": 6828
                },
                {
                    "area": {
                        "id": "5b8e557e-aebe-4553-8402-8973b4ff0a79",
                        "name": "العزيزية"
                    },
                    "value": 6823
                },
                {
                    "area": {
                        "id": "5dfaa455-f597-4c2b-961e-cd2faf15d08f",
                        "name": "النسيم الغربي"
                    },
                    "value": 6542
                },
                {
                    "area": {
                        "id": "01c9ff6a-eb28-4465-a68c-c8a5562c6d39",
                        "name": "بدر"
                    },
                    "value": 6404
                },
                {
                    "area": {
                        "id": "920c7560-2916-44ef-ac0e-f1baac271657",
                        "name": "ديراب"
                    },
                    "value": 6354
                },
                {
                    "area": {
                        "id": "f8bed1dc-356d-43a9-b89b-9d1446a74683",
                        "name": "الحائر"
                    },
                    "value": 5922
                },
                {
                    "area": {
                        "id": "ea504b74-c266-4b09-b298-08e9dfb35eb5",
                        "name": "الـشـرفـيـة"
                    },
                    "value": 5755
                },
                {
                    "area": {
                        "id": "14561646-f4ae-4c62-b7f1-8f95156cc0ef",
                        "name": "أحـد"
                    },
                    "value": 5728
                },
                {
                    "area": {
                        "id": "758da835-c682-46d6-82ad-0d9fb8442113",
                        "name": "العريجاء"
                    },
                    "value": 5699
                },
                {
                    "area": {
                        "id": "5ce6d443-f294-4559-9329-57509cc90cae",
                        "name": "البطيحا"
                    },
                    "value": 5465
                },
                {
                    "area": {
                        "id": "88251c8e-068a-4862-aff5-b6c2feb5e876",
                        "name": "الوشام"
                    },
                    "value": 5447
                },
                {
                    "area": {
                        "id": "0e8da9c4-e4a7-4794-a62d-9ab0554e7579",
                        "name": "أم الحمام الشرقي - الديرة"
                    },
                    "value": 5361
                },
                {
                    "area": {
                        "id": "9d09b05f-35f3-4925-84b1-978e9d701e5e",
                        "name": "أم الحمام الشرقي - المعذر"
                    },
                    "value": 5279
                },
                {
                    "area": {
                        "id": "27783c9e-535f-4d44-9a5d-ed549644c5be",
                        "name": "سلطانة - العريجاء"
                    },
                    "value": 5208
                },
                {
                    "area": {
                        "id": "f0eb256e-8c6b-4943-9812-8a10c483b65d",
                        "name": "هيت"
                    },
                    "value": 4838
                },
                {
                    "area": {
                        "id": "fcf3bfcc-4e81-4db1-8fe5-ef65fc610991",
                        "name": "البديعة"
                    },
                    "value": 4571
                },
                {
                    "area": {
                        "id": "7a4897d9-89ac-4d95-a544-2aeee4f1beb2",
                        "name": "الصناعية"
                    },
                    "value": 4465
                },
                {
                    "area": {
                        "id": "9c5397a5-f624-4116-8db2-34ecf79e5315",
                        "name": "الفيصلية"
                    },
                    "value": 4347
                },
                {
                    "area": {
                        "id": "6eea7b8d-e938-466a-ac3e-ae2b106ac59f",
                        "name": "النور"
                    },
                    "value": 4067
                },
                {
                    "area": {
                        "id": "33808d06-6a8a-42c1-86b2-79b4709905fd",
                        "name": "الناصرية"
                    },
                    "value": 4059
                },
                {
                    "area": {
                        "id": "039f1dd3-6866-4e6c-8f4f-53ba926d1f50",
                        "name": "القرى"
                    },
                    "value": 4000
                },
                {
                    "area": {
                        "id": "c8fbfbfe-c1a0-4079-be04-ad20730038b0",
                        "name": "الوزارات"
                    },
                    "value": 3819
                },
                {
                    "area": {
                        "id": "feb5834c-f023-44d4-8a14-35dc6629017d",
                        "name": "العمل"
                    },
                    "value": 3806
                },
                {
                    "area": {
                        "id": "dde02562-5497-4b68-bb19-baa4d9e93db5",
                        "name": "الخالدية"
                    },
                    "value": 3773
                },
                {
                    "area": {
                        "id": "1a94924e-c8b8-47ae-b6f4-595f4acf8b3d",
                        "name": "غبيراء"
                    },
                    "value": 3752
                },
                {
                    "area": {
                        "id": "27c6e7ac-e6e9-49c9-abc9-c179249cf345",
                        "name": "المناخ"
                    },
                    "value": 3538
                },
                {
                    "area": {
                        "id": "05fe6a6f-34eb-45eb-82be-260adddd6082",
                        "name": "عتيقة"
                    },
                    "value": 3495
                },
                {
                    "area": {
                        "id": "6a6535f2-c3fc-408d-8de8-4d048dd19728",
                        "name": "اليمامة"
                    },
                    "value": 3402
                },
                {
                    "area": {
                        "id": "1bdf2e61-64d7-42c7-bd24-3b58fa806746",
                        "name": "جبرة"
                    },
                    "value": 3223
                },
                {
                    "area": {
                        "id": "408b741e-1704-4e36-be99-3c9201ef4b51",
                        "name": "صياح"
                    },
                    "value": 3153
                },
                {
                    "area": {
                        "id": "19381f2a-1d68-4fc3-bc5a-09d5481cf03b",
                        "name": "الجرادية"
                    },
                    "value": 3152
                },
                {
                    "area": {
                        "id": "b9945c44-61a0-4d1e-85f2-24eefe9611ae",
                        "name": "سلطانة - الديرة"
                    },
                    "value": 3068
                },
                {
                    "area": {
                        "id": "332ccd9e-8159-49fe-935d-bbb98730c2fc",
                        "name": "الشميسي"
                    },
                    "value": 2972
                },
                {
                    "area": {
                        "id": "fd3f2823-fefa-4c52-aaa9-60150ebd0c37",
                        "name": "الديرة"
                    },
                    "value": 2902
                },
                {
                    "area": {
                        "id": "3f6c38e8-6b3e-4775-8e1a-905b71f5858a",
                        "name": "الصالحية"
                    },
                    "value": 2862
                },
                {
                    "area": {
                        "id": "1570d51a-3e9a-4b78-acb2-3d5389cd2a81",
                        "name": "منفوحة الجديدة"
                    },
                    "value": 2841
                },
                {
                    "area": {
                        "id": "51c12d2a-9ae8-4266-adc3-5126aa359cd3",
                        "name": "العود"
                    },
                    "value": 2772
                },
                {
                    "area": {
                        "id": "113113e3-21a3-4a3a-bfae-3dd799ded51c",
                        "name": "الوسيطا"
                    },
                    "value": 2721
                },
                {
                    "area": {
                        "id": "7dd2b8d2-e89d-408b-bc10-b735809ff749",
                        "name": "المرقب"
                    },
                    "value": 2684
                },
                {
                    "area": {
                        "id": "66566263-1c8d-4e72-85e1-406464b90bbe",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 2546
                },
                {
                    "area": {
                        "id": "aa913c8f-ae16-4ee9-a414-1318cda9c41a",
                        "name": "ثليم"
                    },
                    "value": 2519
                },
                {
                    "area": {
                        "id": "e85c3bb7-6f91-41de-8447-7a274dc46df3",
                        "name": "أم سليم"
                    },
                    "value": 2405
                },
                {
                    "area": {
                        "id": "ff86addf-942e-41dc-bb0f-9269251b42a3",
                        "name": "منفوحة"
                    },
                    "value": 2358
                },
                {
                    "area": {
                        "id": "b2fbbbbc-f12f-44a5-8e76-a674c7a1a9e0",
                        "name": "معكال"
                    },
                    "value": 2258
                },
                {
                    "area": {
                        "id": "bc3d0470-797d-4659-9d54-2d5048e158f3",
                        "name": "المصانع"
                    },
                    "value": 2073
                },
                {
                    "area": {
                        "id": "2911ee84-265f-44d7-8105-4c5ea9e1c72b",
                        "name": "طيبة"
                    },
                    "value": 2000
                },
                {
                    "area": {
                        "id": "3c56b430-f38e-4714-81e3-8a502f8fb971",
                        "name": "السلي"
                    },
                    "value": 1982
                },
                {
                    "area": {
                        "id": "888e14d1-e0da-4731-a7d7-605372279f88",
                        "name": "الدوبية"
                    },
                    "value": 1967
                },
                {
                    "area": {
                        "id": "baa1d3f2-7268-4abf-b839-02bd717dfeca",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 1955
                },
                {
                    "area": {
                        "id": "1476a71c-9823-4053-9439-cb7b7ce6a7fa",
                        "name": "سلام"
                    },
                    "value": 1932
                },
                {
                    "area": {
                        "id": "7e0fd377-cd04-4845-8b7f-7144752aea0d",
                        "name": "الدفاع"
                    },
                    "value": 1907
                },
                {
                    "area": {
                        "id": "076e4790-fa1c-4add-9531-491da2447079",
                        "name": "المصفاة"
                    },
                    "value": 1580
                },
                {
                    "area": {
                        "id": "977a2aab-df59-47b7-86c6-0e653c3c4cfd",
                        "name": "المنصورية"
                    },
                    "value": 1500
                }
            ]
        },
        "male": {
            "facts": [
                {
                    "area": {
                        "id": "aa21340b-3580-4a62-8a43-3d12f6b00501",
                        "name": "السفارات"
                    },
                    "value": 39800
                },
                {
                    "area": {
                        "id": "47e60f73-b741-4d9e-87e4-a4e613d37cde",
                        "name": "الملك عبد العزيز"
                    },
                    "value": 29275
                },
                {
                    "area": {
                        "id": "7566b077-f54c-444e-b41f-fb9ba8bbd8dd",
                        "name": "جامعة الملك سعود"
                    },
                    "value": 23605
                },
                {
                    "area": {
                        "id": "fde48b0e-8c5f-4683-8cec-c29e7284ebf5",
                        "name": "المعذر"
                    },
                    "value": 22417
                },
                {
                    "area": {
                        "id": "228ef43a-9e3e-48cb-bf5e-893d71a6554a",
                        "name": "الرائد"
                    },
                    "value": 21541
                },
                {
                    "area": {
                        "id": "843fce03-4fe4-4981-a161-b2284321d375",
                        "name": "النموذجية"
                    },
                    "value": 18422
                },
                {
                    "area": {
                        "id": "e8c5f0cc-8565-4a1e-b40d-f1727489f6aa",
                        "name": "الخزامى"
                    },
                    "value": 18150
                },
                {
                    "area": {
                        "id": "e59fe6ef-9353-440d-b502-dc8ff67b99fb",
                        "name": "عريض"
                    },
                    "value": 16667
                },
                {
                    "area": {
                        "id": "da870943-28b0-48ef-a7e4-3237b6a3908c",
                        "name": "المحمدية"
                    },
                    "value": 16138
                },
                {
                    "area": {
                        "id": "5cf83942-e014-4a10-968d-408e1937b82e",
                        "name": "الورود"
                    },
                    "value": 15861
                },
                {
                    "area": {
                        "id": "3f6854d2-c64c-4718-98bb-00c9c1ff6cd3",
                        "name": "الغدير"
                    },
                    "value": 15825
                },
                {
                    "area": {
                        "id": "2ff065d6-764e-40b8-91fd-8210fad92c44",
                        "name": "الملك عبدالله"
                    },
                    "value": 15408
                },
                {
                    "area": {
                        "id": "a29b89a8-30fd-4d75-9945-ecfec789c7cc",
                        "name": "المهدية"
                    },
                    "value": 15167
                },
                {
                    "area": {
                        "id": "07310269-69f4-4e5a-a093-3b0686e6f92a",
                        "name": "الحمراء"
                    },
                    "value": 14577
                },
                {
                    "area": {
                        "id": "cf8c586f-e220-4ca5-b3d2-c68a2c39df91",
                        "name": "الندي"
                    },
                    "value": 14465
                },
                {
                    "area": {
                        "id": "8dbab168-3b00-4a12-bc76-dc9d95373cac",
                        "name": "أشبيلية"
                    },
                    "value": 14269
                },
                {
                    "area": {
                        "id": "d6d2d11e-2744-418e-904a-dc8ba194998e",
                        "name": "خشم العان"
                    },
                    "value": 14131
                },
                {
                    "area": {
                        "id": "900a8735-f91e-45b7-9702-c556cc4863bc",
                        "name": "الريان"
                    },
                    "value": 13845
                },
                {
                    "area": {
                        "id": "f2724a71-ad73-4765-8462-f299eff48fec",
                        "name": "القدس"
                    },
                    "value": 13799
                },
                {
                    "area": {
                        "id": "c82315c6-3142-41f8-96ff-bc8329391522",
                        "name": "السليمانية - الملز والبطحاء"
                    },
                    "value": 13748
                },
                {
                    "area": {
                        "id": "c7750a62-e42d-42eb-9e83-aa44bf10a777",
                        "name": "النخيل"
                    },
                    "value": 13531
                },
                {
                    "area": {
                        "id": "2f57568c-1f9d-4659-9d1b-70e720b0a45c",
                        "name": "التعاون"
                    },
                    "value": 13249
                },
                {
                    "area": {
                        "id": "a86339c7-1a18-4384-8800-76f1573c04a9",
                        "name": "الواحة"
                    },
                    "value": 13128
                },
                {
                    "area": {
                        "id": "d8229af8-3a8a-421b-8e4f-74969f448e47",
                        "name": "الملقا"
                    },
                    "value": 13123
                },
                {
                    "area": {
                        "id": "72b24564-20c8-4d3a-9d53-dd559786164d",
                        "name": "الفلاح"
                    },
                    "value": 12998
                },
                {
                    "area": {
                        "id": "edd4c9b9-7053-48cf-983e-81c681aab6f8",
                        "name": "حطين"
                    },
                    "value": 12586
                },
                {
                    "area": {
                        "id": "ce4632d7-923a-409e-864a-b9c0e25775b6",
                        "name": "العارض"
                    },
                    "value": 12432
                },
                {
                    "area": {
                        "id": "aa3edb6a-2aaa-4f34-891b-32fd7a64014e",
                        "name": "الربيع"
                    },
                    "value": 12419
                },
                {
                    "area": {
                        "id": "1d18118a-09f4-46a3-a7fe-9f8a4aba9058",
                        "name": "غرناطة"
                    },
                    "value": 12329
                },
                {
                    "area": {
                        "id": "ca70401b-2dbf-4153-afcf-35969ce14bfd",
                        "name": "الصحافة"
                    },
                    "value": 11969
                },
                {
                    "area": {
                        "id": "38434635-316c-4696-bf6e-0d350cf2e76a",
                        "name": "عليشة"
                    },
                    "value": 11948
                },
                {
                    "area": {
                        "id": "7bc70bab-8ac6-42d1-9d55-922d0df681d2",
                        "name": "الربوة"
                    },
                    "value": 11921
                },
                {
                    "area": {
                        "id": "c8f985cb-9b86-4d57-957f-b09b2ae78ab9",
                        "name": "المروج"
                    },
                    "value": 11806
                },
                {
                    "area": {
                        "id": "7c07ad55-b15f-48f6-9aed-ebc1e67eff45",
                        "name": "الرمال"
                    },
                    "value": 11639
                },
                {
                    "area": {
                        "id": "d36380e7-28b8-4926-a30f-8fc9327abfb1",
                        "name": "النزهه"
                    },
                    "value": 11613
                },
                {
                    "area": {
                        "id": "206645fd-79d5-44fb-bcc7-4bdafd602a9b",
                        "name": "النفل"
                    },
                    "value": 11529
                },
                {
                    "area": {
                        "id": "48539b17-54d3-4f28-968c-025684a0ceab",
                        "name": "الملك فيصل"
                    },
                    "value": 11518
                },
                {
                    "area": {
                        "id": "a01d452c-3a36-4f1b-9ede-2eeb934405a8",
                        "name": "الرفيعة"
                    },
                    "value": 11498
                },
                {
                    "area": {
                        "id": "cbb041b7-f87c-4878-821c-16ca4f34e10b",
                        "name": "الياسمين"
                    },
                    "value": 11343
                },
                {
                    "area": {
                        "id": "8dba8acc-a41e-4473-8a52-10622bee365b",
                        "name": "الدريهمية"
                    },
                    "value": 11316
                },
                {
                    "area": {
                        "id": "ec66cc90-a1c0-4cb5-873d-7c4757b69971",
                        "name": "الأندلس"
                    },
                    "value": 11303
                },
                {
                    "area": {
                        "id": "6720febf-8019-40cf-9446-5b2c8474d04d",
                        "name": "الرماية"
                    },
                    "value": 11227
                },
                {
                    "area": {
                        "id": "3b880a15-edb7-459d-817b-bbb4e5212ab9",
                        "name": "عكاظ"
                    },
                    "value": 11218
                },
                {
                    "area": {
                        "id": "ea03b9a1-d5f3-469f-a9fb-cfb72df61d7f",
                        "name": "المعذر الشمالي"
                    },
                    "value": 11183
                },
                {
                    "area": {
                        "id": "c1b851a6-029c-42bc-97f5-bd72af99b3ed",
                        "name": "الروابي"
                    },
                    "value": 11181
                },
                {
                    "area": {
                        "id": "0d7ff18e-c7e2-4607-a063-8b7c73b99838",
                        "name": "العليا - المعذر"
                    },
                    "value": 11112
                },
                {
                    "area": {
                        "id": "68b0afd0-e462-4930-936b-20532c79f1ad",
                        "name": "قرطبة"
                    },
                    "value": 11106
                },
                {
                    "area": {
                        "id": "5e21ce61-1c87-4d44-bb79-62c105b36cc4",
                        "name": "المغرزات"
                    },
                    "value": 11097
                },
                {
                    "area": {
                        "id": "5b05c230-55c9-499b-a012-887d53d66800",
                        "name": "المربع"
                    },
                    "value": 11021
                },
                {
                    "area": {
                        "id": "d8f9c2f5-91d2-4806-be75-b4d5e229e084",
                        "name": "المرسلات"
                    },
                    "value": 10929
                },
                {
                    "area": {
                        "id": "f659dd2c-ba77-464d-8a3d-70771ceda67c",
                        "name": "الصفاء"
                    },
                    "value": 10768
                },
                {
                    "area": {
                        "id": "b1a6d8da-05c8-40fd-87e3-6b99a97079d2",
                        "name": "المنار"
                    },
                    "value": 10766
                },
                {
                    "area": {
                        "id": "c59c5455-500a-4d2b-a7b4-6802fb3f170c",
                        "name": "الرمال"
                    },
                    "value": 10764
                },
                {
                    "area": {
                        "id": "d0759107-5d0c-4fb3-8ac2-745dbe717ed0",
                        "name": "المصيف"
                    },
                    "value": 10644
                },
                {
                    "area": {
                        "id": "86cdd3cf-82dd-461a-8764-5778344f1666",
                        "name": "الفيحاء"
                    },
                    "value": 10578
                },
                {
                    "area": {
                        "id": "009e646e-bb16-4a74-adda-4791c4cbc9c1",
                        "name": "السليمانية - العليا"
                    },
                    "value": 10542
                },
                {
                    "area": {
                        "id": "4731263b-77e7-4938-adc7-a7c5f81b3900",
                        "name": "القيروان"
                    },
                    "value": 10490
                },
                {
                    "area": {
                        "id": "62a893fc-9ec9-4e13-a01e-7191f976e312",
                        "name": "الروضة"
                    },
                    "value": 10489
                },
                {
                    "area": {
                        "id": "52d2e2cd-fbb4-4830-84cc-58ae92d267a6",
                        "name": "الإزدهار"
                    },
                    "value": 10390
                },
                {
                    "area": {
                        "id": "d7a56eca-bec8-49e9-ab68-bfa73a314faa",
                        "name": "السلام"
                    },
                    "value": 10301
                },
                {
                    "area": {
                        "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
                        "name": "صلاح الدين"
                    },
                    "value": 10255
                },
                {
                    "area": {
                        "id": "67ebb7a3-cd3d-480c-ba20-20e8c55c8332",
                        "name": "الرحمانية"
                    },
                    "value": 10230
                },
                {
                    "area": {
                        "id": "ed69f3e8-523c-4ce7-a493-e92f4f9f1986",
                        "name": "أم الحمام الغربي"
                    },
                    "value": 10189
                },
                {
                    "area": {
                        "id": "c37bc305-4ffc-4489-a6e3-9269b32edb1a",
                        "name": "الإسكان"
                    },
                    "value": 10186
                },
                {
                    "area": {
                        "id": "1f8ff56c-ade7-476d-9a18-ebf538ec1767",
                        "name": "الوادي"
                    },
                    "value": 10105
                },
                {
                    "area": {
                        "id": "cfa2d353-9107-4b34-bccf-533aac553ab4",
                        "name": "الزهراء"
                    },
                    "value": 10088
                },
                {
                    "area": {
                        "id": "d3e1ad91-49ce-4b0c-bb5d-1fffecd8fafa",
                        "name": "اليرموك"
                    },
                    "value": 10074
                },
                {
                    "area": {
                        "id": "98f7f0d1-438f-4c87-a98f-e0fda41b84bd",
                        "name": "ظهرة نمار"
                    },
                    "value": 10043
                },
                {
                    "area": {
                        "id": "4ed2e10c-2b71-4414-a8f3-9b8a3f30e560",
                        "name": "العقيق"
                    },
                    "value": 10014
                },
                {
                    "area": {
                        "id": "a7e5ebed-efe6-4956-a53a-19f21c4a2cf9",
                        "name": "المونسية"
                    },
                    "value": 9964
                },
                {
                    "area": {
                        "id": "febe47f1-831b-472c-a068-339a65069dd3",
                        "name": "المعزيلة"
                    },
                    "value": 9908
                },
                {
                    "area": {
                        "id": "2b62095b-102f-441f-ac00-34602cd48536",
                        "name": "الجزيرة"
                    },
                    "value": 9893
                },
                {
                    "area": {
                        "id": "b4aed3f7-045a-443e-b340-81043580d7b9",
                        "name": "هجرة وادي لبن"
                    },
                    "value": 9890
                },
                {
                    "area": {
                        "id": "cd6e3719-5fb9-497a-91b9-e2668e2e75a6",
                        "name": "الهدا - الديرة"
                    },
                    "value": 9833
                },
                {
                    "area": {
                        "id": "aa140531-ded7-47f4-b7d5-591930d0316b",
                        "name": "النهضة"
                    },
                    "value": 9639
                },
                {
                    "area": {
                        "id": "c0c6513b-13b9-45e1-848a-a4959f95971a",
                        "name": "الملك فهد"
                    },
                    "value": 9594
                },
                {
                    "area": {
                        "id": "8014f925-e0b7-4af1-9d9b-20c75afca882",
                        "name": "العليا - الملز والبطحاء"
                    },
                    "value": 9533
                },
                {
                    "area": {
                        "id": "aff3e994-cc0a-4e88-912d-0690a9983b27",
                        "name": "السويدي الغربي"
                    },
                    "value": 9455
                },
                {
                    "area": {
                        "id": "2c51be33-11eb-4645-a407-92d9acd33c9c",
                        "name": "عرقة"
                    },
                    "value": 9379
                },
                {
                    "area": {
                        "id": "d096152a-b6d5-49c8-84b9-b9ca4a46fd2d",
                        "name": "العليا - العليا"
                    },
                    "value": 9360
                },
                {
                    "area": {
                        "id": "e9de74de-e178-4d06-856f-1689820e2c5a",
                        "name": "شبرا"
                    },
                    "value": 9360
                },
                {
                    "area": {
                        "id": "f96795fc-dd23-4de7-9d54-f9050c0f8e9d",
                        "name": "النرجس"
                    },
                    "value": 9353
                },
                {
                    "area": {
                        "id": "2fa38d65-6151-493e-98aa-c14c06a28197",
                        "name": "الفاخرية"
                    },
                    "value": 9251
                },
                {
                    "area": {
                        "id": "30db56d8-31f6-4a21-81fa-f135163359b1",
                        "name": "الخليج"
                    },
                    "value": 8988
                },
                {
                    "area": {
                        "id": "842383e2-3091-4283-b65c-f4a62cd18784",
                        "name": "ظهرة لبن"
                    },
                    "value": 8977
                },
                {
                    "area": {
                        "id": "bf723f44-607f-4114-91b9-db8cd0c77a91",
                        "name": "الشفاء"
                    },
                    "value": 8841
                },
                {
                    "area": {
                        "id": "43f724c9-8295-46e4-b80d-af74e659b872",
                        "name": "العريجاء الغربية"
                    },
                    "value": 8808
                },
                {
                    "area": {
                        "id": "e443160a-e66b-4369-a4bf-95f26060eccd",
                        "name": "الحزم"
                    },
                    "value": 8654
                },
                {
                    "area": {
                        "id": "471d8f88-5a0b-4890-8026-a63a835bf52a",
                        "name": "العوالي"
                    },
                    "value": 8607
                },
                {
                    "area": {
                        "id": "d85bc333-4975-421c-9d03-df228e6ae9ea",
                        "name": "الضباط"
                    },
                    "value": 8583
                },
                {
                    "area": {
                        "id": "0442bf29-e3f1-4dfa-8afd-b11e063b015a",
                        "name": "العريجاء الوسطى"
                    },
                    "value": 8223
                },
                {
                    "area": {
                        "id": "2be8f71f-bb94-4702-87d6-a258a14df452",
                        "name": "الزهرة"
                    },
                    "value": 8215
                },
                {
                    "area": {
                        "id": "b7aeff04-e705-4a9b-ae9f-0da2ac5b3d9e",
                        "name": "القادسية"
                    },
                    "value": 8155
                },
                {
                    "area": {
                        "id": "7b5f813e-a731-40ef-b3a0-afac81467277",
                        "name": "نمار"
                    },
                    "value": 8067
                },
                {
                    "area": {
                        "id": "city-3",
                        "name": "الرياض"
                    },
                    "value": 8009
                },
                {
                    "area": {
                        "id": "c9fe42ca-2797-466e-b1d1-cb90c69a5605",
                        "name": "المروه"
                    },
                    "value": 8005
                },
                {
                    "area": {
                        "id": "c7f18c78-aae4-4895-a83c-57ce0c761cd1",
                        "name": "جرير"
                    },
                    "value": 7961
                },
                {
                    "area": {
                        "id": "39ac02a1-c044-4620-9169-b472154e3768",
                        "name": "ظهرة البديعة"
                    },
                    "value": 7937
                },
                {
                    "area": {
                        "id": "7a9f08b6-502e-4300-87ac-3dc37a27e74c",
                        "name": "النظيم"
                    },
                    "value": 7805
                },
                {
                    "area": {
                        "id": "1297bd50-a138-4c61-9898-97d18963331a",
                        "name": "النسيم الشرقي"
                    },
                    "value": 7785
                },
                {
                    "area": {
                        "id": "b65ac3ce-46ab-419d-be64-7aa2761f4c28",
                        "name": "الجنادرية"
                    },
                    "value": 7783
                },
                {
                    "area": {
                        "id": "61ab70a4-3d37-47bd-a9ee-124bdc0fb670",
                        "name": "المنصورة"
                    },
                    "value": 7774
                },
                {
                    "area": {
                        "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                        "name": "السعادة"
                    },
                    "value": 7768
                },
                {
                    "area": {
                        "id": "1460a408-4989-4c5e-9e97-494e36c3497a",
                        "name": "ضاحية نمار"
                    },
                    "value": 7742
                },
                {
                    "area": {
                        "id": "c1df54b0-feac-4290-9e75-8afd9e313efb",
                        "name": "طويق - عتيقة"
                    },
                    "value": 7693
                },
                {
                    "area": {
                        "id": "40772979-0127-4648-b641-dee43ee6b96b",
                        "name": "السويدي"
                    },
                    "value": 7655
                },
                {
                    "area": {
                        "id": "1f314e74-fac1-4ebf-b83a-830ba70c09c3",
                        "name": "الدرعية"
                    },
                    "value": 7291
                },
                {
                    "area": {
                        "id": "5b8e557e-aebe-4553-8402-8973b4ff0a79",
                        "name": "العزيزية"
                    },
                    "value": 7289
                },
                {
                    "area": {
                        "id": "751de8ea-eab5-45f3-801f-6a969a57b4e7",
                        "name": "الفاروق"
                    },
                    "value": 7218
                },
                {
                    "area": {
                        "id": "b91c2ee4-5fc7-4632-ac89-07e6fc008363",
                        "name": "الملز"
                    },
                    "value": 7165
                },
                {
                    "area": {
                        "id": "13d2af17-de45-4e53-9dcc-17f1f18ba0a1",
                        "name": "المؤتمرات"
                    },
                    "value": 6941
                },
                {
                    "area": {
                        "id": "4f6a0751-1320-4e27-913b-2dfec0d8aa2f",
                        "name": "الدار البيضاء"
                    },
                    "value": 6931
                },
                {
                    "area": {
                        "id": "920c7560-2916-44ef-ac0e-f1baac271657",
                        "name": "ديراب"
                    },
                    "value": 6836
                },
                {
                    "area": {
                        "id": "0434eb81-4f04-4007-92cc-b0c5410bea7c",
                        "name": "الفوطة"
                    },
                    "value": 6823
                },
                {
                    "area": {
                        "id": "5dfaa455-f597-4c2b-961e-cd2faf15d08f",
                        "name": "النسيم الغربي"
                    },
                    "value": 6754
                },
                {
                    "area": {
                        "id": "01c9ff6a-eb28-4465-a68c-c8a5562c6d39",
                        "name": "بدر"
                    },
                    "value": 6637
                },
                {
                    "area": {
                        "id": "f8bed1dc-356d-43a9-b89b-9d1446a74683",
                        "name": "الحائر"
                    },
                    "value": 6138
                },
                {
                    "area": {
                        "id": "758da835-c682-46d6-82ad-0d9fb8442113",
                        "name": "العريجاء"
                    },
                    "value": 5955
                },
                {
                    "area": {
                        "id": "ea504b74-c266-4b09-b298-08e9dfb35eb5",
                        "name": "الـشـرفـيـة"
                    },
                    "value": 5906
                },
                {
                    "area": {
                        "id": "14561646-f4ae-4c62-b7f1-8f95156cc0ef",
                        "name": "أحـد"
                    },
                    "value": 5901
                },
                {
                    "area": {
                        "id": "88251c8e-068a-4862-aff5-b6c2feb5e876",
                        "name": "الوشام"
                    },
                    "value": 5576
                },
                {
                    "area": {
                        "id": "0e8da9c4-e4a7-4794-a62d-9ab0554e7579",
                        "name": "أم الحمام الشرقي - الديرة"
                    },
                    "value": 5515
                },
                {
                    "area": {
                        "id": "27783c9e-535f-4d44-9a5d-ed549644c5be",
                        "name": "سلطانة - العريجاء"
                    },
                    "value": 5498
                },
                {
                    "area": {
                        "id": "9d09b05f-35f3-4925-84b1-978e9d701e5e",
                        "name": "أم الحمام الشرقي - المعذر"
                    },
                    "value": 5483
                },
                {
                    "area": {
                        "id": "f0eb256e-8c6b-4943-9812-8a10c483b65d",
                        "name": "هيت"
                    },
                    "value": 4838
                },
                {
                    "area": {
                        "id": "fcf3bfcc-4e81-4db1-8fe5-ef65fc610991",
                        "name": "البديعة"
                    },
                    "value": 4756
                },
                {
                    "area": {
                        "id": "9c5397a5-f624-4116-8db2-34ecf79e5315",
                        "name": "الفيصلية"
                    },
                    "value": 4472
                },
                {
                    "area": {
                        "id": "7a4897d9-89ac-4d95-a544-2aeee4f1beb2",
                        "name": "الصناعية"
                    },
                    "value": 4411
                },
                {
                    "area": {
                        "id": "6eea7b8d-e938-466a-ac3e-ae2b106ac59f",
                        "name": "النور"
                    },
                    "value": 4067
                },
                {
                    "area": {
                        "id": "dde02562-5497-4b68-bb19-baa4d9e93db5",
                        "name": "الخالدية"
                    },
                    "value": 3808
                },
                {
                    "area": {
                        "id": "feb5834c-f023-44d4-8a14-35dc6629017d",
                        "name": "العمل"
                    },
                    "value": 3805
                },
                {
                    "area": {
                        "id": "c8fbfbfe-c1a0-4079-be04-ad20730038b0",
                        "name": "الوزارات"
                    },
                    "value": 3766
                },
                {
                    "area": {
                        "id": "1a94924e-c8b8-47ae-b6f4-595f4acf8b3d",
                        "name": "غبيراء"
                    },
                    "value": 3738
                },
                {
                    "area": {
                        "id": "27c6e7ac-e6e9-49c9-abc9-c179249cf345",
                        "name": "المناخ"
                    },
                    "value": 3520
                },
                {
                    "area": {
                        "id": "6a6535f2-c3fc-408d-8de8-4d048dd19728",
                        "name": "اليمامة"
                    },
                    "value": 3509
                },
                {
                    "area": {
                        "id": "33808d06-6a8a-42c1-86b2-79b4709905fd",
                        "name": "الناصرية"
                    },
                    "value": 3152
                },
                {
                    "area": {
                        "id": "19381f2a-1d68-4fc3-bc5a-09d5481cf03b",
                        "name": "الجرادية"
                    },
                    "value": 3075
                },
                {
                    "area": {
                        "id": "b9945c44-61a0-4d1e-85f2-24eefe9611ae",
                        "name": "سلطانة - الديرة"
                    },
                    "value": 3068
                },
                {
                    "area": {
                        "id": "1bdf2e61-64d7-42c7-bd24-3b58fa806746",
                        "name": "جبرة"
                    },
                    "value": 3058
                },
                {
                    "area": {
                        "id": "05fe6a6f-34eb-45eb-82be-260adddd6082",
                        "name": "عتيقة"
                    },
                    "value": 3001
                },
                {
                    "area": {
                        "id": "3f6c38e8-6b3e-4775-8e1a-905b71f5858a",
                        "name": "الصالحية"
                    },
                    "value": 2902
                },
                {
                    "area": {
                        "id": "fd3f2823-fefa-4c52-aaa9-60150ebd0c37",
                        "name": "الديرة"
                    },
                    "value": 2897
                },
                {
                    "area": {
                        "id": "332ccd9e-8159-49fe-935d-bbb98730c2fc",
                        "name": "الشميسي"
                    },
                    "value": 2860
                },
                {
                    "area": {
                        "id": "1570d51a-3e9a-4b78-acb2-3d5389cd2a81",
                        "name": "منفوحة الجديدة"
                    },
                    "value": 2780
                },
                {
                    "area": {
                        "id": "51c12d2a-9ae8-4266-adc3-5126aa359cd3",
                        "name": "العود"
                    },
                    "value": 2752
                },
                {
                    "area": {
                        "id": "113113e3-21a3-4a3a-bfae-3dd799ded51c",
                        "name": "الوسيطا"
                    },
                    "value": 2721
                },
                {
                    "area": {
                        "id": "7dd2b8d2-e89d-408b-bc10-b735809ff749",
                        "name": "المرقب"
                    },
                    "value": 2623
                },
                {
                    "area": {
                        "id": "aa913c8f-ae16-4ee9-a414-1318cda9c41a",
                        "name": "ثليم"
                    },
                    "value": 2497
                },
                {
                    "area": {
                        "id": "66566263-1c8d-4e72-85e1-406464b90bbe",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 2434
                },
                {
                    "area": {
                        "id": "e85c3bb7-6f91-41de-8447-7a274dc46df3",
                        "name": "أم سليم"
                    },
                    "value": 2404
                },
                {
                    "area": {
                        "id": "ff86addf-942e-41dc-bb0f-9269251b42a3",
                        "name": "منفوحة"
                    },
                    "value": 2349
                },
                {
                    "area": {
                        "id": "b2fbbbbc-f12f-44a5-8e76-a674c7a1a9e0",
                        "name": "معكال"
                    },
                    "value": 2258
                },
                {
                    "area": {
                        "id": "3c56b430-f38e-4714-81e3-8a502f8fb971",
                        "name": "السلي"
                    },
                    "value": 1960
                },
                {
                    "area": {
                        "id": "888e14d1-e0da-4731-a7d7-605372279f88",
                        "name": "الدوبية"
                    },
                    "value": 1956
                },
                {
                    "area": {
                        "id": "7e0fd377-cd04-4845-8b7f-7144752aea0d",
                        "name": "الدفاع"
                    },
                    "value": 1907
                }
            ]
        },
        "female": {
            "facts": [
                {
                    "area": {
                        "id": "aa21340b-3580-4a62-8a43-3d12f6b00501",
                        "name": "السفارات"
                    },
                    "value": 18583
                },
                {
                    "area": {
                        "id": "1460a408-4989-4c5e-9e97-494e36c3497a",
                        "name": "ضاحية نمار"
                    },
                    "value": 14000
                },
                {
                    "area": {
                        "id": "228ef43a-9e3e-48cb-bf5e-893d71a6554a",
                        "name": "الرائد"
                    },
                    "value": 13333
                },
                {
                    "area": {
                        "id": "05fe6a6f-34eb-45eb-82be-260adddd6082",
                        "name": "عتيقة"
                    },
                    "value": 12125
                },
                {
                    "area": {
                        "id": "7dd2b8d2-e89d-408b-bc10-b735809ff749",
                        "name": "المرقب"
                    },
                    "value": 10300
                },
                {
                    "area": {
                        "id": "1bdf2e61-64d7-42c7-bd24-3b58fa806746",
                        "name": "جبرة"
                    },
                    "value": 9650
                },
                {
                    "area": {
                        "id": "b7aeff04-e705-4a9b-ae9f-0da2ac5b3d9e",
                        "name": "القادسية"
                    },
                    "value": 9341
                },
                {
                    "area": {
                        "id": "c7f18c78-aae4-4895-a83c-57ce0c761cd1",
                        "name": "جرير"
                    },
                    "value": 8603
                },
                {
                    "area": {
                        "id": "c59c5455-500a-4d2b-a7b4-6802fb3f170c",
                        "name": "الرمال"
                    },
                    "value": 7421
                },
                {
                    "area": {
                        "id": "33808d06-6a8a-42c1-86b2-79b4709905fd",
                        "name": "الناصرية"
                    },
                    "value": 7383
                },
                {
                    "area": {
                        "id": "3b880a15-edb7-459d-817b-bbb4e5212ab9",
                        "name": "عكاظ"
                    },
                    "value": 7373
                },
                {
                    "area": {
                        "id": "5cf83942-e014-4a10-968d-408e1937b82e",
                        "name": "الورود"
                    },
                    "value": 7260
                },
                {
                    "area": {
                        "id": "b1a6d8da-05c8-40fd-87e3-6b99a97079d2",
                        "name": "المنار"
                    },
                    "value": 7169
                },
                {
                    "area": {
                        "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                        "name": "السعادة"
                    },
                    "value": 7149
                },
                {
                    "area": {
                        "id": "1d18118a-09f4-46a3-a7fe-9f8a4aba9058",
                        "name": "غرناطة"
                    },
                    "value": 7043
                },
                {
                    "area": {
                        "id": "d096152a-b6d5-49c8-84b9-b9ca4a46fd2d",
                        "name": "العليا - العليا"
                    },
                    "value": 7001
                },
                {
                    "area": {
                        "id": "0434eb81-4f04-4007-92cc-b0c5410bea7c",
                        "name": "الفوطة"
                    },
                    "value": 7000
                },
                {
                    "area": {
                        "id": "07310269-69f4-4e5a-a093-3b0686e6f92a",
                        "name": "الحمراء"
                    },
                    "value": 6971
                },
                {
                    "area": {
                        "id": "a86339c7-1a18-4384-8800-76f1573c04a9",
                        "name": "الواحة"
                    },
                    "value": 6967
                },
                {
                    "area": {
                        "id": "d3e1ad91-49ce-4b0c-bb5d-1fffecd8fafa",
                        "name": "اليرموك"
                    },
                    "value": 6727
                },
                {
                    "area": {
                        "id": "e8c5f0cc-8565-4a1e-b40d-f1727489f6aa",
                        "name": "الخزامى"
                    },
                    "value": 6667
                },
                {
                    "area": {
                        "id": "13d2af17-de45-4e53-9dcc-17f1f18ba0a1",
                        "name": "المؤتمرات"
                    },
                    "value": 6600
                },
                {
                    "area": {
                        "id": "2c51be33-11eb-4645-a407-92d9acd33c9c",
                        "name": "عرقة"
                    },
                    "value": 6584
                },
                {
                    "area": {
                        "id": "a7e5ebed-efe6-4956-a53a-19f21c4a2cf9",
                        "name": "المونسية"
                    },
                    "value": 6570
                },
                {
                    "area": {
                        "id": "471d8f88-5a0b-4890-8026-a63a835bf52a",
                        "name": "العوالي"
                    },
                    "value": 6537
                },
                {
                    "area": {
                        "id": "f2724a71-ad73-4765-8462-f299eff48fec",
                        "name": "القدس"
                    },
                    "value": 6535
                },
                {
                    "area": {
                        "id": "4f6a0751-1320-4e27-913b-2dfec0d8aa2f",
                        "name": "الدار البيضاء"
                    },
                    "value": 6526
                },
                {
                    "area": {
                        "id": "8dbab168-3b00-4a12-bc76-dc9d95373cac",
                        "name": "أشبيلية"
                    },
                    "value": 6465
                },
                {
                    "area": {
                        "id": "c8fbfbfe-c1a0-4079-be04-ad20730038b0",
                        "name": "الوزارات"
                    },
                    "value": 6431
                },
                {
                    "area": {
                        "id": "e443160a-e66b-4369-a4bf-95f26060eccd",
                        "name": "الحزم"
                    },
                    "value": 6369
                },
                {
                    "area": {
                        "id": "ea03b9a1-d5f3-469f-a9fb-cfb72df61d7f",
                        "name": "المعذر الشمالي"
                    },
                    "value": 6311
                },
                {
                    "area": {
                        "id": "cf8c586f-e220-4ca5-b3d2-c68a2c39df91",
                        "name": "الندي"
                    },
                    "value": 6239
                },
                {
                    "area": {
                        "id": "d85bc333-4975-421c-9d03-df228e6ae9ea",
                        "name": "الضباط"
                    },
                    "value": 6218
                },
                {
                    "area": {
                        "id": "0442bf29-e3f1-4dfa-8afd-b11e063b015a",
                        "name": "العريجاء الوسطى"
                    },
                    "value": 6161
                },
                {
                    "area": {
                        "id": "8dba8acc-a41e-4473-8a52-10622bee365b",
                        "name": "الدريهمية"
                    },
                    "value": 6080
                },
                {
                    "area": {
                        "id": "ec66cc90-a1c0-4cb5-873d-7c4757b69971",
                        "name": "الأندلس"
                    },
                    "value": 6064
                },
                {
                    "area": {
                        "id": "d36380e7-28b8-4926-a30f-8fc9327abfb1",
                        "name": "النزهه"
                    },
                    "value": 6029
                },
                {
                    "area": {
                        "id": "66566263-1c8d-4e72-85e1-406464b90bbe",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 6000
                },
                {
                    "area": {
                        "id": "3f6854d2-c64c-4718-98bb-00c9c1ff6cd3",
                        "name": "الغدير"
                    },
                    "value": 5863
                },
                {
                    "area": {
                        "id": "7a9f08b6-502e-4300-87ac-3dc37a27e74c",
                        "name": "النظيم"
                    },
                    "value": 5839
                },
                {
                    "area": {
                        "id": "2b62095b-102f-441f-ac00-34602cd48536",
                        "name": "الجزيرة"
                    },
                    "value": 5813
                },
                {
                    "area": {
                        "id": "4731263b-77e7-4938-adc7-a7c5f81b3900",
                        "name": "القيروان"
                    },
                    "value": 5811
                },
                {
                    "area": {
                        "id": "d0759107-5d0c-4fb3-8ac2-745dbe717ed0",
                        "name": "المصيف"
                    },
                    "value": 5810
                },
                {
                    "area": {
                        "id": "c37bc305-4ffc-4489-a6e3-9269b32edb1a",
                        "name": "الإسكان"
                    },
                    "value": 5795
                },
                {
                    "area": {
                        "id": "fde48b0e-8c5f-4683-8cec-c29e7284ebf5",
                        "name": "المعذر"
                    },
                    "value": 5750
                },
                {
                    "area": {
                        "id": "d7a56eca-bec8-49e9-ab68-bfa73a314faa",
                        "name": "السلام"
                    },
                    "value": 5724
                },
                {
                    "area": {
                        "id": "1f8ff56c-ade7-476d-9a18-ebf538ec1767",
                        "name": "الوادي"
                    },
                    "value": 5711
                },
                {
                    "area": {
                        "id": "1570d51a-3e9a-4b78-acb2-3d5389cd2a81",
                        "name": "منفوحة الجديدة"
                    },
                    "value": 5640
                },
                {
                    "area": {
                        "id": "206645fd-79d5-44fb-bcc7-4bdafd602a9b",
                        "name": "النفل"
                    },
                    "value": 5624
                },
                {
                    "area": {
                        "id": "43f724c9-8295-46e4-b80d-af74e659b872",
                        "name": "العريجاء الغربية"
                    },
                    "value": 5612
                },
                {
                    "area": {
                        "id": "1297bd50-a138-4c61-9898-97d18963331a",
                        "name": "النسيم الشرقي"
                    },
                    "value": 5564
                },
                {
                    "area": {
                        "id": "aa3edb6a-2aaa-4f34-891b-32fd7a64014e",
                        "name": "الربيع"
                    },
                    "value": 5549
                },
                {
                    "area": {
                        "id": "da870943-28b0-48ef-a7e4-3237b6a3908c",
                        "name": "المحمدية"
                    },
                    "value": 5518
                },
                {
                    "area": {
                        "id": "47e60f73-b741-4d9e-87e4-a4e613d37cde",
                        "name": "الملك عبد العزيز"
                    },
                    "value": 5509
                },
                {
                    "area": {
                        "id": "68b0afd0-e462-4930-936b-20532c79f1ad",
                        "name": "قرطبة"
                    },
                    "value": 5507
                },
                {
                    "area": {
                        "id": "7c07ad55-b15f-48f6-9aed-ebc1e67eff45",
                        "name": "الرمال"
                    },
                    "value": 5500
                },
                {
                    "area": {
                        "id": "2be8f71f-bb94-4702-87d6-a258a14df452",
                        "name": "الزهرة"
                    },
                    "value": 5496
                },
                {
                    "area": {
                        "id": "bf723f44-607f-4114-91b9-db8cd0c77a91",
                        "name": "الشفاء"
                    },
                    "value": 5428
                },
                {
                    "area": {
                        "id": "city-3",
                        "name": "الرياض"
                    },
                    "value": 5385
                },
                {
                    "area": {
                        "id": "72b24564-20c8-4d3a-9d53-dd559786164d",
                        "name": "الفلاح"
                    },
                    "value": 5375
                },
                {
                    "area": {
                        "id": "1f314e74-fac1-4ebf-b83a-830ba70c09c3",
                        "name": "الدرعية"
                    },
                    "value": 5364
                },
                {
                    "area": {
                        "id": "4ed2e10c-2b71-4414-a8f3-9b8a3f30e560",
                        "name": "العقيق"
                    },
                    "value": 5354
                },
                {
                    "area": {
                        "id": "86cdd3cf-82dd-461a-8764-5778344f1666",
                        "name": "الفيحاء"
                    },
                    "value": 5344
                },
                {
                    "area": {
                        "id": "5e21ce61-1c87-4d44-bb79-62c105b36cc4",
                        "name": "المغرزات"
                    },
                    "value": 5321
                },
                {
                    "area": {
                        "id": "cd6e3719-5fb9-497a-91b9-e2668e2e75a6",
                        "name": "الهدا - الديرة"
                    },
                    "value": 5320
                },
                {
                    "area": {
                        "id": "aa140531-ded7-47f4-b7d5-591930d0316b",
                        "name": "النهضة"
                    },
                    "value": 5296
                },
                {
                    "area": {
                        "id": "7bc70bab-8ac6-42d1-9d55-922d0df681d2",
                        "name": "الربوة"
                    },
                    "value": 5288
                },
                {
                    "area": {
                        "id": "52d2e2cd-fbb4-4830-84cc-58ae92d267a6",
                        "name": "الإزدهار"
                    },
                    "value": 5286
                },
                {
                    "area": {
                        "id": "01c9ff6a-eb28-4465-a68c-c8a5562c6d39",
                        "name": "بدر"
                    },
                    "value": 5280
                },
                {
                    "area": {
                        "id": "40772979-0127-4648-b641-dee43ee6b96b",
                        "name": "السويدي"
                    },
                    "value": 5256
                },
                {
                    "area": {
                        "id": "b91c2ee4-5fc7-4632-ac89-07e6fc008363",
                        "name": "الملز"
                    },
                    "value": 5238
                },
                {
                    "area": {
                        "id": "cfa2d353-9107-4b34-bccf-533aac553ab4",
                        "name": "الزهراء"
                    },
                    "value": 5231
                },
                {
                    "area": {
                        "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
                        "name": "صلاح الدين"
                    },
                    "value": 5207
                },
                {
                    "area": {
                        "id": "c8f985cb-9b86-4d57-957f-b09b2ae78ab9",
                        "name": "المروج"
                    },
                    "value": 5194
                },
                {
                    "area": {
                        "id": "edd4c9b9-7053-48cf-983e-81c681aab6f8",
                        "name": "حطين"
                    },
                    "value": 5120
                },
                {
                    "area": {
                        "id": "c7750a62-e42d-42eb-9e83-aa44bf10a777",
                        "name": "النخيل"
                    },
                    "value": 5113
                },
                {
                    "area": {
                        "id": "900a8735-f91e-45b7-9702-c556cc4863bc",
                        "name": "الريان"
                    },
                    "value": 5034
                },
                {
                    "area": {
                        "id": "2f57568c-1f9d-4659-9d1b-70e720b0a45c",
                        "name": "التعاون"
                    },
                    "value": 5004
                },
                {
                    "area": {
                        "id": "842383e2-3091-4283-b65c-f4a62cd18784",
                        "name": "ظهرة لبن"
                    },
                    "value": 4999
                },
                {
                    "area": {
                        "id": "c0c6513b-13b9-45e1-848a-a4959f95971a",
                        "name": "الملك فهد"
                    },
                    "value": 4995
                },
                {
                    "area": {
                        "id": "ca70401b-2dbf-4153-afcf-35969ce14bfd",
                        "name": "الصحافة"
                    },
                    "value": 4995
                },
                {
                    "area": {
                        "id": "5b05c230-55c9-499b-a012-887d53d66800",
                        "name": "المربع"
                    },
                    "value": 4991
                },
                {
                    "area": {
                        "id": "7b5f813e-a731-40ef-b3a0-afac81467277",
                        "name": "نمار"
                    },
                    "value": 4962
                },
                {
                    "area": {
                        "id": "cbb041b7-f87c-4878-821c-16ca4f34e10b",
                        "name": "الياسمين"
                    },
                    "value": 4926
                },
                {
                    "area": {
                        "id": "c1b851a6-029c-42bc-97f5-bd72af99b3ed",
                        "name": "الروابي"
                    },
                    "value": 4913
                },
                {
                    "area": {
                        "id": "2ff065d6-764e-40b8-91fd-8210fad92c44",
                        "name": "الملك عبدالله"
                    },
                    "value": 4889
                },
                {
                    "area": {
                        "id": "0d7ff18e-c7e2-4607-a063-8b7c73b99838",
                        "name": "العليا - المعذر"
                    },
                    "value": 4885
                },
                {
                    "area": {
                        "id": "d8229af8-3a8a-421b-8e4f-74969f448e47",
                        "name": "الملقا"
                    },
                    "value": 4884
                },
                {
                    "area": {
                        "id": "30db56d8-31f6-4a21-81fa-f135163359b1",
                        "name": "الخليج"
                    },
                    "value": 4880
                },
                {
                    "area": {
                        "id": "5dfaa455-f597-4c2b-961e-cd2faf15d08f",
                        "name": "النسيم الغربي"
                    },
                    "value": 4876
                },
                {
                    "area": {
                        "id": "d6d2d11e-2744-418e-904a-dc8ba194998e",
                        "name": "خشم العان"
                    },
                    "value": 4843
                },
                {
                    "area": {
                        "id": "7a4897d9-89ac-4d95-a544-2aeee4f1beb2",
                        "name": "الصناعية"
                    },
                    "value": 4825
                },
                {
                    "area": {
                        "id": "843fce03-4fe4-4981-a161-b2284321d375",
                        "name": "النموذجية"
                    },
                    "value": 4817
                },
                {
                    "area": {
                        "id": "c1df54b0-feac-4290-9e75-8afd9e313efb",
                        "name": "طويق - عتيقة"
                    },
                    "value": 4810
                },
                {
                    "area": {
                        "id": "39ac02a1-c044-4620-9169-b472154e3768",
                        "name": "ظهرة البديعة"
                    },
                    "value": 4795
                },
                {
                    "area": {
                        "id": "009e646e-bb16-4a74-adda-4791c4cbc9c1",
                        "name": "السليمانية - العليا"
                    },
                    "value": 4783
                },
                {
                    "area": {
                        "id": "b4aed3f7-045a-443e-b340-81043580d7b9",
                        "name": "هجرة وادي لبن"
                    },
                    "value": 4756
                },
                {
                    "area": {
                        "id": "b65ac3ce-46ab-419d-be64-7aa2761f4c28",
                        "name": "الجنادرية"
                    },
                    "value": 4710
                },
                {
                    "area": {
                        "id": "48539b17-54d3-4f28-968c-025684a0ceab",
                        "name": "الملك فيصل"
                    },
                    "value": 4691
                },
                {
                    "area": {
                        "id": "c82315c6-3142-41f8-96ff-bc8329391522",
                        "name": "السليمانية - الملز والبطحاء"
                    },
                    "value": 4675
                },
                {
                    "area": {
                        "id": "62a893fc-9ec9-4e13-a01e-7191f976e312",
                        "name": "الروضة"
                    },
                    "value": 4581
                },
                {
                    "area": {
                        "id": "aff3e994-cc0a-4e88-912d-0690a9983b27",
                        "name": "السويدي الغربي"
                    },
                    "value": 4537
                },
                {
                    "area": {
                        "id": "0e8da9c4-e4a7-4794-a62d-9ab0554e7579",
                        "name": "أم الحمام الشرقي - الديرة"
                    },
                    "value": 4530
                },
                {
                    "area": {
                        "id": "5b8e557e-aebe-4553-8402-8973b4ff0a79",
                        "name": "العزيزية"
                    },
                    "value": 4520
                },
                {
                    "area": {
                        "id": "332ccd9e-8159-49fe-935d-bbb98730c2fc",
                        "name": "الشميسي"
                    },
                    "value": 4513
                },
                {
                    "area": {
                        "id": "e9de74de-e178-4d06-856f-1689820e2c5a",
                        "name": "شبرا"
                    },
                    "value": 4358
                },
                {
                    "area": {
                        "id": "f96795fc-dd23-4de7-9d54-f9050c0f8e9d",
                        "name": "النرجس"
                    },
                    "value": 4350
                },
                {
                    "area": {
                        "id": "d8f9c2f5-91d2-4806-be75-b4d5e229e084",
                        "name": "المرسلات"
                    },
                    "value": 4317
                },
                {
                    "area": {
                        "id": "88251c8e-068a-4862-aff5-b6c2feb5e876",
                        "name": "الوشام"
                    },
                    "value": 4277
                },
                {
                    "area": {
                        "id": "27c6e7ac-e6e9-49c9-abc9-c179249cf345",
                        "name": "المناخ"
                    },
                    "value": 4250
                },
                {
                    "area": {
                        "id": "758da835-c682-46d6-82ad-0d9fb8442113",
                        "name": "العريجاء"
                    },
                    "value": 4225
                },
                {
                    "area": {
                        "id": "c9fe42ca-2797-466e-b1d1-cb90c69a5605",
                        "name": "المروه"
                    },
                    "value": 4215
                },
                {
                    "area": {
                        "id": "14561646-f4ae-4c62-b7f1-8f95156cc0ef",
                        "name": "أحـد"
                    },
                    "value": 4170
                },
                {
                    "area": {
                        "id": "ce4632d7-923a-409e-864a-b9c0e25775b6",
                        "name": "العارض"
                    },
                    "value": 4096
                },
                {
                    "area": {
                        "id": "38434635-316c-4696-bf6e-0d350cf2e76a",
                        "name": "عليشة"
                    },
                    "value": 4012
                },
                {
                    "area": {
                        "id": "19381f2a-1d68-4fc3-bc5a-09d5481cf03b",
                        "name": "الجرادية"
                    },
                    "value": 4000
                },
                {
                    "area": {
                        "id": "98f7f0d1-438f-4c87-a98f-e0fda41b84bd",
                        "name": "ظهرة نمار"
                    },
                    "value": 3992
                },
                {
                    "area": {
                        "id": "1a94924e-c8b8-47ae-b6f4-595f4acf8b3d",
                        "name": "غبيراء"
                    },
                    "value": 3939
                },
                {
                    "area": {
                        "id": "aa913c8f-ae16-4ee9-a414-1318cda9c41a",
                        "name": "ثليم"
                    },
                    "value": 3900
                },
                {
                    "area": {
                        "id": "febe47f1-831b-472c-a068-339a65069dd3",
                        "name": "المعزيلة"
                    },
                    "value": 3888
                },
                {
                    "area": {
                        "id": "feb5834c-f023-44d4-8a14-35dc6629017d",
                        "name": "العمل"
                    },
                    "value": 3820
                },
                {
                    "area": {
                        "id": "51c12d2a-9ae8-4266-adc3-5126aa359cd3",
                        "name": "العود"
                    },
                    "value": 3800
                },
                {
                    "area": {
                        "id": "61ab70a4-3d37-47bd-a9ee-124bdc0fb670",
                        "name": "المنصورة"
                    },
                    "value": 3743
                },
                {
                    "area": {
                        "id": "ff86addf-942e-41dc-bb0f-9269251b42a3",
                        "name": "منفوحة"
                    },
                    "value": 3733
                },
                {
                    "area": {
                        "id": "9d09b05f-35f3-4925-84b1-978e9d701e5e",
                        "name": "أم الحمام الشرقي - المعذر"
                    },
                    "value": 3700
                },
                {
                    "area": {
                        "id": "2fa38d65-6151-493e-98aa-c14c06a28197",
                        "name": "الفاخرية"
                    },
                    "value": 3686
                },
                {
                    "area": {
                        "id": "751de8ea-eab5-45f3-801f-6a969a57b4e7",
                        "name": "الفاروق"
                    },
                    "value": 3683
                },
                {
                    "area": {
                        "id": "f8bed1dc-356d-43a9-b89b-9d1446a74683",
                        "name": "الحائر"
                    },
                    "value": 3671
                },
                {
                    "area": {
                        "id": "7566b077-f54c-444e-b41f-fb9ba8bbd8dd",
                        "name": "جامعة الملك سعود"
                    },
                    "value": 3665
                },
                {
                    "area": {
                        "id": "fcf3bfcc-4e81-4db1-8fe5-ef65fc610991",
                        "name": "البديعة"
                    },
                    "value": 3661
                },
                {
                    "area": {
                        "id": "a01d452c-3a36-4f1b-9ede-2eeb934405a8",
                        "name": "الرفيعة"
                    },
                    "value": 3643
                },
                {
                    "area": {
                        "id": "27783c9e-535f-4d44-9a5d-ed549644c5be",
                        "name": "سلطانة - العريجاء"
                    },
                    "value": 3595
                },
                {
                    "area": {
                        "id": "fd3f2823-fefa-4c52-aaa9-60150ebd0c37",
                        "name": "الديرة"
                    },
                    "value": 3500
                },
                {
                    "area": {
                        "id": "ea504b74-c266-4b09-b298-08e9dfb35eb5",
                        "name": "الـشـرفـيـة"
                    },
                    "value": 3457
                },
                {
                    "area": {
                        "id": "3c56b430-f38e-4714-81e3-8a502f8fb971",
                        "name": "السلي"
                    },
                    "value": 3333
                },
                {
                    "area": {
                        "id": "920c7560-2916-44ef-ac0e-f1baac271657",
                        "name": "ديراب"
                    },
                    "value": 3086
                },
                {
                    "area": {
                        "id": "ed69f3e8-523c-4ce7-a493-e92f4f9f1986",
                        "name": "أم الحمام الغربي"
                    },
                    "value": 3033
                },
                {
                    "area": {
                        "id": "8014f925-e0b7-4af1-9d9b-20c75afca882",
                        "name": "العليا - الملز والبطحاء"
                    },
                    "value": 2915
                },
                {
                    "area": {
                        "id": "dde02562-5497-4b68-bb19-baa4d9e93db5",
                        "name": "الخالدية"
                    },
                    "value": 2667
                },
                {
                    "area": {
                        "id": "9c5397a5-f624-4116-8db2-34ecf79e5315",
                        "name": "الفيصلية"
                    },
                    "value": 2620
                },
                {
                    "area": {
                        "id": "e85c3bb7-6f91-41de-8447-7a274dc46df3",
                        "name": "أم سليم"
                    },
                    "value": 2443
                },
                {
                    "area": {
                        "id": "3f6c38e8-6b3e-4775-8e1a-905b71f5858a",
                        "name": "الصالحية"
                    },
                    "value": 2400
                },
                {
                    "area": {
                        "id": "f659dd2c-ba77-464d-8a3d-70771ceda67c",
                        "name": "الصفاء"
                    },
                    "value": 2333
                },
                {
                    "area": {
                        "id": "67ebb7a3-cd3d-480c-ba20-20e8c55c8332",
                        "name": "الرحمانية"
                    },
                    "value": 2244
                },
                {
                    "area": {
                        "id": "6a6535f2-c3fc-408d-8de8-4d048dd19728",
                        "name": "اليمامة"
                    },
                    "value": 2200
                },
                {
                    "area": {
                        "id": "888e14d1-e0da-4731-a7d7-605372279f88",
                        "name": "الدوبية"
                    },
                    "value": 2167
                },
                {
                    "area": {
                        "id": "6720febf-8019-40cf-9446-5b2c8474d04d",
                        "name": "الرماية"
                    },
                    "value": 1200
                }
            ]
        },
        "saudi": {
            "facts": [
                {
                    "area": {
                        "id": "aa21340b-3580-4a62-8a43-3d12f6b00501",
                        "name": "السفارات"
                    },
                    "value": 34750
                },
                {
                    "area": {
                        "id": "47e60f73-b741-4d9e-87e4-a4e613d37cde",
                        "name": "الملك عبد العزيز"
                    },
                    "value": 29750
                },
                {
                    "area": {
                        "id": "fde48b0e-8c5f-4683-8cec-c29e7284ebf5",
                        "name": "المعذر"
                    },
                    "value": 25000
                },
                {
                    "area": {
                        "id": "3f6854d2-c64c-4718-98bb-00c9c1ff6cd3",
                        "name": "الغدير"
                    },
                    "value": 24250
                },
                {
                    "area": {
                        "id": "228ef43a-9e3e-48cb-bf5e-893d71a6554a",
                        "name": "الرائد"
                    },
                    "value": 24190
                },
                {
                    "area": {
                        "id": "7566b077-f54c-444e-b41f-fb9ba8bbd8dd",
                        "name": "جامعة الملك سعود"
                    },
                    "value": 22268
                },
                {
                    "area": {
                        "id": "843fce03-4fe4-4981-a161-b2284321d375",
                        "name": "النموذجية"
                    },
                    "value": 22224
                },
                {
                    "area": {
                        "id": "e59fe6ef-9353-440d-b502-dc8ff67b99fb",
                        "name": "عريض"
                    },
                    "value": 22000
                },
                {
                    "area": {
                        "id": "da870943-28b0-48ef-a7e4-3237b6a3908c",
                        "name": "المحمدية"
                    },
                    "value": 20332
                },
                {
                    "area": {
                        "id": "2ff065d6-764e-40b8-91fd-8210fad92c44",
                        "name": "الملك عبدالله"
                    },
                    "value": 19748
                },
                {
                    "area": {
                        "id": "0e8da9c4-e4a7-4794-a62d-9ab0554e7579",
                        "name": "أم الحمام الشرقي - الديرة"
                    },
                    "value": 19000
                },
                {
                    "area": {
                        "id": "a01d452c-3a36-4f1b-9ede-2eeb934405a8",
                        "name": "الرفيعة"
                    },
                    "value": 17896
                },
                {
                    "area": {
                        "id": "a29b89a8-30fd-4d75-9945-ecfec789c7cc",
                        "name": "المهدية"
                    },
                    "value": 17800
                },
                {
                    "area": {
                        "id": "e8c5f0cc-8565-4a1e-b40d-f1727489f6aa",
                        "name": "الخزامى"
                    },
                    "value": 17786
                },
                {
                    "area": {
                        "id": "c82315c6-3142-41f8-96ff-bc8329391522",
                        "name": "السليمانية - الملز والبطحاء"
                    },
                    "value": 17711
                },
                {
                    "area": {
                        "id": "5cf83942-e014-4a10-968d-408e1937b82e",
                        "name": "الورود"
                    },
                    "value": 17297
                },
                {
                    "area": {
                        "id": "c7750a62-e42d-42eb-9e83-aa44bf10a777",
                        "name": "النخيل"
                    },
                    "value": 17200
                },
                {
                    "area": {
                        "id": "c7f18c78-aae4-4895-a83c-57ce0c761cd1",
                        "name": "جرير"
                    },
                    "value": 17104
                },
                {
                    "area": {
                        "id": "a86339c7-1a18-4384-8800-76f1573c04a9",
                        "name": "الواحة"
                    },
                    "value": 16971
                },
                {
                    "area": {
                        "id": "2f57568c-1f9d-4659-9d1b-70e720b0a45c",
                        "name": "التعاون"
                    },
                    "value": 16923
                },
                {
                    "area": {
                        "id": "ea03b9a1-d5f3-469f-a9fb-cfb72df61d7f",
                        "name": "المعذر الشمالي"
                    },
                    "value": 16867
                },
                {
                    "area": {
                        "id": "66566263-1c8d-4e72-85e1-406464b90bbe",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 16800
                },
                {
                    "area": {
                        "id": "72b24564-20c8-4d3a-9d53-dd559786164d",
                        "name": "الفلاح"
                    },
                    "value": 16764
                },
                {
                    "area": {
                        "id": "cf8c586f-e220-4ca5-b3d2-c68a2c39df91",
                        "name": "الندي"
                    },
                    "value": 16685
                },
                {
                    "area": {
                        "id": "07310269-69f4-4e5a-a093-3b0686e6f92a",
                        "name": "الحمراء"
                    },
                    "value": 16459
                },
                {
                    "area": {
                        "id": "d8229af8-3a8a-421b-8e4f-74969f448e47",
                        "name": "الملقا"
                    },
                    "value": 16437
                },
                {
                    "area": {
                        "id": "900a8735-f91e-45b7-9702-c556cc4863bc",
                        "name": "الريان"
                    },
                    "value": 16026
                },
                {
                    "area": {
                        "id": "5e21ce61-1c87-4d44-bb79-62c105b36cc4",
                        "name": "المغرزات"
                    },
                    "value": 15443
                },
                {
                    "area": {
                        "id": "edd4c9b9-7053-48cf-983e-81c681aab6f8",
                        "name": "حطين"
                    },
                    "value": 15382
                },
                {
                    "area": {
                        "id": "aa3edb6a-2aaa-4f34-891b-32fd7a64014e",
                        "name": "الربيع"
                    },
                    "value": 15152
                },
                {
                    "area": {
                        "id": "206645fd-79d5-44fb-bcc7-4bdafd602a9b",
                        "name": "النفل"
                    },
                    "value": 15143
                },
                {
                    "area": {
                        "id": "0d7ff18e-c7e2-4607-a063-8b7c73b99838",
                        "name": "العليا - المعذر"
                    },
                    "value": 15139
                },
                {
                    "area": {
                        "id": "2c51be33-11eb-4645-a407-92d9acd33c9c",
                        "name": "عرقة"
                    },
                    "value": 15057
                },
                {
                    "area": {
                        "id": "b9945c44-61a0-4d1e-85f2-24eefe9611ae",
                        "name": "سلطانة - الديرة"
                    },
                    "value": 15000
                },
                {
                    "area": {
                        "id": "88251c8e-068a-4862-aff5-b6c2feb5e876",
                        "name": "الوشام"
                    },
                    "value": 14943
                },
                {
                    "area": {
                        "id": "d8f9c2f5-91d2-4806-be75-b4d5e229e084",
                        "name": "المرسلات"
                    },
                    "value": 14888
                },
                {
                    "area": {
                        "id": "d6d2d11e-2744-418e-904a-dc8ba194998e",
                        "name": "خشم العان"
                    },
                    "value": 14764
                },
                {
                    "area": {
                        "id": "009e646e-bb16-4a74-adda-4791c4cbc9c1",
                        "name": "السليمانية - العليا"
                    },
                    "value": 14737
                },
                {
                    "area": {
                        "id": "8dbab168-3b00-4a12-bc76-dc9d95373cac",
                        "name": "أشبيلية"
                    },
                    "value": 14669
                },
                {
                    "area": {
                        "id": "38434635-316c-4696-bf6e-0d350cf2e76a",
                        "name": "عليشة"
                    },
                    "value": 14339
                },
                {
                    "area": {
                        "id": "9d09b05f-35f3-4925-84b1-978e9d701e5e",
                        "name": "أم الحمام الشرقي - المعذر"
                    },
                    "value": 14335
                },
                {
                    "area": {
                        "id": "7bc70bab-8ac6-42d1-9d55-922d0df681d2",
                        "name": "الربوة"
                    },
                    "value": 14330
                },
                {
                    "area": {
                        "id": "f2724a71-ad73-4765-8462-f299eff48fec",
                        "name": "القدس"
                    },
                    "value": 14329
                },
                {
                    "area": {
                        "id": "ea504b74-c266-4b09-b298-08e9dfb35eb5",
                        "name": "الـشـرفـيـة"
                    },
                    "value": 14320
                },
                {
                    "area": {
                        "id": "cbb041b7-f87c-4878-821c-16ca4f34e10b",
                        "name": "الياسمين"
                    },
                    "value": 14185
                },
                {
                    "area": {
                        "id": "1f8ff56c-ade7-476d-9a18-ebf538ec1767",
                        "name": "الوادي"
                    },
                    "value": 13939
                },
                {
                    "area": {
                        "id": "13d2af17-de45-4e53-9dcc-17f1f18ba0a1",
                        "name": "المؤتمرات"
                    },
                    "value": 13900
                },
                {
                    "area": {
                        "id": "68b0afd0-e462-4930-936b-20532c79f1ad",
                        "name": "قرطبة"
                    },
                    "value": 13747
                },
                {
                    "area": {
                        "id": "ce4632d7-923a-409e-864a-b9c0e25775b6",
                        "name": "العارض"
                    },
                    "value": 13743
                },
                {
                    "area": {
                        "id": "d0759107-5d0c-4fb3-8ac2-745dbe717ed0",
                        "name": "المصيف"
                    },
                    "value": 13606
                },
                {
                    "area": {
                        "id": "c8f985cb-9b86-4d57-957f-b09b2ae78ab9",
                        "name": "المروج"
                    },
                    "value": 13546
                },
                {
                    "area": {
                        "id": "b1a6d8da-05c8-40fd-87e3-6b99a97079d2",
                        "name": "المنار"
                    },
                    "value": 13534
                },
                {
                    "area": {
                        "id": "1d18118a-09f4-46a3-a7fe-9f8a4aba9058",
                        "name": "غرناطة"
                    },
                    "value": 13506
                },
                {
                    "area": {
                        "id": "f96795fc-dd23-4de7-9d54-f9050c0f8e9d",
                        "name": "النرجس"
                    },
                    "value": 13463
                },
                {
                    "area": {
                        "id": "ca70401b-2dbf-4153-afcf-35969ce14bfd",
                        "name": "الصحافة"
                    },
                    "value": 13387
                },
                {
                    "area": {
                        "id": "d36380e7-28b8-4926-a30f-8fc9327abfb1",
                        "name": "النزهه"
                    },
                    "value": 13211
                },
                {
                    "area": {
                        "id": "67ebb7a3-cd3d-480c-ba20-20e8c55c8332",
                        "name": "الرحمانية"
                    },
                    "value": 13133
                },
                {
                    "area": {
                        "id": "52d2e2cd-fbb4-4830-84cc-58ae92d267a6",
                        "name": "الإزدهار"
                    },
                    "value": 12999
                },
                {
                    "area": {
                        "id": "ec66cc90-a1c0-4cb5-873d-7c4757b69971",
                        "name": "الأندلس"
                    },
                    "value": 12927
                },
                {
                    "area": {
                        "id": "4731263b-77e7-4938-adc7-a7c5f81b3900",
                        "name": "القيروان"
                    },
                    "value": 12900
                },
                {
                    "area": {
                        "id": "d096152a-b6d5-49c8-84b9-b9ca4a46fd2d",
                        "name": "العليا - العليا"
                    },
                    "value": 12780
                },
                {
                    "area": {
                        "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
                        "name": "صلاح الدين"
                    },
                    "value": 12753
                },
                {
                    "area": {
                        "id": "b91c2ee4-5fc7-4632-ac89-07e6fc008363",
                        "name": "الملز"
                    },
                    "value": 12735
                },
                {
                    "area": {
                        "id": "f659dd2c-ba77-464d-8a3d-70771ceda67c",
                        "name": "الصفاء"
                    },
                    "value": 12708
                },
                {
                    "area": {
                        "id": "48539b17-54d3-4f28-968c-025684a0ceab",
                        "name": "الملك فيصل"
                    },
                    "value": 12672
                },
                {
                    "area": {
                        "id": "33808d06-6a8a-42c1-86b2-79b4709905fd",
                        "name": "الناصرية"
                    },
                    "value": 12667
                },
                {
                    "area": {
                        "id": "62a893fc-9ec9-4e13-a01e-7191f976e312",
                        "name": "الروضة"
                    },
                    "value": 12578
                },
                {
                    "area": {
                        "id": "d85bc333-4975-421c-9d03-df228e6ae9ea",
                        "name": "الضباط"
                    },
                    "value": 12564
                },
                {
                    "area": {
                        "id": "86cdd3cf-82dd-461a-8764-5778344f1666",
                        "name": "الفيحاء"
                    },
                    "value": 12545
                },
                {
                    "area": {
                        "id": "ed69f3e8-523c-4ce7-a493-e92f4f9f1986",
                        "name": "أم الحمام الغربي"
                    },
                    "value": 12482
                },
                {
                    "area": {
                        "id": "c1b851a6-029c-42bc-97f5-bd72af99b3ed",
                        "name": "الروابي"
                    },
                    "value": 12415
                },
                {
                    "area": {
                        "id": "3b880a15-edb7-459d-817b-bbb4e5212ab9",
                        "name": "عكاظ"
                    },
                    "value": 12400
                },
                {
                    "area": {
                        "id": "8014f925-e0b7-4af1-9d9b-20c75afca882",
                        "name": "العليا - الملز والبطحاء"
                    },
                    "value": 12200
                },
                {
                    "area": {
                        "id": "c8fbfbfe-c1a0-4079-be04-ad20730038b0",
                        "name": "الوزارات"
                    },
                    "value": 12169
                },
                {
                    "area": {
                        "id": "cfa2d353-9107-4b34-bccf-533aac553ab4",
                        "name": "الزهراء"
                    },
                    "value": 12024
                },
                {
                    "area": {
                        "id": "7c07ad55-b15f-48f6-9aed-ebc1e67eff45",
                        "name": "الرمال"
                    },
                    "value": 11944
                },
                {
                    "area": {
                        "id": "a7e5ebed-efe6-4956-a53a-19f21c4a2cf9",
                        "name": "المونسية"
                    },
                    "value": 11793
                },
                {
                    "area": {
                        "id": "b4aed3f7-045a-443e-b340-81043580d7b9",
                        "name": "هجرة وادي لبن"
                    },
                    "value": 11607
                },
                {
                    "area": {
                        "id": "d3e1ad91-49ce-4b0c-bb5d-1fffecd8fafa",
                        "name": "اليرموك"
                    },
                    "value": 11543
                },
                {
                    "area": {
                        "id": "c0c6513b-13b9-45e1-848a-a4959f95971a",
                        "name": "الملك فهد"
                    },
                    "value": 11436
                },
                {
                    "area": {
                        "id": "c59c5455-500a-4d2b-a7b4-6802fb3f170c",
                        "name": "الرمال"
                    },
                    "value": 11416
                },
                {
                    "area": {
                        "id": "city-3",
                        "name": "الرياض"
                    },
                    "value": 11338
                },
                {
                    "area": {
                        "id": "d7a56eca-bec8-49e9-ab68-bfa73a314faa",
                        "name": "السلام"
                    },
                    "value": 11292
                },
                {
                    "area": {
                        "id": "6720febf-8019-40cf-9446-5b2c8474d04d",
                        "name": "الرماية"
                    },
                    "value": 11227
                },
                {
                    "area": {
                        "id": "2b62095b-102f-441f-ac00-34602cd48536",
                        "name": "الجزيرة"
                    },
                    "value": 11174
                },
                {
                    "area": {
                        "id": "5b05c230-55c9-499b-a012-887d53d66800",
                        "name": "المربع"
                    },
                    "value": 11122
                },
                {
                    "area": {
                        "id": "cd6e3719-5fb9-497a-91b9-e2668e2e75a6",
                        "name": "الهدا - الديرة"
                    },
                    "value": 11118
                },
                {
                    "area": {
                        "id": "e443160a-e66b-4369-a4bf-95f26060eccd",
                        "name": "الحزم"
                    },
                    "value": 11066
                },
                {
                    "area": {
                        "id": "aa140531-ded7-47f4-b7d5-591930d0316b",
                        "name": "النهضة"
                    },
                    "value": 11060
                },
                {
                    "area": {
                        "id": "61ab70a4-3d37-47bd-a9ee-124bdc0fb670",
                        "name": "المنصورة"
                    },
                    "value": 11055
                },
                {
                    "area": {
                        "id": "4ed2e10c-2b71-4414-a8f3-9b8a3f30e560",
                        "name": "العقيق"
                    },
                    "value": 10906
                },
                {
                    "area": {
                        "id": "98f7f0d1-438f-4c87-a98f-e0fda41b84bd",
                        "name": "ظهرة نمار"
                    },
                    "value": 10801
                },
                {
                    "area": {
                        "id": "8dba8acc-a41e-4473-8a52-10622bee365b",
                        "name": "الدريهمية"
                    },
                    "value": 10684
                },
                {
                    "area": {
                        "id": "30db56d8-31f6-4a21-81fa-f135163359b1",
                        "name": "الخليج"
                    },
                    "value": 10629
                },
                {
                    "area": {
                        "id": "b7aeff04-e705-4a9b-ae9f-0da2ac5b3d9e",
                        "name": "القادسية"
                    },
                    "value": 10562
                },
                {
                    "area": {
                        "id": "febe47f1-831b-472c-a068-339a65069dd3",
                        "name": "المعزيلة"
                    },
                    "value": 10504
                },
                {
                    "area": {
                        "id": "e9de74de-e178-4d06-856f-1689820e2c5a",
                        "name": "شبرا"
                    },
                    "value": 10301
                },
                {
                    "area": {
                        "id": "1bdf2e61-64d7-42c7-bd24-3b58fa806746",
                        "name": "جبرة"
                    },
                    "value": 10250
                },
                {
                    "area": {
                        "id": "6eea7b8d-e938-466a-ac3e-ae2b106ac59f",
                        "name": "النور"
                    },
                    "value": 10250
                },
                {
                    "area": {
                        "id": "aff3e994-cc0a-4e88-912d-0690a9983b27",
                        "name": "السويدي الغربي"
                    },
                    "value": 10217
                },
                {
                    "area": {
                        "id": "c35d1f60-d5ff-4885-91c6-85a519c80dcf",
                        "name": "الهدا - المعذر"
                    },
                    "value": 10000
                },
                {
                    "area": {
                        "id": "bf723f44-607f-4114-91b9-db8cd0c77a91",
                        "name": "الشفاء"
                    },
                    "value": 9966
                },
                {
                    "area": {
                        "id": "c37bc305-4ffc-4489-a6e3-9269b32edb1a",
                        "name": "الإسكان"
                    },
                    "value": 9875
                },
                {
                    "area": {
                        "id": "842383e2-3091-4283-b65c-f4a62cd18784",
                        "name": "ظهرة لبن"
                    },
                    "value": 9786
                },
                {
                    "area": {
                        "id": "7b5f813e-a731-40ef-b3a0-afac81467277",
                        "name": "نمار"
                    },
                    "value": 9691
                },
                {
                    "area": {
                        "id": "01c9ff6a-eb28-4465-a68c-c8a5562c6d39",
                        "name": "بدر"
                    },
                    "value": 9619
                },
                {
                    "area": {
                        "id": "dde02562-5497-4b68-bb19-baa4d9e93db5",
                        "name": "الخالدية"
                    },
                    "value": 9526
                },
                {
                    "area": {
                        "id": "39ac02a1-c044-4620-9169-b472154e3768",
                        "name": "ظهرة البديعة"
                    },
                    "value": 9480
                },
                {
                    "area": {
                        "id": "2be8f71f-bb94-4702-87d6-a258a14df452",
                        "name": "الزهرة"
                    },
                    "value": 9477
                },
                {
                    "area": {
                        "id": "751de8ea-eab5-45f3-801f-6a969a57b4e7",
                        "name": "الفاروق"
                    },
                    "value": 9467
                },
                {
                    "area": {
                        "id": "40772979-0127-4648-b641-dee43ee6b96b",
                        "name": "السويدي"
                    },
                    "value": 9356
                },
                {
                    "area": {
                        "id": "7a4897d9-89ac-4d95-a544-2aeee4f1beb2",
                        "name": "الصناعية"
                    },
                    "value": 9350
                },
                {
                    "area": {
                        "id": "c9fe42ca-2797-466e-b1d1-cb90c69a5605",
                        "name": "المروه"
                    },
                    "value": 9302
                },
                {
                    "area": {
                        "id": "27783c9e-535f-4d44-9a5d-ed549644c5be",
                        "name": "سلطانة - العريجاء"
                    },
                    "value": 9217
                },
                {
                    "area": {
                        "id": "43f724c9-8295-46e4-b80d-af74e659b872",
                        "name": "العريجاء الغربية"
                    },
                    "value": 9130
                },
                {
                    "area": {
                        "id": "471d8f88-5a0b-4890-8026-a63a835bf52a",
                        "name": "العوالي"
                    },
                    "value": 9068
                },
                {
                    "area": {
                        "id": "1297bd50-a138-4c61-9898-97d18963331a",
                        "name": "النسيم الشرقي"
                    },
                    "value": 9051
                },
                {
                    "area": {
                        "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                        "name": "السعادة"
                    },
                    "value": 9001
                },
                {
                    "area": {
                        "id": "e85c3bb7-6f91-41de-8447-7a274dc46df3",
                        "name": "أم سليم"
                    },
                    "value": 8983
                },
                {
                    "area": {
                        "id": "5b8e557e-aebe-4553-8402-8973b4ff0a79",
                        "name": "العزيزية"
                    },
                    "value": 8914
                },
                {
                    "area": {
                        "id": "fcf3bfcc-4e81-4db1-8fe5-ef65fc610991",
                        "name": "البديعة"
                    },
                    "value": 8860
                },
                {
                    "area": {
                        "id": "feb5834c-f023-44d4-8a14-35dc6629017d",
                        "name": "العمل"
                    },
                    "value": 8667
                },
                {
                    "area": {
                        "id": "1f314e74-fac1-4ebf-b83a-830ba70c09c3",
                        "name": "الدرعية"
                    },
                    "value": 8451
                },
                {
                    "area": {
                        "id": "0442bf29-e3f1-4dfa-8afd-b11e063b015a",
                        "name": "العريجاء الوسطى"
                    },
                    "value": 8427
                },
                {
                    "area": {
                        "id": "758da835-c682-46d6-82ad-0d9fb8442113",
                        "name": "العريجاء"
                    },
                    "value": 8409
                },
                {
                    "area": {
                        "id": "5dfaa455-f597-4c2b-961e-cd2faf15d08f",
                        "name": "النسيم الغربي"
                    },
                    "value": 8235
                },
                {
                    "area": {
                        "id": "2fa38d65-6151-493e-98aa-c14c06a28197",
                        "name": "الفاخرية"
                    },
                    "value": 8201
                },
                {
                    "area": {
                        "id": "7a9f08b6-502e-4300-87ac-3dc37a27e74c",
                        "name": "النظيم"
                    },
                    "value": 8146
                },
                {
                    "area": {
                        "id": "1460a408-4989-4c5e-9e97-494e36c3497a",
                        "name": "ضاحية نمار"
                    },
                    "value": 8125
                },
                {
                    "area": {
                        "id": "7e0fd377-cd04-4845-8b7f-7144752aea0d",
                        "name": "الدفاع"
                    },
                    "value": 8000
                },
                {
                    "area": {
                        "id": "b65ac3ce-46ab-419d-be64-7aa2761f4c28",
                        "name": "الجنادرية"
                    },
                    "value": 7996
                },
                {
                    "area": {
                        "id": "c1df54b0-feac-4290-9e75-8afd9e313efb",
                        "name": "طويق - عتيقة"
                    },
                    "value": 7979
                },
                {
                    "area": {
                        "id": "4f6a0751-1320-4e27-913b-2dfec0d8aa2f",
                        "name": "الدار البيضاء"
                    },
                    "value": 7833
                },
                {
                    "area": {
                        "id": "920c7560-2916-44ef-ac0e-f1baac271657",
                        "name": "ديراب"
                    },
                    "value": 7411
                },
                {
                    "area": {
                        "id": "3c56b430-f38e-4714-81e3-8a502f8fb971",
                        "name": "السلي"
                    },
                    "value": 7375
                },
                {
                    "area": {
                        "id": "1570d51a-3e9a-4b78-acb2-3d5389cd2a81",
                        "name": "منفوحة الجديدة"
                    },
                    "value": 7111
                },
                {
                    "area": {
                        "id": "f8bed1dc-356d-43a9-b89b-9d1446a74683",
                        "name": "الحائر"
                    },
                    "value": 6822
                },
                {
                    "area": {
                        "id": "14561646-f4ae-4c62-b7f1-8f95156cc0ef",
                        "name": "أحـد"
                    },
                    "value": 6586
                },
                {
                    "area": {
                        "id": "f0eb256e-8c6b-4943-9812-8a10c483b65d",
                        "name": "هيت"
                    },
                    "value": 6571
                },
                {
                    "area": {
                        "id": "05fe6a6f-34eb-45eb-82be-260adddd6082",
                        "name": "عتيقة"
                    },
                    "value": 6523
                },
                {
                    "area": {
                        "id": "0434eb81-4f04-4007-92cc-b0c5410bea7c",
                        "name": "الفوطة"
                    },
                    "value": 6333
                },
                {
                    "area": {
                        "id": "27c6e7ac-e6e9-49c9-abc9-c179249cf345",
                        "name": "المناخ"
                    },
                    "value": 6314
                },
                {
                    "area": {
                        "id": "6a6535f2-c3fc-408d-8de8-4d048dd19728",
                        "name": "اليمامة"
                    },
                    "value": 6036
                },
                {
                    "area": {
                        "id": "7dd2b8d2-e89d-408b-bc10-b735809ff749",
                        "name": "المرقب"
                    },
                    "value": 5873
                },
                {
                    "area": {
                        "id": "1a94924e-c8b8-47ae-b6f4-595f4acf8b3d",
                        "name": "غبيراء"
                    },
                    "value": 5814
                },
                {
                    "area": {
                        "id": "b2fbbbbc-f12f-44a5-8e76-a674c7a1a9e0",
                        "name": "معكال"
                    },
                    "value": 5750
                },
                {
                    "area": {
                        "id": "9c5397a5-f624-4116-8db2-34ecf79e5315",
                        "name": "الفيصلية"
                    },
                    "value": 5591
                },
                {
                    "area": {
                        "id": "19381f2a-1d68-4fc3-bc5a-09d5481cf03b",
                        "name": "الجرادية"
                    },
                    "value": 5455
                },
                {
                    "area": {
                        "id": "fd3f2823-fefa-4c52-aaa9-60150ebd0c37",
                        "name": "الديرة"
                    },
                    "value": 5405
                },
                {
                    "area": {
                        "id": "332ccd9e-8159-49fe-935d-bbb98730c2fc",
                        "name": "الشميسي"
                    },
                    "value": 5122
                },
                {
                    "area": {
                        "id": "ff86addf-942e-41dc-bb0f-9269251b42a3",
                        "name": "منفوحة"
                    },
                    "value": 4929
                },
                {
                    "area": {
                        "id": "51c12d2a-9ae8-4266-adc3-5126aa359cd3",
                        "name": "العود"
                    },
                    "value": 4797
                },
                {
                    "area": {
                        "id": "3f6c38e8-6b3e-4775-8e1a-905b71f5858a",
                        "name": "الصالحية"
                    },
                    "value": 4566
                },
                {
                    "area": {
                        "id": "aa913c8f-ae16-4ee9-a414-1318cda9c41a",
                        "name": "ثليم"
                    },
                    "value": 3978
                },
                {
                    "area": {
                        "id": "113113e3-21a3-4a3a-bfae-3dd799ded51c",
                        "name": "الوسيطا"
                    },
                    "value": 3167
                },
                {
                    "area": {
                        "id": "888e14d1-e0da-4731-a7d7-605372279f88",
                        "name": "الدوبية"
                    },
                    "value": 2000
                }
            ]
        },
        "nonSaudi": {
            "facts": [
                {
                    "area": {
                        "id": "aa21340b-3580-4a62-8a43-3d12f6b00501",
                        "name": "السفارات"
                    },
                    "value": 32389
                },
                {
                    "area": {
                        "id": "fde48b0e-8c5f-4683-8cec-c29e7284ebf5",
                        "name": "المعذر"
                    },
                    "value": 17286
                },
                {
                    "area": {
                        "id": "e59fe6ef-9353-440d-b502-dc8ff67b99fb",
                        "name": "عريض"
                    },
                    "value": 14000
                },
                {
                    "area": {
                        "id": "228ef43a-9e3e-48cb-bf5e-893d71a6554a",
                        "name": "الرائد"
                    },
                    "value": 12622
                },
                {
                    "area": {
                        "id": "47e60f73-b741-4d9e-87e4-a4e613d37cde",
                        "name": "الملك عبد العزيز"
                    },
                    "value": 11720
                },
                {
                    "area": {
                        "id": "5b05c230-55c9-499b-a012-887d53d66800",
                        "name": "المربع"
                    },
                    "value": 9816
                },
                {
                    "area": {
                        "id": "8dba8acc-a41e-4473-8a52-10622bee365b",
                        "name": "الدريهمية"
                    },
                    "value": 9232
                },
                {
                    "area": {
                        "id": "e8c5f0cc-8565-4a1e-b40d-f1727489f6aa",
                        "name": "الخزامى"
                    },
                    "value": 8000
                },
                {
                    "area": {
                        "id": "843fce03-4fe4-4981-a161-b2284321d375",
                        "name": "النموذجية"
                    },
                    "value": 7852
                },
                {
                    "area": {
                        "id": "2fa38d65-6151-493e-98aa-c14c06a28197",
                        "name": "الفاخرية"
                    },
                    "value": 7703
                },
                {
                    "area": {
                        "id": "d85bc333-4975-421c-9d03-df228e6ae9ea",
                        "name": "الضباط"
                    },
                    "value": 7696
                },
                {
                    "area": {
                        "id": "d096152a-b6d5-49c8-84b9-b9ca4a46fd2d",
                        "name": "العليا - العليا"
                    },
                    "value": 6876
                },
                {
                    "area": {
                        "id": "0434eb81-4f04-4007-92cc-b0c5410bea7c",
                        "name": "الفوطة"
                    },
                    "value": 6851
                },
                {
                    "area": {
                        "id": "009e646e-bb16-4a74-adda-4791c4cbc9c1",
                        "name": "السليمانية - العليا"
                    },
                    "value": 6815
                },
                {
                    "area": {
                        "id": "8014f925-e0b7-4af1-9d9b-20c75afca882",
                        "name": "العليا - الملز والبطحاء"
                    },
                    "value": 6296
                },
                {
                    "area": {
                        "id": "c8f985cb-9b86-4d57-957f-b09b2ae78ab9",
                        "name": "المروج"
                    },
                    "value": 6070
                },
                {
                    "area": {
                        "id": "cfa2d353-9107-4b34-bccf-533aac553ab4",
                        "name": "الزهراء"
                    },
                    "value": 6059
                },
                {
                    "area": {
                        "id": "f659dd2c-ba77-464d-8a3d-70771ceda67c",
                        "name": "الصفاء"
                    },
                    "value": 5910
                },
                {
                    "area": {
                        "id": "5cf83942-e014-4a10-968d-408e1937b82e",
                        "name": "الورود"
                    },
                    "value": 5698
                },
                {
                    "area": {
                        "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
                        "name": "صلاح الدين"
                    },
                    "value": 5679
                },
                {
                    "area": {
                        "id": "5ce6d443-f294-4559-9329-57509cc90cae",
                        "name": "البطيحا"
                    },
                    "value": 5465
                },
                {
                    "area": {
                        "id": "c7f18c78-aae4-4895-a83c-57ce0c761cd1",
                        "name": "جرير"
                    },
                    "value": 5191
                },
                {
                    "area": {
                        "id": "0d7ff18e-c7e2-4607-a063-8b7c73b99838",
                        "name": "العليا - المعذر"
                    },
                    "value": 5160
                },
                {
                    "area": {
                        "id": "38434635-316c-4696-bf6e-0d350cf2e76a",
                        "name": "عليشة"
                    },
                    "value": 5096
                },
                {
                    "area": {
                        "id": "c35d1f60-d5ff-4885-91c6-85a519c80dcf",
                        "name": "الهدا - المعذر"
                    },
                    "value": 5000
                },
                {
                    "area": {
                        "id": "ed69f3e8-523c-4ce7-a493-e92f4f9f1986",
                        "name": "أم الحمام الغربي"
                    },
                    "value": 4856
                },
                {
                    "area": {
                        "id": "1460a408-4989-4c5e-9e97-494e36c3497a",
                        "name": "ضاحية نمار"
                    },
                    "value": 4800
                },
                {
                    "area": {
                        "id": "b91c2ee4-5fc7-4632-ac89-07e6fc008363",
                        "name": "الملز"
                    },
                    "value": 4634
                },
                {
                    "area": {
                        "id": "c82315c6-3142-41f8-96ff-bc8329391522",
                        "name": "السليمانية - الملز والبطحاء"
                    },
                    "value": 4609
                },
                {
                    "area": {
                        "id": "8dbab168-3b00-4a12-bc76-dc9d95373cac",
                        "name": "أشبيلية"
                    },
                    "value": 4609
                },
                {
                    "area": {
                        "id": "d36380e7-28b8-4926-a30f-8fc9327abfb1",
                        "name": "النزهه"
                    },
                    "value": 4604
                },
                {
                    "area": {
                        "id": "cf8c586f-e220-4ca5-b3d2-c68a2c39df91",
                        "name": "الندي"
                    },
                    "value": 4591
                },
                {
                    "area": {
                        "id": "d8f9c2f5-91d2-4806-be75-b4d5e229e084",
                        "name": "المرسلات"
                    },
                    "value": 4500
                },
                {
                    "area": {
                        "id": "751de8ea-eab5-45f3-801f-6a969a57b4e7",
                        "name": "الفاروق"
                    },
                    "value": 4447
                },
                {
                    "area": {
                        "id": "1d18118a-09f4-46a3-a7fe-9f8a4aba9058",
                        "name": "غرناطة"
                    },
                    "value": 4428
                },
                {
                    "area": {
                        "id": "61ab70a4-3d37-47bd-a9ee-124bdc0fb670",
                        "name": "المنصورة"
                    },
                    "value": 4312
                },
                {
                    "area": {
                        "id": "88251c8e-068a-4862-aff5-b6c2feb5e876",
                        "name": "الوشام"
                    },
                    "value": 4300
                },
                {
                    "area": {
                        "id": "c0c6513b-13b9-45e1-848a-a4959f95971a",
                        "name": "الملك فهد"
                    },
                    "value": 4298
                },
                {
                    "area": {
                        "id": "d0759107-5d0c-4fb3-8ac2-745dbe717ed0",
                        "name": "المصيف"
                    },
                    "value": 4296
                },
                {
                    "area": {
                        "id": "039f1dd3-6866-4e6c-8f4f-53ba926d1f50",
                        "name": "القرى"
                    },
                    "value": 4000
                },
                {
                    "area": {
                        "id": "5b8e557e-aebe-4553-8402-8973b4ff0a79",
                        "name": "العزيزية"
                    },
                    "value": 3959
                },
                {
                    "area": {
                        "id": "9d09b05f-35f3-4925-84b1-978e9d701e5e",
                        "name": "أم الحمام الشرقي - المعذر"
                    },
                    "value": 3770
                },
                {
                    "area": {
                        "id": "a86339c7-1a18-4384-8800-76f1573c04a9",
                        "name": "الواحة"
                    },
                    "value": 3728
                },
                {
                    "area": {
                        "id": "4ed2e10c-2b71-4414-a8f3-9b8a3f30e560",
                        "name": "العقيق"
                    },
                    "value": 3675
                },
                {
                    "area": {
                        "id": "206645fd-79d5-44fb-bcc7-4bdafd602a9b",
                        "name": "النفل"
                    },
                    "value": 3674
                },
                {
                    "area": {
                        "id": "a7e5ebed-efe6-4956-a53a-19f21c4a2cf9",
                        "name": "المونسية"
                    },
                    "value": 3651
                },
                {
                    "area": {
                        "id": "c8fbfbfe-c1a0-4079-be04-ad20730038b0",
                        "name": "الوزارات"
                    },
                    "value": 3647
                },
                {
                    "area": {
                        "id": "feb5834c-f023-44d4-8a14-35dc6629017d",
                        "name": "العمل"
                    },
                    "value": 3593
                },
                {
                    "area": {
                        "id": "0442bf29-e3f1-4dfa-8afd-b11e063b015a",
                        "name": "العريجاء الوسطى"
                    },
                    "value": 3556
                },
                {
                    "area": {
                        "id": "52d2e2cd-fbb4-4830-84cc-58ae92d267a6",
                        "name": "الإزدهار"
                    },
                    "value": 3548
                },
                {
                    "area": {
                        "id": "7bc70bab-8ac6-42d1-9d55-922d0df681d2",
                        "name": "الربوة"
                    },
                    "value": 3541
                },
                {
                    "area": {
                        "id": "ec66cc90-a1c0-4cb5-873d-7c4757b69971",
                        "name": "الأندلس"
                    },
                    "value": 3485
                },
                {
                    "area": {
                        "id": "c37bc305-4ffc-4489-a6e3-9269b32edb1a",
                        "name": "الإسكان"
                    },
                    "value": 3484
                },
                {
                    "area": {
                        "id": "d7a56eca-bec8-49e9-ab68-bfa73a314faa",
                        "name": "السلام"
                    },
                    "value": 3466
                },
                {
                    "area": {
                        "id": "ca70401b-2dbf-4153-afcf-35969ce14bfd",
                        "name": "الصحافة"
                    },
                    "value": 3447
                },
                {
                    "area": {
                        "id": "0e8da9c4-e4a7-4794-a62d-9ab0554e7579",
                        "name": "أم الحمام الشرقي - الديرة"
                    },
                    "value": 3413
                },
                {
                    "area": {
                        "id": "c59c5455-500a-4d2b-a7b4-6802fb3f170c",
                        "name": "الرمال"
                    },
                    "value": 3410
                },
                {
                    "area": {
                        "id": "1a94924e-c8b8-47ae-b6f4-595f4acf8b3d",
                        "name": "غبيراء"
                    },
                    "value": 3403
                },
                {
                    "area": {
                        "id": "ea504b74-c266-4b09-b298-08e9dfb35eb5",
                        "name": "الـشـرفـيـة"
                    },
                    "value": 3349
                },
                {
                    "area": {
                        "id": "68b0afd0-e462-4930-936b-20532c79f1ad",
                        "name": "قرطبة"
                    },
                    "value": 3334
                },
                {
                    "area": {
                        "id": "2b62095b-102f-441f-ac00-34602cd48536",
                        "name": "الجزيرة"
                    },
                    "value": 3321
                },
                {
                    "area": {
                        "id": "city-3",
                        "name": "الرياض"
                    },
                    "value": 3293
                },
                {
                    "area": {
                        "id": "aa140531-ded7-47f4-b7d5-591930d0316b",
                        "name": "النهضة"
                    },
                    "value": 3271
                },
                {
                    "area": {
                        "id": "bf723f44-607f-4114-91b9-db8cd0c77a91",
                        "name": "الشفاء"
                    },
                    "value": 3262
                },
                {
                    "area": {
                        "id": "1297bd50-a138-4c61-9898-97d18963331a",
                        "name": "النسيم الشرقي"
                    },
                    "value": 3257
                },
                {
                    "area": {
                        "id": "d3e1ad91-49ce-4b0c-bb5d-1fffecd8fafa",
                        "name": "اليرموك"
                    },
                    "value": 3239
                },
                {
                    "area": {
                        "id": "f2724a71-ad73-4765-8462-f299eff48fec",
                        "name": "القدس"
                    },
                    "value": 3172
                },
                {
                    "area": {
                        "id": "408b741e-1704-4e36-be99-3c9201ef4b51",
                        "name": "صياح"
                    },
                    "value": 3153
                },
                {
                    "area": {
                        "id": "5dfaa455-f597-4c2b-961e-cd2faf15d08f",
                        "name": "النسيم الغربي"
                    },
                    "value": 3109
                },
                {
                    "area": {
                        "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                        "name": "السعادة"
                    },
                    "value": 3102
                },
                {
                    "area": {
                        "id": "4f6a0751-1320-4e27-913b-2dfec0d8aa2f",
                        "name": "الدار البيضاء"
                    },
                    "value": 3095
                },
                {
                    "area": {
                        "id": "471d8f88-5a0b-4890-8026-a63a835bf52a",
                        "name": "العوالي"
                    },
                    "value": 3091
                },
                {
                    "area": {
                        "id": "c1b851a6-029c-42bc-97f5-bd72af99b3ed",
                        "name": "الروابي"
                    },
                    "value": 3048
                },
                {
                    "area": {
                        "id": "2f57568c-1f9d-4659-9d1b-70e720b0a45c",
                        "name": "التعاون"
                    },
                    "value": 3038
                },
                {
                    "area": {
                        "id": "dde02562-5497-4b68-bb19-baa4d9e93db5",
                        "name": "الخالدية"
                    },
                    "value": 3031
                },
                {
                    "area": {
                        "id": "33808d06-6a8a-42c1-86b2-79b4709905fd",
                        "name": "الناصرية"
                    },
                    "value": 3026
                },
                {
                    "area": {
                        "id": "842383e2-3091-4283-b65c-f4a62cd18784",
                        "name": "ظهرة لبن"
                    },
                    "value": 3026
                },
                {
                    "area": {
                        "id": "3b880a15-edb7-459d-817b-bbb4e5212ab9",
                        "name": "عكاظ"
                    },
                    "value": 2967
                },
                {
                    "area": {
                        "id": "b4aed3f7-045a-443e-b340-81043580d7b9",
                        "name": "هجرة وادي لبن"
                    },
                    "value": 2935
                },
                {
                    "area": {
                        "id": "27783c9e-535f-4d44-9a5d-ed549644c5be",
                        "name": "سلطانة - العريجاء"
                    },
                    "value": 2931
                },
                {
                    "area": {
                        "id": "a01d452c-3a36-4f1b-9ede-2eeb934405a8",
                        "name": "الرفيعة"
                    },
                    "value": 2928
                },
                {
                    "area": {
                        "id": "1bdf2e61-64d7-42c7-bd24-3b58fa806746",
                        "name": "جبرة"
                    },
                    "value": 2853
                },
                {
                    "area": {
                        "id": "62a893fc-9ec9-4e13-a01e-7191f976e312",
                        "name": "الروضة"
                    },
                    "value": 2846
                },
                {
                    "area": {
                        "id": "7a9f08b6-502e-4300-87ac-3dc37a27e74c",
                        "name": "النظيم"
                    },
                    "value": 2846
                },
                {
                    "area": {
                        "id": "2c51be33-11eb-4645-a407-92d9acd33c9c",
                        "name": "عرقة"
                    },
                    "value": 2843
                },
                {
                    "area": {
                        "id": "86cdd3cf-82dd-461a-8764-5778344f1666",
                        "name": "الفيحاء"
                    },
                    "value": 2819
                },
                {
                    "area": {
                        "id": "07310269-69f4-4e5a-a093-3b0686e6f92a",
                        "name": "الحمراء"
                    },
                    "value": 2817
                },
                {
                    "area": {
                        "id": "7c07ad55-b15f-48f6-9aed-ebc1e67eff45",
                        "name": "الرمال"
                    },
                    "value": 2750
                },
                {
                    "area": {
                        "id": "fd3f2823-fefa-4c52-aaa9-60150ebd0c37",
                        "name": "الديرة"
                    },
                    "value": 2692
                },
                {
                    "area": {
                        "id": "40772979-0127-4648-b641-dee43ee6b96b",
                        "name": "السويدي"
                    },
                    "value": 2681
                },
                {
                    "area": {
                        "id": "e9de74de-e178-4d06-856f-1689820e2c5a",
                        "name": "شبرا"
                    },
                    "value": 2680
                },
                {
                    "area": {
                        "id": "6a6535f2-c3fc-408d-8de8-4d048dd19728",
                        "name": "اليمامة"
                    },
                    "value": 2672
                },
                {
                    "area": {
                        "id": "113113e3-21a3-4a3a-bfae-3dd799ded51c",
                        "name": "الوسيطا"
                    },
                    "value": 2657
                },
                {
                    "area": {
                        "id": "9c5397a5-f624-4116-8db2-34ecf79e5315",
                        "name": "الفيصلية"
                    },
                    "value": 2623
                },
                {
                    "area": {
                        "id": "fcf3bfcc-4e81-4db1-8fe5-ef65fc610991",
                        "name": "البديعة"
                    },
                    "value": 2572
                },
                {
                    "area": {
                        "id": "d8229af8-3a8a-421b-8e4f-74969f448e47",
                        "name": "الملقا"
                    },
                    "value": 2555
                },
                {
                    "area": {
                        "id": "b1a6d8da-05c8-40fd-87e3-6b99a97079d2",
                        "name": "المنار"
                    },
                    "value": 2545
                },
                {
                    "area": {
                        "id": "b65ac3ce-46ab-419d-be64-7aa2761f4c28",
                        "name": "الجنادرية"
                    },
                    "value": 2518
                },
                {
                    "area": {
                        "id": "1570d51a-3e9a-4b78-acb2-3d5389cd2a81",
                        "name": "منفوحة الجديدة"
                    },
                    "value": 2513
                },
                {
                    "area": {
                        "id": "05fe6a6f-34eb-45eb-82be-260adddd6082",
                        "name": "عتيقة"
                    },
                    "value": 2497
                },
                {
                    "area": {
                        "id": "7dd2b8d2-e89d-408b-bc10-b735809ff749",
                        "name": "المرقب"
                    },
                    "value": 2480
                },
                {
                    "area": {
                        "id": "2ff065d6-764e-40b8-91fd-8210fad92c44",
                        "name": "الملك عبدالله"
                    },
                    "value": 2464
                },
                {
                    "area": {
                        "id": "aa913c8f-ae16-4ee9-a414-1318cda9c41a",
                        "name": "ثليم"
                    },
                    "value": 2462
                },
                {
                    "area": {
                        "id": "c7750a62-e42d-42eb-9e83-aa44bf10a777",
                        "name": "النخيل"
                    },
                    "value": 2441
                },
                {
                    "area": {
                        "id": "332ccd9e-8159-49fe-935d-bbb98730c2fc",
                        "name": "الشميسي"
                    },
                    "value": 2422
                },
                {
                    "area": {
                        "id": "51c12d2a-9ae8-4266-adc3-5126aa359cd3",
                        "name": "العود"
                    },
                    "value": 2414
                },
                {
                    "area": {
                        "id": "f0eb256e-8c6b-4943-9812-8a10c483b65d",
                        "name": "هيت"
                    },
                    "value": 2410
                },
                {
                    "area": {
                        "id": "b9945c44-61a0-4d1e-85f2-24eefe9611ae",
                        "name": "سلطانة - الديرة"
                    },
                    "value": 2406
                },
                {
                    "area": {
                        "id": "5e21ce61-1c87-4d44-bb79-62c105b36cc4",
                        "name": "المغرزات"
                    },
                    "value": 2400
                },
                {
                    "area": {
                        "id": "4731263b-77e7-4938-adc7-a7c5f81b3900",
                        "name": "القيروان"
                    },
                    "value": 2376
                },
                {
                    "area": {
                        "id": "e85c3bb7-6f91-41de-8447-7a274dc46df3",
                        "name": "أم سليم"
                    },
                    "value": 2349
                },
                {
                    "area": {
                        "id": "19381f2a-1d68-4fc3-bc5a-09d5481cf03b",
                        "name": "الجرادية"
                    },
                    "value": 2325
                },
                {
                    "area": {
                        "id": "6eea7b8d-e938-466a-ac3e-ae2b106ac59f",
                        "name": "النور"
                    },
                    "value": 2300
                },
                {
                    "area": {
                        "id": "43f724c9-8295-46e4-b80d-af74e659b872",
                        "name": "العريجاء الغربية"
                    },
                    "value": 2294
                },
                {
                    "area": {
                        "id": "ea03b9a1-d5f3-469f-a9fb-cfb72df61d7f",
                        "name": "المعذر الشمالي"
                    },
                    "value": 2287
                },
                {
                    "area": {
                        "id": "1f8ff56c-ade7-476d-9a18-ebf538ec1767",
                        "name": "الوادي"
                    },
                    "value": 2282
                },
                {
                    "area": {
                        "id": "39ac02a1-c044-4620-9169-b472154e3768",
                        "name": "ظهرة البديعة"
                    },
                    "value": 2273
                },
                {
                    "area": {
                        "id": "30db56d8-31f6-4a21-81fa-f135163359b1",
                        "name": "الخليج"
                    },
                    "value": 2272
                },
                {
                    "area": {
                        "id": "1f314e74-fac1-4ebf-b83a-830ba70c09c3",
                        "name": "الدرعية"
                    },
                    "value": 2268
                },
                {
                    "area": {
                        "id": "01c9ff6a-eb28-4465-a68c-c8a5562c6d39",
                        "name": "بدر"
                    },
                    "value": 2197
                },
                {
                    "area": {
                        "id": "ff86addf-942e-41dc-bb0f-9269251b42a3",
                        "name": "منفوحة"
                    },
                    "value": 2188
                },
                {
                    "area": {
                        "id": "3f6c38e8-6b3e-4775-8e1a-905b71f5858a",
                        "name": "الصالحية"
                    },
                    "value": 2186
                },
                {
                    "area": {
                        "id": "920c7560-2916-44ef-ac0e-f1baac271657",
                        "name": "ديراب"
                    },
                    "value": 2173
                },
                {
                    "area": {
                        "id": "b2fbbbbc-f12f-44a5-8e76-a674c7a1a9e0",
                        "name": "معكال"
                    },
                    "value": 2151
                },
                {
                    "area": {
                        "id": "7a4897d9-89ac-4d95-a544-2aeee4f1beb2",
                        "name": "الصناعية"
                    },
                    "value": 2138
                },
                {
                    "area": {
                        "id": "758da835-c682-46d6-82ad-0d9fb8442113",
                        "name": "العريجاء"
                    },
                    "value": 2137
                },
                {
                    "area": {
                        "id": "bc3d0470-797d-4659-9d54-2d5048e158f3",
                        "name": "المصانع"
                    },
                    "value": 2073
                },
                {
                    "area": {
                        "id": "febe47f1-831b-472c-a068-339a65069dd3",
                        "name": "المعزيلة"
                    },
                    "value": 2065
                },
                {
                    "area": {
                        "id": "72b24564-20c8-4d3a-9d53-dd559786164d",
                        "name": "الفلاح"
                    },
                    "value": 2052
                },
                {
                    "area": {
                        "id": "f8bed1dc-356d-43a9-b89b-9d1446a74683",
                        "name": "الحائر"
                    },
                    "value": 2023
                },
                {
                    "area": {
                        "id": "900a8735-f91e-45b7-9702-c556cc4863bc",
                        "name": "الريان"
                    },
                    "value": 2013
                },
                {
                    "area": {
                        "id": "2911ee84-265f-44d7-8105-4c5ea9e1c72b",
                        "name": "طيبة"
                    },
                    "value": 2000
                },
                {
                    "area": {
                        "id": "a29b89a8-30fd-4d75-9945-ecfec789c7cc",
                        "name": "المهدية"
                    },
                    "value": 2000
                },
                {
                    "area": {
                        "id": "2be8f71f-bb94-4702-87d6-a258a14df452",
                        "name": "الزهرة"
                    },
                    "value": 1999
                },
                {
                    "area": {
                        "id": "27c6e7ac-e6e9-49c9-abc9-c179249cf345",
                        "name": "المناخ"
                    },
                    "value": 1984
                },
                {
                    "area": {
                        "id": "888e14d1-e0da-4731-a7d7-605372279f88",
                        "name": "الدوبية"
                    },
                    "value": 1966
                },
                {
                    "area": {
                        "id": "baa1d3f2-7268-4abf-b839-02bd717dfeca",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 1955
                },
                {
                    "area": {
                        "id": "cbb041b7-f87c-4878-821c-16ca4f34e10b",
                        "name": "الياسمين"
                    },
                    "value": 1953
                },
                {
                    "area": {
                        "id": "48539b17-54d3-4f28-968c-025684a0ceab",
                        "name": "الملك فيصل"
                    },
                    "value": 1938
                },
                {
                    "area": {
                        "id": "1476a71c-9823-4053-9439-cb7b7ce6a7fa",
                        "name": "سلام"
                    },
                    "value": 1932
                },
                {
                    "area": {
                        "id": "aff3e994-cc0a-4e88-912d-0690a9983b27",
                        "name": "السويدي الغربي"
                    },
                    "value": 1912
                },
                {
                    "area": {
                        "id": "b7aeff04-e705-4a9b-ae9f-0da2ac5b3d9e",
                        "name": "القادسية"
                    },
                    "value": 1911
                },
                {
                    "area": {
                        "id": "7b5f813e-a731-40ef-b3a0-afac81467277",
                        "name": "نمار"
                    },
                    "value": 1894
                },
                {
                    "area": {
                        "id": "c1df54b0-feac-4290-9e75-8afd9e313efb",
                        "name": "طويق - عتيقة"
                    },
                    "value": 1893
                },
                {
                    "area": {
                        "id": "e443160a-e66b-4369-a4bf-95f26060eccd",
                        "name": "الحزم"
                    },
                    "value": 1878
                },
                {
                    "area": {
                        "id": "aa3edb6a-2aaa-4f34-891b-32fd7a64014e",
                        "name": "الربيع"
                    },
                    "value": 1876
                },
                {
                    "area": {
                        "id": "67ebb7a3-cd3d-480c-ba20-20e8c55c8332",
                        "name": "الرحمانية"
                    },
                    "value": 1863
                },
                {
                    "area": {
                        "id": "3c56b430-f38e-4714-81e3-8a502f8fb971",
                        "name": "السلي"
                    },
                    "value": 1862
                },
                {
                    "area": {
                        "id": "14561646-f4ae-4c62-b7f1-8f95156cc0ef",
                        "name": "أحـد"
                    },
                    "value": 1817
                },
                {
                    "area": {
                        "id": "13d2af17-de45-4e53-9dcc-17f1f18ba0a1",
                        "name": "المؤتمرات"
                    },
                    "value": 1800
                },
                {
                    "area": {
                        "id": "c9fe42ca-2797-466e-b1d1-cb90c69a5605",
                        "name": "المروه"
                    },
                    "value": 1781
                },
                {
                    "area": {
                        "id": "66566263-1c8d-4e72-85e1-406464b90bbe",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 1762
                },
                {
                    "area": {
                        "id": "edd4c9b9-7053-48cf-983e-81c681aab6f8",
                        "name": "حطين"
                    },
                    "value": 1755
                },
                {
                    "area": {
                        "id": "076e4790-fa1c-4add-9531-491da2447079",
                        "name": "المصفاة"
                    },
                    "value": 1580
                },
                {
                    "area": {
                        "id": "3f6854d2-c64c-4718-98bb-00c9c1ff6cd3",
                        "name": "الغدير"
                    },
                    "value": 1549
                },
                {
                    "area": {
                        "id": "da870943-28b0-48ef-a7e4-3237b6a3908c",
                        "name": "المحمدية"
                    },
                    "value": 1500
                },
                {
                    "area": {
                        "id": "977a2aab-df59-47b7-86c6-0e653c3c4cfd",
                        "name": "المنصورية"
                    },
                    "value": 1500
                },
                {
                    "area": {
                        "id": "7566b077-f54c-444e-b41f-fb9ba8bbd8dd",
                        "name": "جامعة الملك سعود"
                    },
                    "value": 1493
                },
                {
                    "area": {
                        "id": "f96795fc-dd23-4de7-9d54-f9050c0f8e9d",
                        "name": "النرجس"
                    },
                    "value": 1490
                },
                {
                    "area": {
                        "id": "7e0fd377-cd04-4845-8b7f-7144752aea0d",
                        "name": "الدفاع"
                    },
                    "value": 1471
                },
                {
                    "area": {
                        "id": "cd6e3719-5fb9-497a-91b9-e2668e2e75a6",
                        "name": "الهدا - الديرة"
                    },
                    "value": 1463
                },
                {
                    "area": {
                        "id": "ce4632d7-923a-409e-864a-b9c0e25775b6",
                        "name": "العارض"
                    },
                    "value": 1459
                },
                {
                    "area": {
                        "id": "98f7f0d1-438f-4c87-a98f-e0fda41b84bd",
                        "name": "ظهرة نمار"
                    },
                    "value": 1381
                },
                {
                    "area": {
                        "id": "d6d2d11e-2744-418e-904a-dc8ba194998e",
                        "name": "خشم العان"
                    },
                    "value": 1341
                },
                {
                    "area": {
                        "id": "6720febf-8019-40cf-9446-5b2c8474d04d",
                        "name": "الرماية"
                    },
                    "value": 1200
                }
            ]
        },
        "saudiMale": {
            "facts": [
                {
                    "area": {
                        "id": "47e60f73-b741-4d9e-87e4-a4e613d37cde",
                        "name": "الملك عبد العزيز"
                    },
                    "value": 44000
                },
                {
                    "area": {
                        "id": "aa21340b-3580-4a62-8a43-3d12f6b00501",
                        "name": "السفارات"
                    },
                    "value": 37545
                },
                {
                    "area": {
                        "id": "228ef43a-9e3e-48cb-bf5e-893d71a6554a",
                        "name": "الرائد"
                    },
                    "value": 25263
                },
                {
                    "area": {
                        "id": "843fce03-4fe4-4981-a161-b2284321d375",
                        "name": "النموذجية"
                    },
                    "value": 25218
                },
                {
                    "area": {
                        "id": "2ff065d6-764e-40b8-91fd-8210fad92c44",
                        "name": "الملك عبدالله"
                    },
                    "value": 25176
                },
                {
                    "area": {
                        "id": "fde48b0e-8c5f-4683-8cec-c29e7284ebf5",
                        "name": "المعذر"
                    },
                    "value": 25000
                },
                {
                    "area": {
                        "id": "7566b077-f54c-444e-b41f-fb9ba8bbd8dd",
                        "name": "جامعة الملك سعود"
                    },
                    "value": 24833
                },
                {
                    "area": {
                        "id": "3f6854d2-c64c-4718-98bb-00c9c1ff6cd3",
                        "name": "الغدير"
                    },
                    "value": 24776
                },
                {
                    "area": {
                        "id": "0e8da9c4-e4a7-4794-a62d-9ab0554e7579",
                        "name": "أم الحمام الشرقي - الديرة"
                    },
                    "value": 24200
                },
                {
                    "area": {
                        "id": "e59fe6ef-9353-440d-b502-dc8ff67b99fb",
                        "name": "عريض"
                    },
                    "value": 22000
                },
                {
                    "area": {
                        "id": "da870943-28b0-48ef-a7e4-3237b6a3908c",
                        "name": "المحمدية"
                    },
                    "value": 21338
                },
                {
                    "area": {
                        "id": "88251c8e-068a-4862-aff5-b6c2feb5e876",
                        "name": "الوشام"
                    },
                    "value": 21000
                },
                {
                    "area": {
                        "id": "5cf83942-e014-4a10-968d-408e1937b82e",
                        "name": "الورود"
                    },
                    "value": 19541
                },
                {
                    "area": {
                        "id": "c7750a62-e42d-42eb-9e83-aa44bf10a777",
                        "name": "النخيل"
                    },
                    "value": 19468
                },
                {
                    "area": {
                        "id": "cf8c586f-e220-4ca5-b3d2-c68a2c39df91",
                        "name": "الندي"
                    },
                    "value": 19278
                },
                {
                    "area": {
                        "id": "72b24564-20c8-4d3a-9d53-dd559786164d",
                        "name": "الفلاح"
                    },
                    "value": 19244
                },
                {
                    "area": {
                        "id": "c82315c6-3142-41f8-96ff-bc8329391522",
                        "name": "السليمانية - الملز والبطحاء"
                    },
                    "value": 19132
                },
                {
                    "area": {
                        "id": "a86339c7-1a18-4384-8800-76f1573c04a9",
                        "name": "الواحة"
                    },
                    "value": 19110
                },
                {
                    "area": {
                        "id": "07310269-69f4-4e5a-a093-3b0686e6f92a",
                        "name": "الحمراء"
                    },
                    "value": 18991
                },
                {
                    "area": {
                        "id": "a01d452c-3a36-4f1b-9ede-2eeb934405a8",
                        "name": "الرفيعة"
                    },
                    "value": 18875
                },
                {
                    "area": {
                        "id": "e8c5f0cc-8565-4a1e-b40d-f1727489f6aa",
                        "name": "الخزامى"
                    },
                    "value": 18647
                },
                {
                    "area": {
                        "id": "2f57568c-1f9d-4659-9d1b-70e720b0a45c",
                        "name": "التعاون"
                    },
                    "value": 18394
                },
                {
                    "area": {
                        "id": "a29b89a8-30fd-4d75-9945-ecfec789c7cc",
                        "name": "المهدية"
                    },
                    "value": 17800
                },
                {
                    "area": {
                        "id": "d8229af8-3a8a-421b-8e4f-74969f448e47",
                        "name": "الملقا"
                    },
                    "value": 17711
                },
                {
                    "area": {
                        "id": "900a8735-f91e-45b7-9702-c556cc4863bc",
                        "name": "الريان"
                    },
                    "value": 17306
                },
                {
                    "area": {
                        "id": "66566263-1c8d-4e72-85e1-406464b90bbe",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 17250
                },
                {
                    "area": {
                        "id": "5e21ce61-1c87-4d44-bb79-62c105b36cc4",
                        "name": "المغرزات"
                    },
                    "value": 16938
                },
                {
                    "area": {
                        "id": "c7f18c78-aae4-4895-a83c-57ce0c761cd1",
                        "name": "جرير"
                    },
                    "value": 16699
                },
                {
                    "area": {
                        "id": "ea03b9a1-d5f3-469f-a9fb-cfb72df61d7f",
                        "name": "المعذر الشمالي"
                    },
                    "value": 16698
                },
                {
                    "area": {
                        "id": "aa3edb6a-2aaa-4f34-891b-32fd7a64014e",
                        "name": "الربيع"
                    },
                    "value": 16644
                },
                {
                    "area": {
                        "id": "edd4c9b9-7053-48cf-983e-81c681aab6f8",
                        "name": "حطين"
                    },
                    "value": 16561
                },
                {
                    "area": {
                        "id": "d8f9c2f5-91d2-4806-be75-b4d5e229e084",
                        "name": "المرسلات"
                    },
                    "value": 16518
                },
                {
                    "area": {
                        "id": "0d7ff18e-c7e2-4607-a063-8b7c73b99838",
                        "name": "العليا - المعذر"
                    },
                    "value": 16253
                },
                {
                    "area": {
                        "id": "009e646e-bb16-4a74-adda-4791c4cbc9c1",
                        "name": "السليمانية - العليا"
                    },
                    "value": 16248
                },
                {
                    "area": {
                        "id": "206645fd-79d5-44fb-bcc7-4bdafd602a9b",
                        "name": "النفل"
                    },
                    "value": 16003
                },
                {
                    "area": {
                        "id": "2c51be33-11eb-4645-a407-92d9acd33c9c",
                        "name": "عرقة"
                    },
                    "value": 15872
                },
                {
                    "area": {
                        "id": "cbb041b7-f87c-4878-821c-16ca4f34e10b",
                        "name": "الياسمين"
                    },
                    "value": 15764
                },
                {
                    "area": {
                        "id": "8dbab168-3b00-4a12-bc76-dc9d95373cac",
                        "name": "أشبيلية"
                    },
                    "value": 15626
                },
                {
                    "area": {
                        "id": "f2724a71-ad73-4765-8462-f299eff48fec",
                        "name": "القدس"
                    },
                    "value": 15511
                },
                {
                    "area": {
                        "id": "7bc70bab-8ac6-42d1-9d55-922d0df681d2",
                        "name": "الربوة"
                    },
                    "value": 15477
                },
                {
                    "area": {
                        "id": "d6d2d11e-2744-418e-904a-dc8ba194998e",
                        "name": "خشم العان"
                    },
                    "value": 15323
                },
                {
                    "area": {
                        "id": "1f8ff56c-ade7-476d-9a18-ebf538ec1767",
                        "name": "الوادي"
                    },
                    "value": 15293
                },
                {
                    "area": {
                        "id": "38434635-316c-4696-bf6e-0d350cf2e76a",
                        "name": "عليشة"
                    },
                    "value": 15289
                },
                {
                    "area": {
                        "id": "ce4632d7-923a-409e-864a-b9c0e25775b6",
                        "name": "العارض"
                    },
                    "value": 15053
                },
                {
                    "area": {
                        "id": "b9945c44-61a0-4d1e-85f2-24eefe9611ae",
                        "name": "سلطانة - الديرة"
                    },
                    "value": 15000
                },
                {
                    "area": {
                        "id": "68b0afd0-e462-4930-936b-20532c79f1ad",
                        "name": "قرطبة"
                    },
                    "value": 14869
                },
                {
                    "area": {
                        "id": "9d09b05f-35f3-4925-84b1-978e9d701e5e",
                        "name": "أم الحمام الشرقي - المعذر"
                    },
                    "value": 14844
                },
                {
                    "area": {
                        "id": "d36380e7-28b8-4926-a30f-8fc9327abfb1",
                        "name": "النزهه"
                    },
                    "value": 14583
                },
                {
                    "area": {
                        "id": "d0759107-5d0c-4fb3-8ac2-745dbe717ed0",
                        "name": "المصيف"
                    },
                    "value": 14572
                },
                {
                    "area": {
                        "id": "ec66cc90-a1c0-4cb5-873d-7c4757b69971",
                        "name": "الأندلس"
                    },
                    "value": 14352
                },
                {
                    "area": {
                        "id": "1d18118a-09f4-46a3-a7fe-9f8a4aba9058",
                        "name": "غرناطة"
                    },
                    "value": 14334
                },
                {
                    "area": {
                        "id": "ea504b74-c266-4b09-b298-08e9dfb35eb5",
                        "name": "الـشـرفـيـة"
                    },
                    "value": 14292
                },
                {
                    "area": {
                        "id": "ca70401b-2dbf-4153-afcf-35969ce14bfd",
                        "name": "الصحافة"
                    },
                    "value": 14261
                },
                {
                    "area": {
                        "id": "c8f985cb-9b86-4d57-957f-b09b2ae78ab9",
                        "name": "المروج"
                    },
                    "value": 14200
                },
                {
                    "area": {
                        "id": "13d2af17-de45-4e53-9dcc-17f1f18ba0a1",
                        "name": "المؤتمرات"
                    },
                    "value": 14143
                },
                {
                    "area": {
                        "id": "f96795fc-dd23-4de7-9d54-f9050c0f8e9d",
                        "name": "النرجس"
                    },
                    "value": 13957
                },
                {
                    "area": {
                        "id": "8014f925-e0b7-4af1-9d9b-20c75afca882",
                        "name": "العليا - الملز والبطحاء"
                    },
                    "value": 13795
                },
                {
                    "area": {
                        "id": "b1a6d8da-05c8-40fd-87e3-6b99a97079d2",
                        "name": "المنار"
                    },
                    "value": 13706
                },
                {
                    "area": {
                        "id": "d85bc333-4975-421c-9d03-df228e6ae9ea",
                        "name": "الضباط"
                    },
                    "value": 13467
                },
                {
                    "area": {
                        "id": "62a893fc-9ec9-4e13-a01e-7191f976e312",
                        "name": "الروضة"
                    },
                    "value": 13446
                },
                {
                    "area": {
                        "id": "52d2e2cd-fbb4-4830-84cc-58ae92d267a6",
                        "name": "الإزدهار"
                    },
                    "value": 13442
                },
                {
                    "area": {
                        "id": "f659dd2c-ba77-464d-8a3d-70771ceda67c",
                        "name": "الصفاء"
                    },
                    "value": 13409
                },
                {
                    "area": {
                        "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
                        "name": "صلاح الدين"
                    },
                    "value": 13396
                },
                {
                    "area": {
                        "id": "67ebb7a3-cd3d-480c-ba20-20e8c55c8332",
                        "name": "الرحمانية"
                    },
                    "value": 13259
                },
                {
                    "area": {
                        "id": "86cdd3cf-82dd-461a-8764-5778344f1666",
                        "name": "الفيحاء"
                    },
                    "value": 13240
                },
                {
                    "area": {
                        "id": "48539b17-54d3-4f28-968c-025684a0ceab",
                        "name": "الملك فيصل"
                    },
                    "value": 13228
                },
                {
                    "area": {
                        "id": "b91c2ee4-5fc7-4632-ac89-07e6fc008363",
                        "name": "الملز"
                    },
                    "value": 13218
                },
                {
                    "area": {
                        "id": "c1b851a6-029c-42bc-97f5-bd72af99b3ed",
                        "name": "الروابي"
                    },
                    "value": 13085
                },
                {
                    "area": {
                        "id": "3b880a15-edb7-459d-817b-bbb4e5212ab9",
                        "name": "عكاظ"
                    },
                    "value": 12930
                },
                {
                    "area": {
                        "id": "4731263b-77e7-4938-adc7-a7c5f81b3900",
                        "name": "القيروان"
                    },
                    "value": 12843
                },
                {
                    "area": {
                        "id": "d096152a-b6d5-49c8-84b9-b9ca4a46fd2d",
                        "name": "العليا - العليا"
                    },
                    "value": 12661
                },
                {
                    "area": {
                        "id": "ed69f3e8-523c-4ce7-a493-e92f4f9f1986",
                        "name": "أم الحمام الغربي"
                    },
                    "value": 12628
                },
                {
                    "area": {
                        "id": "a7e5ebed-efe6-4956-a53a-19f21c4a2cf9",
                        "name": "المونسية"
                    },
                    "value": 12458
                },
                {
                    "area": {
                        "id": "cfa2d353-9107-4b34-bccf-533aac553ab4",
                        "name": "الزهراء"
                    },
                    "value": 12382
                },
                {
                    "area": {
                        "id": "b4aed3f7-045a-443e-b340-81043580d7b9",
                        "name": "هجرة وادي لبن"
                    },
                    "value": 12112
                },
                {
                    "area": {
                        "id": "7c07ad55-b15f-48f6-9aed-ebc1e67eff45",
                        "name": "الرمال"
                    },
                    "value": 12059
                },
                {
                    "area": {
                        "id": "61ab70a4-3d37-47bd-a9ee-124bdc0fb670",
                        "name": "المنصورة"
                    },
                    "value": 12027
                },
                {
                    "area": {
                        "id": "cd6e3719-5fb9-497a-91b9-e2668e2e75a6",
                        "name": "الهدا - الديرة"
                    },
                    "value": 11917
                },
                {
                    "area": {
                        "id": "d7a56eca-bec8-49e9-ab68-bfa73a314faa",
                        "name": "السلام"
                    },
                    "value": 11865
                },
                {
                    "area": {
                        "id": "d3e1ad91-49ce-4b0c-bb5d-1fffecd8fafa",
                        "name": "اليرموك"
                    },
                    "value": 11851
                },
                {
                    "area": {
                        "id": "city-3",
                        "name": "الرياض"
                    },
                    "value": 11725
                },
                {
                    "area": {
                        "id": "c0c6513b-13b9-45e1-848a-a4959f95971a",
                        "name": "الملك فهد"
                    },
                    "value": 11701
                },
                {
                    "area": {
                        "id": "c59c5455-500a-4d2b-a7b4-6802fb3f170c",
                        "name": "الرمال"
                    },
                    "value": 11698
                },
                {
                    "area": {
                        "id": "2b62095b-102f-441f-ac00-34602cd48536",
                        "name": "الجزيرة"
                    },
                    "value": 11639
                },
                {
                    "area": {
                        "id": "4ed2e10c-2b71-4414-a8f3-9b8a3f30e560",
                        "name": "العقيق"
                    },
                    "value": 11594
                },
                {
                    "area": {
                        "id": "5b05c230-55c9-499b-a012-887d53d66800",
                        "name": "المربع"
                    },
                    "value": 11488
                },
                {
                    "area": {
                        "id": "aa140531-ded7-47f4-b7d5-591930d0316b",
                        "name": "النهضة"
                    },
                    "value": 11431
                },
                {
                    "area": {
                        "id": "98f7f0d1-438f-4c87-a98f-e0fda41b84bd",
                        "name": "ظهرة نمار"
                    },
                    "value": 11315
                },
                {
                    "area": {
                        "id": "6720febf-8019-40cf-9446-5b2c8474d04d",
                        "name": "الرماية"
                    },
                    "value": 11227
                },
                {
                    "area": {
                        "id": "febe47f1-831b-472c-a068-339a65069dd3",
                        "name": "المعزيلة"
                    },
                    "value": 11109
                },
                {
                    "area": {
                        "id": "e443160a-e66b-4369-a4bf-95f26060eccd",
                        "name": "الحزم"
                    },
                    "value": 11060
                },
                {
                    "area": {
                        "id": "8dba8acc-a41e-4473-8a52-10622bee365b",
                        "name": "الدريهمية"
                    },
                    "value": 10817
                },
                {
                    "area": {
                        "id": "30db56d8-31f6-4a21-81fa-f135163359b1",
                        "name": "الخليج"
                    },
                    "value": 10774
                },
                {
                    "area": {
                        "id": "e9de74de-e178-4d06-856f-1689820e2c5a",
                        "name": "شبرا"
                    },
                    "value": 10611
                },
                {
                    "area": {
                        "id": "c37bc305-4ffc-4489-a6e3-9269b32edb1a",
                        "name": "الإسكان"
                    },
                    "value": 10504
                },
                {
                    "area": {
                        "id": "aff3e994-cc0a-4e88-912d-0690a9983b27",
                        "name": "السويدي الغربي"
                    },
                    "value": 10426
                },
                {
                    "area": {
                        "id": "c8fbfbfe-c1a0-4079-be04-ad20730038b0",
                        "name": "الوزارات"
                    },
                    "value": 10267
                },
                {
                    "area": {
                        "id": "6eea7b8d-e938-466a-ac3e-ae2b106ac59f",
                        "name": "النور"
                    },
                    "value": 10250
                },
                {
                    "area": {
                        "id": "bf723f44-607f-4114-91b9-db8cd0c77a91",
                        "name": "الشفاء"
                    },
                    "value": 10135
                },
                {
                    "area": {
                        "id": "842383e2-3091-4283-b65c-f4a62cd18784",
                        "name": "ظهرة لبن"
                    },
                    "value": 10108
                },
                {
                    "area": {
                        "id": "dde02562-5497-4b68-bb19-baa4d9e93db5",
                        "name": "الخالدية"
                    },
                    "value": 10079
                },
                {
                    "area": {
                        "id": "c35d1f60-d5ff-4885-91c6-85a519c80dcf",
                        "name": "الهدا - المعذر"
                    },
                    "value": 10000
                },
                {
                    "area": {
                        "id": "39ac02a1-c044-4620-9169-b472154e3768",
                        "name": "ظهرة البديعة"
                    },
                    "value": 9849
                },
                {
                    "area": {
                        "id": "fcf3bfcc-4e81-4db1-8fe5-ef65fc610991",
                        "name": "البديعة"
                    },
                    "value": 9848
                },
                {
                    "area": {
                        "id": "b7aeff04-e705-4a9b-ae9f-0da2ac5b3d9e",
                        "name": "القادسية"
                    },
                    "value": 9812
                },
                {
                    "area": {
                        "id": "40772979-0127-4648-b641-dee43ee6b96b",
                        "name": "السويدي"
                    },
                    "value": 9769
                },
                {
                    "area": {
                        "id": "c9fe42ca-2797-466e-b1d1-cb90c69a5605",
                        "name": "المروه"
                    },
                    "value": 9754
                },
                {
                    "area": {
                        "id": "2be8f71f-bb94-4702-87d6-a258a14df452",
                        "name": "الزهرة"
                    },
                    "value": 9742
                },
                {
                    "area": {
                        "id": "7b5f813e-a731-40ef-b3a0-afac81467277",
                        "name": "نمار"
                    },
                    "value": 9730
                },
                {
                    "area": {
                        "id": "7a4897d9-89ac-4d95-a544-2aeee4f1beb2",
                        "name": "الصناعية"
                    },
                    "value": 9625
                },
                {
                    "area": {
                        "id": "01c9ff6a-eb28-4465-a68c-c8a5562c6d39",
                        "name": "بدر"
                    },
                    "value": 9611
                },
                {
                    "area": {
                        "id": "27783c9e-535f-4d44-9a5d-ed549644c5be",
                        "name": "سلطانة - العريجاء"
                    },
                    "value": 9606
                },
                {
                    "area": {
                        "id": "43f724c9-8295-46e4-b80d-af74e659b872",
                        "name": "العريجاء الغربية"
                    },
                    "value": 9575
                },
                {
                    "area": {
                        "id": "751de8ea-eab5-45f3-801f-6a969a57b4e7",
                        "name": "الفاروق"
                    },
                    "value": 9536
                },
                {
                    "area": {
                        "id": "471d8f88-5a0b-4890-8026-a63a835bf52a",
                        "name": "العوالي"
                    },
                    "value": 9260
                },
                {
                    "area": {
                        "id": "5b8e557e-aebe-4553-8402-8973b4ff0a79",
                        "name": "العزيزية"
                    },
                    "value": 9225
                },
                {
                    "area": {
                        "id": "1297bd50-a138-4c61-9898-97d18963331a",
                        "name": "النسيم الشرقي"
                    },
                    "value": 9099
                },
                {
                    "area": {
                        "id": "2fa38d65-6151-493e-98aa-c14c06a28197",
                        "name": "الفاخرية"
                    },
                    "value": 9093
                },
                {
                    "area": {
                        "id": "e85c3bb7-6f91-41de-8447-7a274dc46df3",
                        "name": "أم سليم"
                    },
                    "value": 8983
                },
                {
                    "area": {
                        "id": "758da835-c682-46d6-82ad-0d9fb8442113",
                        "name": "العريجاء"
                    },
                    "value": 8767
                },
                {
                    "area": {
                        "id": "0442bf29-e3f1-4dfa-8afd-b11e063b015a",
                        "name": "العريجاء الوسطى"
                    },
                    "value": 8614
                },
                {
                    "area": {
                        "id": "feb5834c-f023-44d4-8a14-35dc6629017d",
                        "name": "العمل"
                    },
                    "value": 8600
                },
                {
                    "area": {
                        "id": "1f314e74-fac1-4ebf-b83a-830ba70c09c3",
                        "name": "الدرعية"
                    },
                    "value": 8592
                },
                {
                    "area": {
                        "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                        "name": "السعادة"
                    },
                    "value": 8556
                },
                {
                    "area": {
                        "id": "5dfaa455-f597-4c2b-961e-cd2faf15d08f",
                        "name": "النسيم الغربي"
                    },
                    "value": 8368
                },
                {
                    "area": {
                        "id": "c1df54b0-feac-4290-9e75-8afd9e313efb",
                        "name": "طويق - عتيقة"
                    },
                    "value": 8194
                },
                {
                    "area": {
                        "id": "7a9f08b6-502e-4300-87ac-3dc37a27e74c",
                        "name": "النظيم"
                    },
                    "value": 8122
                },
                {
                    "area": {
                        "id": "b65ac3ce-46ab-419d-be64-7aa2761f4c28",
                        "name": "الجنادرية"
                    },
                    "value": 8037
                },
                {
                    "area": {
                        "id": "1bdf2e61-64d7-42c7-bd24-3b58fa806746",
                        "name": "جبرة"
                    },
                    "value": 8000
                },
                {
                    "area": {
                        "id": "7e0fd377-cd04-4845-8b7f-7144752aea0d",
                        "name": "الدفاع"
                    },
                    "value": 8000
                },
                {
                    "area": {
                        "id": "1460a408-4989-4c5e-9e97-494e36c3497a",
                        "name": "ضاحية نمار"
                    },
                    "value": 7870
                },
                {
                    "area": {
                        "id": "920c7560-2916-44ef-ac0e-f1baac271657",
                        "name": "ديراب"
                    },
                    "value": 7791
                },
                {
                    "area": {
                        "id": "4f6a0751-1320-4e27-913b-2dfec0d8aa2f",
                        "name": "الدار البيضاء"
                    },
                    "value": 7750
                },
                {
                    "area": {
                        "id": "3c56b430-f38e-4714-81e3-8a502f8fb971",
                        "name": "السلي"
                    },
                    "value": 7500
                },
                {
                    "area": {
                        "id": "1570d51a-3e9a-4b78-acb2-3d5389cd2a81",
                        "name": "منفوحة الجديدة"
                    },
                    "value": 7351
                },
                {
                    "area": {
                        "id": "f8bed1dc-356d-43a9-b89b-9d1446a74683",
                        "name": "الحائر"
                    },
                    "value": 7203
                },
                {
                    "area": {
                        "id": "14561646-f4ae-4c62-b7f1-8f95156cc0ef",
                        "name": "أحـد"
                    },
                    "value": 6619
                },
                {
                    "area": {
                        "id": "f0eb256e-8c6b-4943-9812-8a10c483b65d",
                        "name": "هيت"
                    },
                    "value": 6571
                },
                {
                    "area": {
                        "id": "27c6e7ac-e6e9-49c9-abc9-c179249cf345",
                        "name": "المناخ"
                    },
                    "value": 6473
                },
                {
                    "area": {
                        "id": "6a6535f2-c3fc-408d-8de8-4d048dd19728",
                        "name": "اليمامة"
                    },
                    "value": 6192
                },
                {
                    "area": {
                        "id": "0434eb81-4f04-4007-92cc-b0c5410bea7c",
                        "name": "الفوطة"
                    },
                    "value": 6000
                },
                {
                    "area": {
                        "id": "33808d06-6a8a-42c1-86b2-79b4709905fd",
                        "name": "الناصرية"
                    },
                    "value": 6000
                },
                {
                    "area": {
                        "id": "1a94924e-c8b8-47ae-b6f4-595f4acf8b3d",
                        "name": "غبيراء"
                    },
                    "value": 5928
                },
                {
                    "area": {
                        "id": "9c5397a5-f624-4116-8db2-34ecf79e5315",
                        "name": "الفيصلية"
                    },
                    "value": 5844
                },
                {
                    "area": {
                        "id": "b2fbbbbc-f12f-44a5-8e76-a674c7a1a9e0",
                        "name": "معكال"
                    },
                    "value": 5750
                },
                {
                    "area": {
                        "id": "fd3f2823-fefa-4c52-aaa9-60150ebd0c37",
                        "name": "الديرة"
                    },
                    "value": 5532
                },
                {
                    "area": {
                        "id": "19381f2a-1d68-4fc3-bc5a-09d5481cf03b",
                        "name": "الجرادية"
                    },
                    "value": 5527
                },
                {
                    "area": {
                        "id": "7dd2b8d2-e89d-408b-bc10-b735809ff749",
                        "name": "المرقب"
                    },
                    "value": 5192
                },
                {
                    "area": {
                        "id": "332ccd9e-8159-49fe-935d-bbb98730c2fc",
                        "name": "الشميسي"
                    },
                    "value": 5110
                },
                {
                    "area": {
                        "id": "ff86addf-942e-41dc-bb0f-9269251b42a3",
                        "name": "منفوحة"
                    },
                    "value": 5072
                },
                {
                    "area": {
                        "id": "3f6c38e8-6b3e-4775-8e1a-905b71f5858a",
                        "name": "الصالحية"
                    },
                    "value": 5008
                },
                {
                    "area": {
                        "id": "51c12d2a-9ae8-4266-adc3-5126aa359cd3",
                        "name": "العود"
                    },
                    "value": 4948
                },
                {
                    "area": {
                        "id": "05fe6a6f-34eb-45eb-82be-260adddd6082",
                        "name": "عتيقة"
                    },
                    "value": 4725
                },
                {
                    "area": {
                        "id": "aa913c8f-ae16-4ee9-a414-1318cda9c41a",
                        "name": "ثليم"
                    },
                    "value": 4034
                },
                {
                    "area": {
                        "id": "113113e3-21a3-4a3a-bfae-3dd799ded51c",
                        "name": "الوسيطا"
                    },
                    "value": 3167
                }
            ]
        },
        "saudiFemale": {
            "facts": [
                {
                    "area": {
                        "id": "c8fbfbfe-c1a0-4079-be04-ad20730038b0",
                        "name": "الوزارات"
                    },
                    "value": 35000
                },
                {
                    "area": {
                        "id": "3f6854d2-c64c-4718-98bb-00c9c1ff6cd3",
                        "name": "الغدير"
                    },
                    "value": 22176
                },
                {
                    "area": {
                        "id": "b7aeff04-e705-4a9b-ae9f-0da2ac5b3d9e",
                        "name": "القادسية"
                    },
                    "value": 18625
                },
                {
                    "area": {
                        "id": "c7f18c78-aae4-4895-a83c-57ce0c761cd1",
                        "name": "جرير"
                    },
                    "value": 18038
                },
                {
                    "area": {
                        "id": "ea03b9a1-d5f3-469f-a9fb-cfb72df61d7f",
                        "name": "المعذر الشمالي"
                    },
                    "value": 17857
                },
                {
                    "area": {
                        "id": "1bdf2e61-64d7-42c7-bd24-3b58fa806746",
                        "name": "جبرة"
                    },
                    "value": 17000
                },
                {
                    "area": {
                        "id": "33808d06-6a8a-42c1-86b2-79b4709905fd",
                        "name": "الناصرية"
                    },
                    "value": 16000
                },
                {
                    "area": {
                        "id": "05fe6a6f-34eb-45eb-82be-260adddd6082",
                        "name": "عتيقة"
                    },
                    "value": 15711
                },
                {
                    "area": {
                        "id": "da870943-28b0-48ef-a7e4-3237b6a3908c",
                        "name": "المحمدية"
                    },
                    "value": 15600
                },
                {
                    "area": {
                        "id": "47e60f73-b741-4d9e-87e4-a4e613d37cde",
                        "name": "الملك عبد العزيز"
                    },
                    "value": 15500
                },
                {
                    "area": {
                        "id": "ea504b74-c266-4b09-b298-08e9dfb35eb5",
                        "name": "الـشـرفـيـة"
                    },
                    "value": 15000
                },
                {
                    "area": {
                        "id": "66566263-1c8d-4e72-85e1-406464b90bbe",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 15000
                },
                {
                    "area": {
                        "id": "228ef43a-9e3e-48cb-bf5e-893d71a6554a",
                        "name": "الرائد"
                    },
                    "value": 14000
                },
                {
                    "area": {
                        "id": "1460a408-4989-4c5e-9e97-494e36c3497a",
                        "name": "ضاحية نمار"
                    },
                    "value": 14000
                },
                {
                    "area": {
                        "id": "13d2af17-de45-4e53-9dcc-17f1f18ba0a1",
                        "name": "المؤتمرات"
                    },
                    "value": 13333
                },
                {
                    "area": {
                        "id": "4731263b-77e7-4938-adc7-a7c5f81b3900",
                        "name": "القيروان"
                    },
                    "value": 13286
                },
                {
                    "area": {
                        "id": "d096152a-b6d5-49c8-84b9-b9ca4a46fd2d",
                        "name": "العليا - العليا"
                    },
                    "value": 13089
                },
                {
                    "area": {
                        "id": "5cf83942-e014-4a10-968d-408e1937b82e",
                        "name": "الورود"
                    },
                    "value": 13070
                },
                {
                    "area": {
                        "id": "a86339c7-1a18-4384-8800-76f1573c04a9",
                        "name": "الواحة"
                    },
                    "value": 13065
                },
                {
                    "area": {
                        "id": "b1a6d8da-05c8-40fd-87e3-6b99a97079d2",
                        "name": "المنار"
                    },
                    "value": 13005
                },
                {
                    "area": {
                        "id": "a01d452c-3a36-4f1b-9ede-2eeb934405a8",
                        "name": "الرفيعة"
                    },
                    "value": 13000
                },
                {
                    "area": {
                        "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                        "name": "السعادة"
                    },
                    "value": 12577
                },
                {
                    "area": {
                        "id": "2f57568c-1f9d-4659-9d1b-70e720b0a45c",
                        "name": "التعاون"
                    },
                    "value": 12563
                },
                {
                    "area": {
                        "id": "c82315c6-3142-41f8-96ff-bc8329391522",
                        "name": "السليمانية - الملز والبطحاء"
                    },
                    "value": 12500
                },
                {
                    "area": {
                        "id": "e8c5f0cc-8565-4a1e-b40d-f1727489f6aa",
                        "name": "الخزامى"
                    },
                    "value": 12333
                },
                {
                    "area": {
                        "id": "206645fd-79d5-44fb-bcc7-4bdafd602a9b",
                        "name": "النفل"
                    },
                    "value": 12313
                },
                {
                    "area": {
                        "id": "c7750a62-e42d-42eb-9e83-aa44bf10a777",
                        "name": "النخيل"
                    },
                    "value": 11983
                },
                {
                    "area": {
                        "id": "5e21ce61-1c87-4d44-bb79-62c105b36cc4",
                        "name": "المغرزات"
                    },
                    "value": 11780
                },
                {
                    "area": {
                        "id": "edd4c9b9-7053-48cf-983e-81c681aab6f8",
                        "name": "حطين"
                    },
                    "value": 11729
                },
                {
                    "area": {
                        "id": "900a8735-f91e-45b7-9702-c556cc4863bc",
                        "name": "الريان"
                    },
                    "value": 11596
                },
                {
                    "area": {
                        "id": "2c51be33-11eb-4645-a407-92d9acd33c9c",
                        "name": "عرقة"
                    },
                    "value": 11559
                },
                {
                    "area": {
                        "id": "d8229af8-3a8a-421b-8e4f-74969f448e47",
                        "name": "الملقا"
                    },
                    "value": 11555
                },
                {
                    "area": {
                        "id": "52d2e2cd-fbb4-4830-84cc-58ae92d267a6",
                        "name": "الإزدهار"
                    },
                    "value": 11482
                },
                {
                    "area": {
                        "id": "c8f985cb-9b86-4d57-957f-b09b2ae78ab9",
                        "name": "المروج"
                    },
                    "value": 11400
                },
                {
                    "area": {
                        "id": "72b24564-20c8-4d3a-9d53-dd559786164d",
                        "name": "الفلاح"
                    },
                    "value": 11294
                },
                {
                    "area": {
                        "id": "8dbab168-3b00-4a12-bc76-dc9d95373cac",
                        "name": "أشبيلية"
                    },
                    "value": 11189
                },
                {
                    "area": {
                        "id": "b91c2ee4-5fc7-4632-ac89-07e6fc008363",
                        "name": "الملز"
                    },
                    "value": 11173
                },
                {
                    "area": {
                        "id": "07310269-69f4-4e5a-a093-3b0686e6f92a",
                        "name": "الحمراء"
                    },
                    "value": 11133
                },
                {
                    "area": {
                        "id": "e443160a-e66b-4369-a4bf-95f26060eccd",
                        "name": "الحزم"
                    },
                    "value": 11100
                },
                {
                    "area": {
                        "id": "0d7ff18e-c7e2-4607-a063-8b7c73b99838",
                        "name": "العليا - المعذر"
                    },
                    "value": 10917
                },
                {
                    "area": {
                        "id": "aa3edb6a-2aaa-4f34-891b-32fd7a64014e",
                        "name": "الربيع"
                    },
                    "value": 10889
                },
                {
                    "area": {
                        "id": "009e646e-bb16-4a74-adda-4791c4cbc9c1",
                        "name": "السليمانية - العليا"
                    },
                    "value": 10866
                },
                {
                    "area": {
                        "id": "7bc70bab-8ac6-42d1-9d55-922d0df681d2",
                        "name": "الربوة"
                    },
                    "value": 10865
                },
                {
                    "area": {
                        "id": "1d18118a-09f4-46a3-a7fe-9f8a4aba9058",
                        "name": "غرناطة"
                    },
                    "value": 10777
                },
                {
                    "area": {
                        "id": "cf8c586f-e220-4ca5-b3d2-c68a2c39df91",
                        "name": "الندي"
                    },
                    "value": 10757
                },
                {
                    "area": {
                        "id": "7566b077-f54c-444e-b41f-fb9ba8bbd8dd",
                        "name": "جامعة الملك سعود"
                    },
                    "value": 10725
                },
                {
                    "area": {
                        "id": "c0c6513b-13b9-45e1-848a-a4959f95971a",
                        "name": "الملك فهد"
                    },
                    "value": 10457
                },
                {
                    "area": {
                        "id": "2ff065d6-764e-40b8-91fd-8210fad92c44",
                        "name": "الملك عبدالله"
                    },
                    "value": 10443
                },
                {
                    "area": {
                        "id": "0e8da9c4-e4a7-4794-a62d-9ab0554e7579",
                        "name": "أم الحمام الشرقي - الديرة"
                    },
                    "value": 10333
                },
                {
                    "area": {
                        "id": "68b0afd0-e462-4930-936b-20532c79f1ad",
                        "name": "قرطبة"
                    },
                    "value": 10310
                },
                {
                    "area": {
                        "id": "7dd2b8d2-e89d-408b-bc10-b735809ff749",
                        "name": "المرقب"
                    },
                    "value": 10300
                },
                {
                    "area": {
                        "id": "8dba8acc-a41e-4473-8a52-10622bee365b",
                        "name": "الدريهمية"
                    },
                    "value": 10288
                },
                {
                    "area": {
                        "id": "cfa2d353-9107-4b34-bccf-533aac553ab4",
                        "name": "الزهراء"
                    },
                    "value": 10286
                },
                {
                    "area": {
                        "id": "ca70401b-2dbf-4153-afcf-35969ce14bfd",
                        "name": "الصحافة"
                    },
                    "value": 10255
                },
                {
                    "area": {
                        "id": "1f8ff56c-ade7-476d-9a18-ebf538ec1767",
                        "name": "الوادي"
                    },
                    "value": 10243
                },
                {
                    "area": {
                        "id": "f2724a71-ad73-4765-8462-f299eff48fec",
                        "name": "القدس"
                    },
                    "value": 10224
                },
                {
                    "area": {
                        "id": "cbb041b7-f87c-4878-821c-16ca4f34e10b",
                        "name": "الياسمين"
                    },
                    "value": 10195
                },
                {
                    "area": {
                        "id": "c59c5455-500a-4d2b-a7b4-6802fb3f170c",
                        "name": "الرمال"
                    },
                    "value": 10173
                },
                {
                    "area": {
                        "id": "5b05c230-55c9-499b-a012-887d53d66800",
                        "name": "المربع"
                    },
                    "value": 10083
                },
                {
                    "area": {
                        "id": "c35d1f60-d5ff-4885-91c6-85a519c80dcf",
                        "name": "الهدا - المعذر"
                    },
                    "value": 10000
                },
                {
                    "area": {
                        "id": "f96795fc-dd23-4de7-9d54-f9050c0f8e9d",
                        "name": "النرجس"
                    },
                    "value": 10000
                },
                {
                    "area": {
                        "id": "7c07ad55-b15f-48f6-9aed-ebc1e67eff45",
                        "name": "الرمال"
                    },
                    "value": 10000
                },
                {
                    "area": {
                        "id": "d36380e7-28b8-4926-a30f-8fc9327abfb1",
                        "name": "النزهه"
                    },
                    "value": 9975
                },
                {
                    "area": {
                        "id": "b4aed3f7-045a-443e-b340-81043580d7b9",
                        "name": "هجرة وادي لبن"
                    },
                    "value": 9934
                },
                {
                    "area": {
                        "id": "a7e5ebed-efe6-4956-a53a-19f21c4a2cf9",
                        "name": "المونسية"
                    },
                    "value": 9861
                },
                {
                    "area": {
                        "id": "38434635-316c-4696-bf6e-0d350cf2e76a",
                        "name": "عليشة"
                    },
                    "value": 9825
                },
                {
                    "area": {
                        "id": "30db56d8-31f6-4a21-81fa-f135163359b1",
                        "name": "الخليج"
                    },
                    "value": 9802
                },
                {
                    "area": {
                        "id": "d0759107-5d0c-4fb3-8ac2-745dbe717ed0",
                        "name": "المصيف"
                    },
                    "value": 9775
                },
                {
                    "area": {
                        "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
                        "name": "صلاح الدين"
                    },
                    "value": 9750
                },
                {
                    "area": {
                        "id": "9d09b05f-35f3-4925-84b1-978e9d701e5e",
                        "name": "أم الحمام الشرقي - المعذر"
                    },
                    "value": 9750
                },
                {
                    "area": {
                        "id": "3b880a15-edb7-459d-817b-bbb4e5212ab9",
                        "name": "عكاظ"
                    },
                    "value": 9750
                },
                {
                    "area": {
                        "id": "c1b851a6-029c-42bc-97f5-bd72af99b3ed",
                        "name": "الروابي"
                    },
                    "value": 9720
                },
                {
                    "area": {
                        "id": "2b62095b-102f-441f-ac00-34602cd48536",
                        "name": "الجزيرة"
                    },
                    "value": 9694
                },
                {
                    "area": {
                        "id": "48539b17-54d3-4f28-968c-025684a0ceab",
                        "name": "الملك فيصل"
                    },
                    "value": 9687
                },
                {
                    "area": {
                        "id": "01c9ff6a-eb28-4465-a68c-c8a5562c6d39",
                        "name": "بدر"
                    },
                    "value": 9666
                },
                {
                    "area": {
                        "id": "city-3",
                        "name": "الرياض"
                    },
                    "value": 9644
                },
                {
                    "area": {
                        "id": "d3e1ad91-49ce-4b0c-bb5d-1fffecd8fafa",
                        "name": "اليرموك"
                    },
                    "value": 9590
                },
                {
                    "area": {
                        "id": "62a893fc-9ec9-4e13-a01e-7191f976e312",
                        "name": "الروضة"
                    },
                    "value": 9541
                },
                {
                    "area": {
                        "id": "86cdd3cf-82dd-461a-8764-5778344f1666",
                        "name": "الفيحاء"
                    },
                    "value": 9526
                },
                {
                    "area": {
                        "id": "843fce03-4fe4-4981-a161-b2284321d375",
                        "name": "النموذجية"
                    },
                    "value": 9500
                },
                {
                    "area": {
                        "id": "67ebb7a3-cd3d-480c-ba20-20e8c55c8332",
                        "name": "الرحمانية"
                    },
                    "value": 9500
                },
                {
                    "area": {
                        "id": "7b5f813e-a731-40ef-b3a0-afac81467277",
                        "name": "نمار"
                    },
                    "value": 9500
                },
                {
                    "area": {
                        "id": "aa140531-ded7-47f4-b7d5-591930d0316b",
                        "name": "النهضة"
                    },
                    "value": 9485
                },
                {
                    "area": {
                        "id": "d7a56eca-bec8-49e9-ab68-bfa73a314faa",
                        "name": "السلام"
                    },
                    "value": 9469
                },
                {
                    "area": {
                        "id": "d6d2d11e-2744-418e-904a-dc8ba194998e",
                        "name": "خشم العان"
                    },
                    "value": 9350
                },
                {
                    "area": {
                        "id": "d8f9c2f5-91d2-4806-be75-b4d5e229e084",
                        "name": "المرسلات"
                    },
                    "value": 9255
                },
                {
                    "area": {
                        "id": "bf723f44-607f-4114-91b9-db8cd0c77a91",
                        "name": "الشفاء"
                    },
                    "value": 9234
                },
                {
                    "area": {
                        "id": "cd6e3719-5fb9-497a-91b9-e2668e2e75a6",
                        "name": "الهدا - الديرة"
                    },
                    "value": 9200
                },
                {
                    "area": {
                        "id": "feb5834c-f023-44d4-8a14-35dc6629017d",
                        "name": "العمل"
                    },
                    "value": 9000
                },
                {
                    "area": {
                        "id": "aff3e994-cc0a-4e88-912d-0690a9983b27",
                        "name": "السويدي الغربي"
                    },
                    "value": 8993
                },
                {
                    "area": {
                        "id": "e9de74de-e178-4d06-856f-1689820e2c5a",
                        "name": "شبرا"
                    },
                    "value": 8682
                },
                {
                    "area": {
                        "id": "4ed2e10c-2b71-4414-a8f3-9b8a3f30e560",
                        "name": "العقيق"
                    },
                    "value": 8588
                },
                {
                    "area": {
                        "id": "d85bc333-4975-421c-9d03-df228e6ae9ea",
                        "name": "الضباط"
                    },
                    "value": 8500
                },
                {
                    "area": {
                        "id": "751de8ea-eab5-45f3-801f-6a969a57b4e7",
                        "name": "الفاروق"
                    },
                    "value": 8500
                },
                {
                    "area": {
                        "id": "842383e2-3091-4283-b65c-f4a62cd18784",
                        "name": "ظهرة لبن"
                    },
                    "value": 8457
                },
                {
                    "area": {
                        "id": "1297bd50-a138-4c61-9898-97d18963331a",
                        "name": "النسيم الشرقي"
                    },
                    "value": 8428
                },
                {
                    "area": {
                        "id": "2be8f71f-bb94-4702-87d6-a258a14df452",
                        "name": "الزهرة"
                    },
                    "value": 8402
                },
                {
                    "area": {
                        "id": "ec66cc90-a1c0-4cb5-873d-7c4757b69971",
                        "name": "الأندلس"
                    },
                    "value": 8389
                },
                {
                    "area": {
                        "id": "7a9f08b6-502e-4300-87ac-3dc37a27e74c",
                        "name": "النظيم"
                    },
                    "value": 8370
                },
                {
                    "area": {
                        "id": "ed69f3e8-523c-4ce7-a493-e92f4f9f1986",
                        "name": "أم الحمام الغربي"
                    },
                    "value": 8333
                },
                {
                    "area": {
                        "id": "4f6a0751-1320-4e27-913b-2dfec0d8aa2f",
                        "name": "الدار البيضاء"
                    },
                    "value": 8320
                },
                {
                    "area": {
                        "id": "7a4897d9-89ac-4d95-a544-2aeee4f1beb2",
                        "name": "الصناعية"
                    },
                    "value": 8250
                },
                {
                    "area": {
                        "id": "39ac02a1-c044-4620-9169-b472154e3768",
                        "name": "ظهرة البديعة"
                    },
                    "value": 8060
                },
                {
                    "area": {
                        "id": "471d8f88-5a0b-4890-8026-a63a835bf52a",
                        "name": "العوالي"
                    },
                    "value": 7957
                },
                {
                    "area": {
                        "id": "40772979-0127-4648-b641-dee43ee6b96b",
                        "name": "السويدي"
                    },
                    "value": 7730
                },
                {
                    "area": {
                        "id": "1f314e74-fac1-4ebf-b83a-830ba70c09c3",
                        "name": "الدرعية"
                    },
                    "value": 7667
                },
                {
                    "area": {
                        "id": "c37bc305-4ffc-4489-a6e3-9269b32edb1a",
                        "name": "الإسكان"
                    },
                    "value": 7578
                },
                {
                    "area": {
                        "id": "0442bf29-e3f1-4dfa-8afd-b11e063b015a",
                        "name": "العريجاء الوسطى"
                    },
                    "value": 7542
                },
                {
                    "area": {
                        "id": "ce4632d7-923a-409e-864a-b9c0e25775b6",
                        "name": "العارض"
                    },
                    "value": 7525
                },
                {
                    "area": {
                        "id": "43f724c9-8295-46e4-b80d-af74e659b872",
                        "name": "العريجاء الغربية"
                    },
                    "value": 7376
                },
                {
                    "area": {
                        "id": "98f7f0d1-438f-4c87-a98f-e0fda41b84bd",
                        "name": "ظهرة نمار"
                    },
                    "value": 7331
                },
                {
                    "area": {
                        "id": "5b8e557e-aebe-4553-8402-8973b4ff0a79",
                        "name": "العزيزية"
                    },
                    "value": 7217
                },
                {
                    "area": {
                        "id": "febe47f1-831b-472c-a068-339a65069dd3",
                        "name": "المعزيلة"
                    },
                    "value": 7175
                },
                {
                    "area": {
                        "id": "c9fe42ca-2797-466e-b1d1-cb90c69a5605",
                        "name": "المروه"
                    },
                    "value": 7160
                },
                {
                    "area": {
                        "id": "b65ac3ce-46ab-419d-be64-7aa2761f4c28",
                        "name": "الجنادرية"
                    },
                    "value": 7150
                },
                {
                    "area": {
                        "id": "5dfaa455-f597-4c2b-961e-cd2faf15d08f",
                        "name": "النسيم الغربي"
                    },
                    "value": 7042
                },
                {
                    "area": {
                        "id": "0434eb81-4f04-4007-92cc-b0c5410bea7c",
                        "name": "الفوطة"
                    },
                    "value": 7000
                },
                {
                    "area": {
                        "id": "3c56b430-f38e-4714-81e3-8a502f8fb971",
                        "name": "السلي"
                    },
                    "value": 7000
                },
                {
                    "area": {
                        "id": "88251c8e-068a-4862-aff5-b6c2feb5e876",
                        "name": "الوشام"
                    },
                    "value": 6867
                },
                {
                    "area": {
                        "id": "27783c9e-535f-4d44-9a5d-ed549644c5be",
                        "name": "سلطانة - العريجاء"
                    },
                    "value": 6829
                },
                {
                    "area": {
                        "id": "61ab70a4-3d37-47bd-a9ee-124bdc0fb670",
                        "name": "المنصورة"
                    },
                    "value": 6773
                },
                {
                    "area": {
                        "id": "c1df54b0-feac-4290-9e75-8afd9e313efb",
                        "name": "طويق - عتيقة"
                    },
                    "value": 6648
                },
                {
                    "area": {
                        "id": "758da835-c682-46d6-82ad-0d9fb8442113",
                        "name": "العريجاء"
                    },
                    "value": 6414
                },
                {
                    "area": {
                        "id": "1570d51a-3e9a-4b78-acb2-3d5389cd2a81",
                        "name": "منفوحة الجديدة"
                    },
                    "value": 6200
                },
                {
                    "area": {
                        "id": "14561646-f4ae-4c62-b7f1-8f95156cc0ef",
                        "name": "أحـد"
                    },
                    "value": 6167
                },
                {
                    "area": {
                        "id": "2fa38d65-6151-493e-98aa-c14c06a28197",
                        "name": "الفاخرية"
                    },
                    "value": 5750
                },
                {
                    "area": {
                        "id": "fcf3bfcc-4e81-4db1-8fe5-ef65fc610991",
                        "name": "البديعة"
                    },
                    "value": 5532
                },
                {
                    "area": {
                        "id": "8014f925-e0b7-4af1-9d9b-20c75afca882",
                        "name": "العليا - الملز والبطحاء"
                    },
                    "value": 5500
                },
                {
                    "area": {
                        "id": "1a94924e-c8b8-47ae-b6f4-595f4acf8b3d",
                        "name": "غبيراء"
                    },
                    "value": 5299
                },
                {
                    "area": {
                        "id": "19381f2a-1d68-4fc3-bc5a-09d5481cf03b",
                        "name": "الجرادية"
                    },
                    "value": 5167
                },
                {
                    "area": {
                        "id": "332ccd9e-8159-49fe-935d-bbb98730c2fc",
                        "name": "الشميسي"
                    },
                    "value": 5163
                },
                {
                    "area": {
                        "id": "f659dd2c-ba77-464d-8a3d-70771ceda67c",
                        "name": "الصفاء"
                    },
                    "value": 5000
                },
                {
                    "area": {
                        "id": "27c6e7ac-e6e9-49c9-abc9-c179249cf345",
                        "name": "المناخ"
                    },
                    "value": 4250
                },
                {
                    "area": {
                        "id": "920c7560-2916-44ef-ac0e-f1baac271657",
                        "name": "ديراب"
                    },
                    "value": 4122
                },
                {
                    "area": {
                        "id": "dde02562-5497-4b68-bb19-baa4d9e93db5",
                        "name": "الخالدية"
                    },
                    "value": 4000
                },
                {
                    "area": {
                        "id": "6a6535f2-c3fc-408d-8de8-4d048dd19728",
                        "name": "اليمامة"
                    },
                    "value": 4000
                },
                {
                    "area": {
                        "id": "aa21340b-3580-4a62-8a43-3d12f6b00501",
                        "name": "السفارات"
                    },
                    "value": 4000
                },
                {
                    "area": {
                        "id": "aa913c8f-ae16-4ee9-a414-1318cda9c41a",
                        "name": "ثليم"
                    },
                    "value": 3900
                },
                {
                    "area": {
                        "id": "51c12d2a-9ae8-4266-adc3-5126aa359cd3",
                        "name": "العود"
                    },
                    "value": 3800
                },
                {
                    "area": {
                        "id": "ff86addf-942e-41dc-bb0f-9269251b42a3",
                        "name": "منفوحة"
                    },
                    "value": 3733
                },
                {
                    "area": {
                        "id": "f8bed1dc-356d-43a9-b89b-9d1446a74683",
                        "name": "الحائر"
                    },
                    "value": 3671
                },
                {
                    "area": {
                        "id": "9c5397a5-f624-4116-8db2-34ecf79e5315",
                        "name": "الفيصلية"
                    },
                    "value": 3125
                },
                {
                    "area": {
                        "id": "fd3f2823-fefa-4c52-aaa9-60150ebd0c37",
                        "name": "الديرة"
                    },
                    "value": 3000
                },
                {
                    "area": {
                        "id": "3f6c38e8-6b3e-4775-8e1a-905b71f5858a",
                        "name": "الصالحية"
                    },
                    "value": 2800
                },
                {
                    "area": {
                        "id": "888e14d1-e0da-4731-a7d7-605372279f88",
                        "name": "الدوبية"
                    },
                    "value": 2000
                }
            ]
        },
        "nonSaudiMale": {
            "facts": [
                {
                    "area": {
                        "id": "aa21340b-3580-4a62-8a43-3d12f6b00501",
                        "name": "السفارات"
                    },
                    "value": 46000
                },
                {
                    "area": {
                        "id": "47e60f73-b741-4d9e-87e4-a4e613d37cde",
                        "name": "الملك عبد العزيز"
                    },
                    "value": 24367
                },
                {
                    "area": {
                        "id": "fde48b0e-8c5f-4683-8cec-c29e7284ebf5",
                        "name": "المعذر"
                    },
                    "value": 21900
                },
                {
                    "area": {
                        "id": "e8c5f0cc-8565-4a1e-b40d-f1727489f6aa",
                        "name": "الخزامى"
                    },
                    "value": 15000
                },
                {
                    "area": {
                        "id": "e59fe6ef-9353-440d-b502-dc8ff67b99fb",
                        "name": "عريض"
                    },
                    "value": 14000
                },
                {
                    "area": {
                        "id": "228ef43a-9e3e-48cb-bf5e-893d71a6554a",
                        "name": "الرائد"
                    },
                    "value": 12700
                },
                {
                    "area": {
                        "id": "8dba8acc-a41e-4473-8a52-10622bee365b",
                        "name": "الدريهمية"
                    },
                    "value": 11886
                },
                {
                    "area": {
                        "id": "5b05c230-55c9-499b-a012-887d53d66800",
                        "name": "المربع"
                    },
                    "value": 10939
                },
                {
                    "area": {
                        "id": "843fce03-4fe4-4981-a161-b2284321d375",
                        "name": "النموذجية"
                    },
                    "value": 10720
                },
                {
                    "area": {
                        "id": "5cf83942-e014-4a10-968d-408e1937b82e",
                        "name": "الورود"
                    },
                    "value": 9519
                },
                {
                    "area": {
                        "id": "2fa38d65-6151-493e-98aa-c14c06a28197",
                        "name": "الفاخرية"
                    },
                    "value": 9396
                },
                {
                    "area": {
                        "id": "c8f985cb-9b86-4d57-957f-b09b2ae78ab9",
                        "name": "المروج"
                    },
                    "value": 8918
                },
                {
                    "area": {
                        "id": "009e646e-bb16-4a74-adda-4791c4cbc9c1",
                        "name": "السليمانية - العليا"
                    },
                    "value": 8386
                },
                {
                    "area": {
                        "id": "8dbab168-3b00-4a12-bc76-dc9d95373cac",
                        "name": "أشبيلية"
                    },
                    "value": 8238
                },
                {
                    "area": {
                        "id": "d85bc333-4975-421c-9d03-df228e6ae9ea",
                        "name": "الضباط"
                    },
                    "value": 8053
                },
                {
                    "area": {
                        "id": "d096152a-b6d5-49c8-84b9-b9ca4a46fd2d",
                        "name": "العليا - العليا"
                    },
                    "value": 7879
                },
                {
                    "area": {
                        "id": "cfa2d353-9107-4b34-bccf-533aac553ab4",
                        "name": "الزهراء"
                    },
                    "value": 7487
                },
                {
                    "area": {
                        "id": "38434635-316c-4696-bf6e-0d350cf2e76a",
                        "name": "عليشة"
                    },
                    "value": 7414
                },
                {
                    "area": {
                        "id": "8014f925-e0b7-4af1-9d9b-20c75afca882",
                        "name": "العليا - الملز والبطحاء"
                    },
                    "value": 7295
                },
                {
                    "area": {
                        "id": "c82315c6-3142-41f8-96ff-bc8329391522",
                        "name": "السليمانية - الملز والبطحاء"
                    },
                    "value": 7167
                },
                {
                    "area": {
                        "id": "f659dd2c-ba77-464d-8a3d-70771ceda67c",
                        "name": "الصفاء"
                    },
                    "value": 7138
                },
                {
                    "area": {
                        "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
                        "name": "صلاح الدين"
                    },
                    "value": 6873
                },
                {
                    "area": {
                        "id": "0434eb81-4f04-4007-92cc-b0c5410bea7c",
                        "name": "الفوطة"
                    },
                    "value": 6846
                },
                {
                    "area": {
                        "id": "0d7ff18e-c7e2-4607-a063-8b7c73b99838",
                        "name": "العليا - المعذر"
                    },
                    "value": 6699
                },
                {
                    "area": {
                        "id": "c37bc305-4ffc-4489-a6e3-9269b32edb1a",
                        "name": "الإسكان"
                    },
                    "value": 6371
                },
                {
                    "area": {
                        "id": "d36380e7-28b8-4926-a30f-8fc9327abfb1",
                        "name": "النزهه"
                    },
                    "value": 6168
                },
                {
                    "area": {
                        "id": "c0c6513b-13b9-45e1-848a-a4959f95971a",
                        "name": "الملك فهد"
                    },
                    "value": 6150
                },
                {
                    "area": {
                        "id": "d8f9c2f5-91d2-4806-be75-b4d5e229e084",
                        "name": "المرسلات"
                    },
                    "value": 5871
                },
                {
                    "area": {
                        "id": "1d18118a-09f4-46a3-a7fe-9f8a4aba9058",
                        "name": "غرناطة"
                    },
                    "value": 5871
                },
                {
                    "area": {
                        "id": "ed69f3e8-523c-4ce7-a493-e92f4f9f1986",
                        "name": "أم الحمام الغربي"
                    },
                    "value": 5777
                },
                {
                    "area": {
                        "id": "ca70401b-2dbf-4153-afcf-35969ce14bfd",
                        "name": "الصحافة"
                    },
                    "value": 5763
                },
                {
                    "area": {
                        "id": "c7f18c78-aae4-4895-a83c-57ce0c761cd1",
                        "name": "جرير"
                    },
                    "value": 5739
                },
                {
                    "area": {
                        "id": "5ce6d443-f294-4559-9329-57509cc90cae",
                        "name": "البطيحا"
                    },
                    "value": 5465
                },
                {
                    "area": {
                        "id": "cf8c586f-e220-4ca5-b3d2-c68a2c39df91",
                        "name": "الندي"
                    },
                    "value": 5406
                },
                {
                    "area": {
                        "id": "a86339c7-1a18-4384-8800-76f1573c04a9",
                        "name": "الواحة"
                    },
                    "value": 5278
                },
                {
                    "area": {
                        "id": "4ed2e10c-2b71-4414-a8f3-9b8a3f30e560",
                        "name": "العقيق"
                    },
                    "value": 5243
                },
                {
                    "area": {
                        "id": "7bc70bab-8ac6-42d1-9d55-922d0df681d2",
                        "name": "الربوة"
                    },
                    "value": 5225
                },
                {
                    "area": {
                        "id": "52d2e2cd-fbb4-4830-84cc-58ae92d267a6",
                        "name": "الإزدهار"
                    },
                    "value": 5157
                },
                {
                    "area": {
                        "id": "b91c2ee4-5fc7-4632-ac89-07e6fc008363",
                        "name": "الملز"
                    },
                    "value": 5140
                },
                {
                    "area": {
                        "id": "206645fd-79d5-44fb-bcc7-4bdafd602a9b",
                        "name": "النفل"
                    },
                    "value": 5104
                },
                {
                    "area": {
                        "id": "d7a56eca-bec8-49e9-ab68-bfa73a314faa",
                        "name": "السلام"
                    },
                    "value": 4937
                },
                {
                    "area": {
                        "id": "61ab70a4-3d37-47bd-a9ee-124bdc0fb670",
                        "name": "المنصورة"
                    },
                    "value": 4909
                },
                {
                    "area": {
                        "id": "751de8ea-eab5-45f3-801f-6a969a57b4e7",
                        "name": "الفاروق"
                    },
                    "value": 4900
                },
                {
                    "area": {
                        "id": "c1b851a6-029c-42bc-97f5-bd72af99b3ed",
                        "name": "الروابي"
                    },
                    "value": 4900
                },
                {
                    "area": {
                        "id": "2f57568c-1f9d-4659-9d1b-70e720b0a45c",
                        "name": "التعاون"
                    },
                    "value": 4875
                },
                {
                    "area": {
                        "id": "2b62095b-102f-441f-ac00-34602cd48536",
                        "name": "الجزيرة"
                    },
                    "value": 4801
                },
                {
                    "area": {
                        "id": "1460a408-4989-4c5e-9e97-494e36c3497a",
                        "name": "ضاحية نمار"
                    },
                    "value": 4800
                },
                {
                    "area": {
                        "id": "d0759107-5d0c-4fb3-8ac2-745dbe717ed0",
                        "name": "المصيف"
                    },
                    "value": 4753
                },
                {
                    "area": {
                        "id": "b4aed3f7-045a-443e-b340-81043580d7b9",
                        "name": "هجرة وادي لبن"
                    },
                    "value": 4687
                },
                {
                    "area": {
                        "id": "aa140531-ded7-47f4-b7d5-591930d0316b",
                        "name": "النهضة"
                    },
                    "value": 4648
                },
                {
                    "area": {
                        "id": "0442bf29-e3f1-4dfa-8afd-b11e063b015a",
                        "name": "العريجاء الوسطى"
                    },
                    "value": 4595
                },
                {
                    "area": {
                        "id": "a7e5ebed-efe6-4956-a53a-19f21c4a2cf9",
                        "name": "المونسية"
                    },
                    "value": 4583
                },
                {
                    "area": {
                        "id": "bf723f44-607f-4114-91b9-db8cd0c77a91",
                        "name": "الشفاء"
                    },
                    "value": 4579
                },
                {
                    "area": {
                        "id": "842383e2-3091-4283-b65c-f4a62cd18784",
                        "name": "ظهرة لبن"
                    },
                    "value": 4535
                },
                {
                    "area": {
                        "id": "5b8e557e-aebe-4553-8402-8973b4ff0a79",
                        "name": "العزيزية"
                    },
                    "value": 4533
                },
                {
                    "area": {
                        "id": "7c07ad55-b15f-48f6-9aed-ebc1e67eff45",
                        "name": "الرمال"
                    },
                    "value": 4500
                },
                {
                    "area": {
                        "id": "88251c8e-068a-4862-aff5-b6c2feb5e876",
                        "name": "الوشام"
                    },
                    "value": 4444
                },
                {
                    "area": {
                        "id": "68b0afd0-e462-4930-936b-20532c79f1ad",
                        "name": "قرطبة"
                    },
                    "value": 4406
                },
                {
                    "area": {
                        "id": "f2724a71-ad73-4765-8462-f299eff48fec",
                        "name": "القدس"
                    },
                    "value": 4388
                },
                {
                    "area": {
                        "id": "c59c5455-500a-4d2b-a7b4-6802fb3f170c",
                        "name": "الرمال"
                    },
                    "value": 4296
                },
                {
                    "area": {
                        "id": "62a893fc-9ec9-4e13-a01e-7191f976e312",
                        "name": "الروضة"
                    },
                    "value": 4235
                },
                {
                    "area": {
                        "id": "e9de74de-e178-4d06-856f-1689820e2c5a",
                        "name": "شبرا"
                    },
                    "value": 4220
                },
                {
                    "area": {
                        "id": "a01d452c-3a36-4f1b-9ede-2eeb934405a8",
                        "name": "الرفيعة"
                    },
                    "value": 4120
                },
                {
                    "area": {
                        "id": "7a9f08b6-502e-4300-87ac-3dc37a27e74c",
                        "name": "النظيم"
                    },
                    "value": 4084
                },
                {
                    "area": {
                        "id": "039f1dd3-6866-4e6c-8f4f-53ba926d1f50",
                        "name": "القرى"
                    },
                    "value": 4000
                },
                {
                    "area": {
                        "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                        "name": "السعادة"
                    },
                    "value": 3937
                },
                {
                    "area": {
                        "id": "9d09b05f-35f3-4925-84b1-978e9d701e5e",
                        "name": "أم الحمام الشرقي - المعذر"
                    },
                    "value": 3893
                },
                {
                    "area": {
                        "id": "d8229af8-3a8a-421b-8e4f-74969f448e47",
                        "name": "الملقا"
                    },
                    "value": 3773
                },
                {
                    "area": {
                        "id": "city-3",
                        "name": "الرياض"
                    },
                    "value": 3749
                },
                {
                    "area": {
                        "id": "2ff065d6-764e-40b8-91fd-8210fad92c44",
                        "name": "الملك عبدالله"
                    },
                    "value": 3685
                },
                {
                    "area": {
                        "id": "471d8f88-5a0b-4890-8026-a63a835bf52a",
                        "name": "العوالي"
                    },
                    "value": 3663
                },
                {
                    "area": {
                        "id": "c8fbfbfe-c1a0-4079-be04-ad20730038b0",
                        "name": "الوزارات"
                    },
                    "value": 3639
                },
                {
                    "area": {
                        "id": "feb5834c-f023-44d4-8a14-35dc6629017d",
                        "name": "العمل"
                    },
                    "value": 3625
                },
                {
                    "area": {
                        "id": "3b880a15-edb7-459d-817b-bbb4e5212ab9",
                        "name": "عكاظ"
                    },
                    "value": 3611
                },
                {
                    "area": {
                        "id": "0e8da9c4-e4a7-4794-a62d-9ab0554e7579",
                        "name": "أم الحمام الشرقي - الديرة"
                    },
                    "value": 3608
                },
                {
                    "area": {
                        "id": "86cdd3cf-82dd-461a-8764-5778344f1666",
                        "name": "الفيحاء"
                    },
                    "value": 3601
                },
                {
                    "area": {
                        "id": "c7750a62-e42d-42eb-9e83-aa44bf10a777",
                        "name": "النخيل"
                    },
                    "value": 3599
                },
                {
                    "area": {
                        "id": "d3e1ad91-49ce-4b0c-bb5d-1fffecd8fafa",
                        "name": "اليرموك"
                    },
                    "value": 3591
                },
                {
                    "area": {
                        "id": "07310269-69f4-4e5a-a093-3b0686e6f92a",
                        "name": "الحمراء"
                    },
                    "value": 3590
                },
                {
                    "area": {
                        "id": "ea504b74-c266-4b09-b298-08e9dfb35eb5",
                        "name": "الـشـرفـيـة"
                    },
                    "value": 3481
                },
                {
                    "area": {
                        "id": "1297bd50-a138-4c61-9898-97d18963331a",
                        "name": "النسيم الشرقي"
                    },
                    "value": 3448
                },
                {
                    "area": {
                        "id": "4f6a0751-1320-4e27-913b-2dfec0d8aa2f",
                        "name": "الدار البيضاء"
                    },
                    "value": 3448
                },
                {
                    "area": {
                        "id": "1a94924e-c8b8-47ae-b6f4-595f4acf8b3d",
                        "name": "غبيراء"
                    },
                    "value": 3420
                },
                {
                    "area": {
                        "id": "b1a6d8da-05c8-40fd-87e3-6b99a97079d2",
                        "name": "المنار"
                    },
                    "value": 3361
                },
                {
                    "area": {
                        "id": "b65ac3ce-46ab-419d-be64-7aa2761f4c28",
                        "name": "الجنادرية"
                    },
                    "value": 3357
                },
                {
                    "area": {
                        "id": "5dfaa455-f597-4c2b-961e-cd2faf15d08f",
                        "name": "النسيم الغربي"
                    },
                    "value": 3339
                },
                {
                    "area": {
                        "id": "febe47f1-831b-472c-a068-339a65069dd3",
                        "name": "المعزيلة"
                    },
                    "value": 3300
                },
                {
                    "area": {
                        "id": "408b741e-1704-4e36-be99-3c9201ef4b51",
                        "name": "صياح"
                    },
                    "value": 3153
                },
                {
                    "area": {
                        "id": "40772979-0127-4648-b641-dee43ee6b96b",
                        "name": "السويدي"
                    },
                    "value": 3129
                },
                {
                    "area": {
                        "id": "4731263b-77e7-4938-adc7-a7c5f81b3900",
                        "name": "القيروان"
                    },
                    "value": 3117
                },
                {
                    "area": {
                        "id": "27783c9e-535f-4d44-9a5d-ed549644c5be",
                        "name": "سلطانة - العريجاء"
                    },
                    "value": 3111
                },
                {
                    "area": {
                        "id": "ec66cc90-a1c0-4cb5-873d-7c4757b69971",
                        "name": "الأندلس"
                    },
                    "value": 3109
                },
                {
                    "area": {
                        "id": "900a8735-f91e-45b7-9702-c556cc4863bc",
                        "name": "الريان"
                    },
                    "value": 3105
                },
                {
                    "area": {
                        "id": "dde02562-5497-4b68-bb19-baa4d9e93db5",
                        "name": "الخالدية"
                    },
                    "value": 3056
                },
                {
                    "area": {
                        "id": "33808d06-6a8a-42c1-86b2-79b4709905fd",
                        "name": "الناصرية"
                    },
                    "value": 3017
                },
                {
                    "area": {
                        "id": "48539b17-54d3-4f28-968c-025684a0ceab",
                        "name": "الملك فيصل"
                    },
                    "value": 3010
                },
                {
                    "area": {
                        "id": "30db56d8-31f6-4a21-81fa-f135163359b1",
                        "name": "الخليج"
                    },
                    "value": 2995
                },
                {
                    "area": {
                        "id": "2c51be33-11eb-4645-a407-92d9acd33c9c",
                        "name": "عرقة"
                    },
                    "value": 2974
                },
                {
                    "area": {
                        "id": "5e21ce61-1c87-4d44-bb79-62c105b36cc4",
                        "name": "المغرزات"
                    },
                    "value": 2920
                },
                {
                    "area": {
                        "id": "43f724c9-8295-46e4-b80d-af74e659b872",
                        "name": "العريجاء الغربية"
                    },
                    "value": 2866
                },
                {
                    "area": {
                        "id": "1bdf2e61-64d7-42c7-bd24-3b58fa806746",
                        "name": "جبرة"
                    },
                    "value": 2860
                },
                {
                    "area": {
                        "id": "72b24564-20c8-4d3a-9d53-dd559786164d",
                        "name": "الفلاح"
                    },
                    "value": 2815
                },
                {
                    "area": {
                        "id": "6a6535f2-c3fc-408d-8de8-4d048dd19728",
                        "name": "اليمامة"
                    },
                    "value": 2755
                },
                {
                    "area": {
                        "id": "39ac02a1-c044-4620-9169-b472154e3768",
                        "name": "ظهرة البديعة"
                    },
                    "value": 2699
                },
                {
                    "area": {
                        "id": "9c5397a5-f624-4116-8db2-34ecf79e5315",
                        "name": "الفيصلية"
                    },
                    "value": 2690
                },
                {
                    "area": {
                        "id": "fd3f2823-fefa-4c52-aaa9-60150ebd0c37",
                        "name": "الديرة"
                    },
                    "value": 2687
                },
                {
                    "area": {
                        "id": "113113e3-21a3-4a3a-bfae-3dd799ded51c",
                        "name": "الوسيطا"
                    },
                    "value": 2657
                },
                {
                    "area": {
                        "id": "1f314e74-fac1-4ebf-b83a-830ba70c09c3",
                        "name": "الدرعية"
                    },
                    "value": 2643
                },
                {
                    "area": {
                        "id": "fcf3bfcc-4e81-4db1-8fe5-ef65fc610991",
                        "name": "البديعة"
                    },
                    "value": 2626
                },
                {
                    "area": {
                        "id": "1f8ff56c-ade7-476d-9a18-ebf538ec1767",
                        "name": "الوادي"
                    },
                    "value": 2619
                },
                {
                    "area": {
                        "id": "edd4c9b9-7053-48cf-983e-81c681aab6f8",
                        "name": "حطين"
                    },
                    "value": 2542
                },
                {
                    "area": {
                        "id": "05fe6a6f-34eb-45eb-82be-260adddd6082",
                        "name": "عتيقة"
                    },
                    "value": 2518
                },
                {
                    "area": {
                        "id": "2be8f71f-bb94-4702-87d6-a258a14df452",
                        "name": "الزهرة"
                    },
                    "value": 2504
                },
                {
                    "area": {
                        "id": "cbb041b7-f87c-4878-821c-16ca4f34e10b",
                        "name": "الياسمين"
                    },
                    "value": 2503
                },
                {
                    "area": {
                        "id": "1570d51a-3e9a-4b78-acb2-3d5389cd2a81",
                        "name": "منفوحة الجديدة"
                    },
                    "value": 2500
                },
                {
                    "area": {
                        "id": "c1df54b0-feac-4290-9e75-8afd9e313efb",
                        "name": "طويق - عتيقة"
                    },
                    "value": 2483
                },
                {
                    "area": {
                        "id": "7dd2b8d2-e89d-408b-bc10-b735809ff749",
                        "name": "المرقب"
                    },
                    "value": 2480
                },
                {
                    "area": {
                        "id": "aa913c8f-ae16-4ee9-a414-1318cda9c41a",
                        "name": "ثليم"
                    },
                    "value": 2462
                },
                {
                    "area": {
                        "id": "920c7560-2916-44ef-ac0e-f1baac271657",
                        "name": "ديراب"
                    },
                    "value": 2453
                },
                {
                    "area": {
                        "id": "7b5f813e-a731-40ef-b3a0-afac81467277",
                        "name": "نمار"
                    },
                    "value": 2438
                },
                {
                    "area": {
                        "id": "01c9ff6a-eb28-4465-a68c-c8a5562c6d39",
                        "name": "بدر"
                    },
                    "value": 2424
                },
                {
                    "area": {
                        "id": "51c12d2a-9ae8-4266-adc3-5126aa359cd3",
                        "name": "العود"
                    },
                    "value": 2414
                },
                {
                    "area": {
                        "id": "f0eb256e-8c6b-4943-9812-8a10c483b65d",
                        "name": "هيت"
                    },
                    "value": 2410
                },
                {
                    "area": {
                        "id": "332ccd9e-8159-49fe-935d-bbb98730c2fc",
                        "name": "الشميسي"
                    },
                    "value": 2406
                },
                {
                    "area": {
                        "id": "b9945c44-61a0-4d1e-85f2-24eefe9611ae",
                        "name": "سلطانة - الديرة"
                    },
                    "value": 2406
                },
                {
                    "area": {
                        "id": "e85c3bb7-6f91-41de-8447-7a274dc46df3",
                        "name": "أم سليم"
                    },
                    "value": 2347
                },
                {
                    "area": {
                        "id": "19381f2a-1d68-4fc3-bc5a-09d5481cf03b",
                        "name": "الجرادية"
                    },
                    "value": 2339
                },
                {
                    "area": {
                        "id": "6eea7b8d-e938-466a-ac3e-ae2b106ac59f",
                        "name": "النور"
                    },
                    "value": 2300
                },
                {
                    "area": {
                        "id": "758da835-c682-46d6-82ad-0d9fb8442113",
                        "name": "العريجاء"
                    },
                    "value": 2300
                },
                {
                    "area": {
                        "id": "aff3e994-cc0a-4e88-912d-0690a9983b27",
                        "name": "السويدي الغربي"
                    },
                    "value": 2278
                },
                {
                    "area": {
                        "id": "67ebb7a3-cd3d-480c-ba20-20e8c55c8332",
                        "name": "الرحمانية"
                    },
                    "value": 2245
                },
                {
                    "area": {
                        "id": "b7aeff04-e705-4a9b-ae9f-0da2ac5b3d9e",
                        "name": "القادسية"
                    },
                    "value": 2219
                },
                {
                    "area": {
                        "id": "7a4897d9-89ac-4d95-a544-2aeee4f1beb2",
                        "name": "الصناعية"
                    },
                    "value": 2216
                },
                {
                    "area": {
                        "id": "3f6c38e8-6b3e-4775-8e1a-905b71f5858a",
                        "name": "الصالحية"
                    },
                    "value": 2211
                },
                {
                    "area": {
                        "id": "ff86addf-942e-41dc-bb0f-9269251b42a3",
                        "name": "منفوحة"
                    },
                    "value": 2188
                },
                {
                    "area": {
                        "id": "aa3edb6a-2aaa-4f34-891b-32fd7a64014e",
                        "name": "الربيع"
                    },
                    "value": 2179
                },
                {
                    "area": {
                        "id": "e443160a-e66b-4369-a4bf-95f26060eccd",
                        "name": "الحزم"
                    },
                    "value": 2154
                },
                {
                    "area": {
                        "id": "b2fbbbbc-f12f-44a5-8e76-a674c7a1a9e0",
                        "name": "معكال"
                    },
                    "value": 2151
                },
                {
                    "area": {
                        "id": "c9fe42ca-2797-466e-b1d1-cb90c69a5605",
                        "name": "المروه"
                    },
                    "value": 2141
                },
                {
                    "area": {
                        "id": "ea03b9a1-d5f3-469f-a9fb-cfb72df61d7f",
                        "name": "المعذر الشمالي"
                    },
                    "value": 2140
                },
                {
                    "area": {
                        "id": "bc3d0470-797d-4659-9d54-2d5048e158f3",
                        "name": "المصانع"
                    },
                    "value": 2073
                },
                {
                    "area": {
                        "id": "f8bed1dc-356d-43a9-b89b-9d1446a74683",
                        "name": "الحائر"
                    },
                    "value": 2023
                },
                {
                    "area": {
                        "id": "2911ee84-265f-44d7-8105-4c5ea9e1c72b",
                        "name": "طيبة"
                    },
                    "value": 2000
                },
                {
                    "area": {
                        "id": "14561646-f4ae-4c62-b7f1-8f95156cc0ef",
                        "name": "أحـد"
                    },
                    "value": 2000
                },
                {
                    "area": {
                        "id": "a29b89a8-30fd-4d75-9945-ecfec789c7cc",
                        "name": "المهدية"
                    },
                    "value": 2000
                },
                {
                    "area": {
                        "id": "27c6e7ac-e6e9-49c9-abc9-c179249cf345",
                        "name": "المناخ"
                    },
                    "value": 1984
                },
                {
                    "area": {
                        "id": "888e14d1-e0da-4731-a7d7-605372279f88",
                        "name": "الدوبية"
                    },
                    "value": 1956
                },
                {
                    "area": {
                        "id": "baa1d3f2-7268-4abf-b839-02bd717dfeca",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 1955
                },
                {
                    "area": {
                        "id": "1476a71c-9823-4053-9439-cb7b7ce6a7fa",
                        "name": "سلام"
                    },
                    "value": 1932
                },
                {
                    "area": {
                        "id": "13d2af17-de45-4e53-9dcc-17f1f18ba0a1",
                        "name": "المؤتمرات"
                    },
                    "value": 1900
                },
                {
                    "area": {
                        "id": "3f6854d2-c64c-4718-98bb-00c9c1ff6cd3",
                        "name": "الغدير"
                    },
                    "value": 1878
                },
                {
                    "area": {
                        "id": "3c56b430-f38e-4714-81e3-8a502f8fb971",
                        "name": "السلي"
                    },
                    "value": 1866
                },
                {
                    "area": {
                        "id": "66566263-1c8d-4e72-85e1-406464b90bbe",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 1768
                },
                {
                    "area": {
                        "id": "ce4632d7-923a-409e-864a-b9c0e25775b6",
                        "name": "العارض"
                    },
                    "value": 1761
                },
                {
                    "area": {
                        "id": "da870943-28b0-48ef-a7e4-3237b6a3908c",
                        "name": "المحمدية"
                    },
                    "value": 1759
                },
                {
                    "area": {
                        "id": "076e4790-fa1c-4add-9531-491da2447079",
                        "name": "المصفاة"
                    },
                    "value": 1580
                },
                {
                    "area": {
                        "id": "f96795fc-dd23-4de7-9d54-f9050c0f8e9d",
                        "name": "النرجس"
                    },
                    "value": 1572
                },
                {
                    "area": {
                        "id": "cd6e3719-5fb9-497a-91b9-e2668e2e75a6",
                        "name": "الهدا - الديرة"
                    },
                    "value": 1500
                },
                {
                    "area": {
                        "id": "7566b077-f54c-444e-b41f-fb9ba8bbd8dd",
                        "name": "جامعة الملك سعود"
                    },
                    "value": 1500
                },
                {
                    "area": {
                        "id": "977a2aab-df59-47b7-86c6-0e653c3c4cfd",
                        "name": "المنصورية"
                    },
                    "value": 1500
                },
                {
                    "area": {
                        "id": "7e0fd377-cd04-4845-8b7f-7144752aea0d",
                        "name": "الدفاع"
                    },
                    "value": 1471
                },
                {
                    "area": {
                        "id": "98f7f0d1-438f-4c87-a98f-e0fda41b84bd",
                        "name": "ظهرة نمار"
                    },
                    "value": 1456
                },
                {
                    "area": {
                        "id": "d6d2d11e-2744-418e-904a-dc8ba194998e",
                        "name": "خشم العان"
                    },
                    "value": 1289
                }
            ]
        },
        "nonSaudiFemale": {
            "facts": [
                {
                    "area": {
                        "id": "aa21340b-3580-4a62-8a43-3d12f6b00501",
                        "name": "السفارات"
                    },
                    "value": 21500
                },
                {
                    "area": {
                        "id": "228ef43a-9e3e-48cb-bf5e-893d71a6554a",
                        "name": "الرائد"
                    },
                    "value": 12000
                },
                {
                    "area": {
                        "id": "0434eb81-4f04-4007-92cc-b0c5410bea7c",
                        "name": "الفوطة"
                    },
                    "value": 7000
                },
                {
                    "area": {
                        "id": "d85bc333-4975-421c-9d03-df228e6ae9ea",
                        "name": "الضباط"
                    },
                    "value": 5950
                },
                {
                    "area": {
                        "id": "fde48b0e-8c5f-4683-8cec-c29e7284ebf5",
                        "name": "المعذر"
                    },
                    "value": 5750
                },
                {
                    "area": {
                        "id": "c35d1f60-d5ff-4885-91c6-85a519c80dcf",
                        "name": "الهدا - المعذر"
                    },
                    "value": 5000
                },
                {
                    "area": {
                        "id": "d096152a-b6d5-49c8-84b9-b9ca4a46fd2d",
                        "name": "العليا - العليا"
                    },
                    "value": 4392
                },
                {
                    "area": {
                        "id": "1570d51a-3e9a-4b78-acb2-3d5389cd2a81",
                        "name": "منفوحة الجديدة"
                    },
                    "value": 4333
                },
                {
                    "area": {
                        "id": "cf8c586f-e220-4ca5-b3d2-c68a2c39df91",
                        "name": "الندي"
                    },
                    "value": 4130
                },
                {
                    "area": {
                        "id": "c8fbfbfe-c1a0-4079-be04-ad20730038b0",
                        "name": "الوزارات"
                    },
                    "value": 4050
                },
                {
                    "area": {
                        "id": "fd3f2823-fefa-4c52-aaa9-60150ebd0c37",
                        "name": "الديرة"
                    },
                    "value": 4000
                },
                {
                    "area": {
                        "id": "ec66cc90-a1c0-4cb5-873d-7c4757b69971",
                        "name": "الأندلس"
                    },
                    "value": 3900
                },
                {
                    "area": {
                        "id": "d0759107-5d0c-4fb3-8ac2-745dbe717ed0",
                        "name": "المصيف"
                    },
                    "value": 3633
                },
                {
                    "area": {
                        "id": "47e60f73-b741-4d9e-87e4-a4e613d37cde",
                        "name": "الملك عبد العزيز"
                    },
                    "value": 3289
                },
                {
                    "area": {
                        "id": "d36380e7-28b8-4926-a30f-8fc9327abfb1",
                        "name": "النزهه"
                    },
                    "value": 3121
                },
                {
                    "area": {
                        "id": "5b05c230-55c9-499b-a012-887d53d66800",
                        "name": "المربع"
                    },
                    "value": 3081
                },
                {
                    "area": {
                        "id": "33808d06-6a8a-42c1-86b2-79b4709905fd",
                        "name": "الناصرية"
                    },
                    "value": 3075
                },
                {
                    "area": {
                        "id": "1a94924e-c8b8-47ae-b6f4-595f4acf8b3d",
                        "name": "غبيراء"
                    },
                    "value": 3064
                },
                {
                    "area": {
                        "id": "332ccd9e-8159-49fe-935d-bbb98730c2fc",
                        "name": "الشميسي"
                    },
                    "value": 3029
                },
                {
                    "area": {
                        "id": "9d09b05f-35f3-4925-84b1-978e9d701e5e",
                        "name": "أم الحمام الشرقي - المعذر"
                    },
                    "value": 2836
                },
                {
                    "area": {
                        "id": "0d7ff18e-c7e2-4607-a063-8b7c73b99838",
                        "name": "العليا - المعذر"
                    },
                    "value": 2725
                },
                {
                    "area": {
                        "id": "1d18118a-09f4-46a3-a7fe-9f8a4aba9058",
                        "name": "غرناطة"
                    },
                    "value": 2718
                },
                {
                    "area": {
                        "id": "feb5834c-f023-44d4-8a14-35dc6629017d",
                        "name": "العمل"
                    },
                    "value": 2525
                },
                {
                    "area": {
                        "id": "888e14d1-e0da-4731-a7d7-605372279f88",
                        "name": "الدوبية"
                    },
                    "value": 2500
                },
                {
                    "area": {
                        "id": "843fce03-4fe4-4981-a161-b2284321d375",
                        "name": "النموذجية"
                    },
                    "value": 2475
                },
                {
                    "area": {
                        "id": "ea03b9a1-d5f3-469f-a9fb-cfb72df61d7f",
                        "name": "المعذر الشمالي"
                    },
                    "value": 2462
                },
                {
                    "area": {
                        "id": "1297bd50-a138-4c61-9898-97d18963331a",
                        "name": "النسيم الشرقي"
                    },
                    "value": 2450
                },
                {
                    "area": {
                        "id": "e85c3bb7-6f91-41de-8447-7a274dc46df3",
                        "name": "أم سليم"
                    },
                    "value": 2443
                },
                {
                    "area": {
                        "id": "c59c5455-500a-4d2b-a7b4-6802fb3f170c",
                        "name": "الرمال"
                    },
                    "value": 2375
                },
                {
                    "area": {
                        "id": "2c51be33-11eb-4645-a407-92d9acd33c9c",
                        "name": "عرقة"
                    },
                    "value": 2355
                },
                {
                    "area": {
                        "id": "1bdf2e61-64d7-42c7-bd24-3b58fa806746",
                        "name": "جبرة"
                    },
                    "value": 2300
                },
                {
                    "area": {
                        "id": "d3e1ad91-49ce-4b0c-bb5d-1fffecd8fafa",
                        "name": "اليرموك"
                    },
                    "value": 2290
                },
                {
                    "area": {
                        "id": "f2724a71-ad73-4765-8462-f299eff48fec",
                        "name": "القدس"
                    },
                    "value": 2288
                },
                {
                    "area": {
                        "id": "fcf3bfcc-4e81-4db1-8fe5-ef65fc610991",
                        "name": "البديعة"
                    },
                    "value": 2240
                },
                {
                    "area": {
                        "id": "d7a56eca-bec8-49e9-ab68-bfa73a314faa",
                        "name": "السلام"
                    },
                    "value": 2172
                },
                {
                    "area": {
                        "id": "009e646e-bb16-4a74-adda-4791c4cbc9c1",
                        "name": "السليمانية - العليا"
                    },
                    "value": 2079
                },
                {
                    "area": {
                        "id": "88251c8e-068a-4862-aff5-b6c2feb5e876",
                        "name": "الوشام"
                    },
                    "value": 2057
                },
                {
                    "area": {
                        "id": "07310269-69f4-4e5a-a093-3b0686e6f92a",
                        "name": "الحمراء"
                    },
                    "value": 2045
                },
                {
                    "area": {
                        "id": "0e8da9c4-e4a7-4794-a62d-9ab0554e7579",
                        "name": "أم الحمام الشرقي - الديرة"
                    },
                    "value": 2043
                },
                {
                    "area": {
                        "id": "c0c6513b-13b9-45e1-848a-a4959f95971a",
                        "name": "الملك فهد"
                    },
                    "value": 2005
                },
                {
                    "area": {
                        "id": "dde02562-5497-4b68-bb19-baa4d9e93db5",
                        "name": "الخالدية"
                    },
                    "value": 2000
                },
                {
                    "area": {
                        "id": "19381f2a-1d68-4fc3-bc5a-09d5481cf03b",
                        "name": "الجرادية"
                    },
                    "value": 2000
                },
                {
                    "area": {
                        "id": "27783c9e-535f-4d44-9a5d-ed549644c5be",
                        "name": "سلطانة - العريجاء"
                    },
                    "value": 1979
                },
                {
                    "area": {
                        "id": "68b0afd0-e462-4930-936b-20532c79f1ad",
                        "name": "قرطبة"
                    },
                    "value": 1978
                },
                {
                    "area": {
                        "id": "ed69f3e8-523c-4ce7-a493-e92f4f9f1986",
                        "name": "أم الحمام الغربي"
                    },
                    "value": 1973
                },
                {
                    "area": {
                        "id": "a86339c7-1a18-4384-8800-76f1573c04a9",
                        "name": "الواحة"
                    },
                    "value": 1957
                },
                {
                    "area": {
                        "id": "5e21ce61-1c87-4d44-bb79-62c105b36cc4",
                        "name": "المغرزات"
                    },
                    "value": 1921
                },
                {
                    "area": {
                        "id": "0442bf29-e3f1-4dfa-8afd-b11e063b015a",
                        "name": "العريجاء الوسطى"
                    },
                    "value": 1921
                },
                {
                    "area": {
                        "id": "7bc70bab-8ac6-42d1-9d55-922d0df681d2",
                        "name": "الربوة"
                    },
                    "value": 1900
                },
                {
                    "area": {
                        "id": "a7e5ebed-efe6-4956-a53a-19f21c4a2cf9",
                        "name": "المونسية"
                    },
                    "value": 1848
                },
                {
                    "area": {
                        "id": "city-3",
                        "name": "الرياض"
                    },
                    "value": 1840
                },
                {
                    "area": {
                        "id": "4f6a0751-1320-4e27-913b-2dfec0d8aa2f",
                        "name": "الدار البيضاء"
                    },
                    "value": 1817
                },
                {
                    "area": {
                        "id": "b91c2ee4-5fc7-4632-ac89-07e6fc008363",
                        "name": "الملز"
                    },
                    "value": 1813
                },
                {
                    "area": {
                        "id": "206645fd-79d5-44fb-bcc7-4bdafd602a9b",
                        "name": "النفل"
                    },
                    "value": 1802
                },
                {
                    "area": {
                        "id": "73890e3c-ec19-489f-8ad8-59b52b9e5b7f",
                        "name": "صلاح الدين"
                    },
                    "value": 1800
                },
                {
                    "area": {
                        "id": "61ab70a4-3d37-47bd-a9ee-124bdc0fb670",
                        "name": "المنصورة"
                    },
                    "value": 1782
                },
                {
                    "area": {
                        "id": "6a6535f2-c3fc-408d-8de8-4d048dd19728",
                        "name": "اليمامة"
                    },
                    "value": 1776
                },
                {
                    "area": {
                        "id": "aff3e994-cc0a-4e88-912d-0690a9983b27",
                        "name": "السويدي الغربي"
                    },
                    "value": 1728
                },
                {
                    "area": {
                        "id": "0f92057c-dd62-4975-83bb-7e5ebd897727",
                        "name": "السعادة"
                    },
                    "value": 1721
                },
                {
                    "area": {
                        "id": "1f8ff56c-ade7-476d-9a18-ebf538ec1767",
                        "name": "الوادي"
                    },
                    "value": 1719
                },
                {
                    "area": {
                        "id": "39ac02a1-c044-4620-9169-b472154e3768",
                        "name": "ظهرة البديعة"
                    },
                    "value": 1709
                },
                {
                    "area": {
                        "id": "5cf83942-e014-4a10-968d-408e1937b82e",
                        "name": "الورود"
                    },
                    "value": 1708
                },
                {
                    "area": {
                        "id": "4ed2e10c-2b71-4414-a8f3-9b8a3f30e560",
                        "name": "العقيق"
                    },
                    "value": 1695
                },
                {
                    "area": {
                        "id": "86cdd3cf-82dd-461a-8764-5778344f1666",
                        "name": "الفيحاء"
                    },
                    "value": 1685
                },
                {
                    "area": {
                        "id": "a01d452c-3a36-4f1b-9ede-2eeb934405a8",
                        "name": "الرفيعة"
                    },
                    "value": 1674
                },
                {
                    "area": {
                        "id": "52d2e2cd-fbb4-4830-84cc-58ae92d267a6",
                        "name": "الإزدهار"
                    },
                    "value": 1671
                },
                {
                    "area": {
                        "id": "c8f985cb-9b86-4d57-957f-b09b2ae78ab9",
                        "name": "المروج"
                    },
                    "value": 1668
                },
                {
                    "area": {
                        "id": "5dfaa455-f597-4c2b-961e-cd2faf15d08f",
                        "name": "النسيم الغربي"
                    },
                    "value": 1666
                },
                {
                    "area": {
                        "id": "43f724c9-8295-46e4-b80d-af74e659b872",
                        "name": "العريجاء الغربية"
                    },
                    "value": 1641
                },
                {
                    "area": {
                        "id": "c7750a62-e42d-42eb-9e83-aa44bf10a777",
                        "name": "النخيل"
                    },
                    "value": 1635
                },
                {
                    "area": {
                        "id": "aa3edb6a-2aaa-4f34-891b-32fd7a64014e",
                        "name": "الربيع"
                    },
                    "value": 1613
                },
                {
                    "area": {
                        "id": "b1a6d8da-05c8-40fd-87e3-6b99a97079d2",
                        "name": "المنار"
                    },
                    "value": 1587
                },
                {
                    "area": {
                        "id": "471d8f88-5a0b-4890-8026-a63a835bf52a",
                        "name": "العوالي"
                    },
                    "value": 1567
                },
                {
                    "area": {
                        "id": "13d2af17-de45-4e53-9dcc-17f1f18ba0a1",
                        "name": "المؤتمرات"
                    },
                    "value": 1550
                },
                {
                    "area": {
                        "id": "2b62095b-102f-441f-ac00-34602cd48536",
                        "name": "الجزيرة"
                    },
                    "value": 1545
                },
                {
                    "area": {
                        "id": "ea504b74-c266-4b09-b298-08e9dfb35eb5",
                        "name": "الـشـرفـيـة"
                    },
                    "value": 1533
                },
                {
                    "area": {
                        "id": "cbb041b7-f87c-4878-821c-16ca4f34e10b",
                        "name": "الياسمين"
                    },
                    "value": 1501
                },
                {
                    "area": {
                        "id": "3c56b430-f38e-4714-81e3-8a502f8fb971",
                        "name": "السلي"
                    },
                    "value": 1500
                },
                {
                    "area": {
                        "id": "66566263-1c8d-4e72-85e1-406464b90bbe",
                        "name": "المدينة الصناعية الجديدة"
                    },
                    "value": 1500
                },
                {
                    "area": {
                        "id": "7566b077-f54c-444e-b41f-fb9ba8bbd8dd",
                        "name": "جامعة الملك سعود"
                    },
                    "value": 1492
                },
                {
                    "area": {
                        "id": "2f57568c-1f9d-4659-9d1b-70e720b0a45c",
                        "name": "التعاون"
                    },
                    "value": 1477
                },
                {
                    "area": {
                        "id": "8dbab168-3b00-4a12-bc76-dc9d95373cac",
                        "name": "أشبيلية"
                    },
                    "value": 1469
                },
                {
                    "area": {
                        "id": "5b8e557e-aebe-4553-8402-8973b4ff0a79",
                        "name": "العزيزية"
                    },
                    "value": 1451
                },
                {
                    "area": {
                        "id": "4731263b-77e7-4938-adc7-a7c5f81b3900",
                        "name": "القيروان"
                    },
                    "value": 1450
                },
                {
                    "area": {
                        "id": "bf723f44-607f-4114-91b9-db8cd0c77a91",
                        "name": "الشفاء"
                    },
                    "value": 1442
                },
                {
                    "area": {
                        "id": "cd6e3719-5fb9-497a-91b9-e2668e2e75a6",
                        "name": "الهدا - الديرة"
                    },
                    "value": 1440
                },
                {
                    "area": {
                        "id": "30db56d8-31f6-4a21-81fa-f135163359b1",
                        "name": "الخليج"
                    },
                    "value": 1410
                },
                {
                    "area": {
                        "id": "7a4897d9-89ac-4d95-a544-2aeee4f1beb2",
                        "name": "الصناعية"
                    },
                    "value": 1400
                },
                {
                    "area": {
                        "id": "3f6c38e8-6b3e-4775-8e1a-905b71f5858a",
                        "name": "الصالحية"
                    },
                    "value": 1400
                },
                {
                    "area": {
                        "id": "c1b851a6-029c-42bc-97f5-bd72af99b3ed",
                        "name": "الروابي"
                    },
                    "value": 1394
                },
                {
                    "area": {
                        "id": "40772979-0127-4648-b641-dee43ee6b96b",
                        "name": "السويدي"
                    },
                    "value": 1391
                },
                {
                    "area": {
                        "id": "c7f18c78-aae4-4895-a83c-57ce0c761cd1",
                        "name": "جرير"
                    },
                    "value": 1388
                },
                {
                    "area": {
                        "id": "d6d2d11e-2744-418e-904a-dc8ba194998e",
                        "name": "خشم العان"
                    },
                    "value": 1377
                },
                {
                    "area": {
                        "id": "05fe6a6f-34eb-45eb-82be-260adddd6082",
                        "name": "عتيقة"
                    },
                    "value": 1367
                },
                {
                    "area": {
                        "id": "2ff065d6-764e-40b8-91fd-8210fad92c44",
                        "name": "الملك عبدالله"
                    },
                    "value": 1355
                },
                {
                    "area": {
                        "id": "842383e2-3091-4283-b65c-f4a62cd18784",
                        "name": "ظهرة لبن"
                    },
                    "value": 1353
                },
                {
                    "area": {
                        "id": "72b24564-20c8-4d3a-9d53-dd559786164d",
                        "name": "الفلاح"
                    },
                    "value": 1350
                },
                {
                    "area": {
                        "id": "62a893fc-9ec9-4e13-a01e-7191f976e312",
                        "name": "الروضة"
                    },
                    "value": 1348
                },
                {
                    "area": {
                        "id": "67ebb7a3-cd3d-480c-ba20-20e8c55c8332",
                        "name": "الرحمانية"
                    },
                    "value": 1338
                },
                {
                    "area": {
                        "id": "d8229af8-3a8a-421b-8e4f-74969f448e47",
                        "name": "الملقا"
                    },
                    "value": 1337
                },
                {
                    "area": {
                        "id": "01c9ff6a-eb28-4465-a68c-c8a5562c6d39",
                        "name": "بدر"
                    },
                    "value": 1333
                },
                {
                    "area": {
                        "id": "900a8735-f91e-45b7-9702-c556cc4863bc",
                        "name": "الريان"
                    },
                    "value": 1325
                },
                {
                    "area": {
                        "id": "c82315c6-3142-41f8-96ff-bc8329391522",
                        "name": "السليمانية - الملز والبطحاء"
                    },
                    "value": 1321
                },
                {
                    "area": {
                        "id": "98f7f0d1-438f-4c87-a98f-e0fda41b84bd",
                        "name": "ظهرة نمار"
                    },
                    "value": 1320
                },
                {
                    "area": {
                        "id": "da870943-28b0-48ef-a7e4-3237b6a3908c",
                        "name": "المحمدية"
                    },
                    "value": 1317
                },
                {
                    "area": {
                        "id": "3f6854d2-c64c-4718-98bb-00c9c1ff6cd3",
                        "name": "الغدير"
                    },
                    "value": 1316
                },
                {
                    "area": {
                        "id": "f96795fc-dd23-4de7-9d54-f9050c0f8e9d",
                        "name": "النرجس"
                    },
                    "value": 1308
                },
                {
                    "area": {
                        "id": "d8f9c2f5-91d2-4806-be75-b4d5e229e084",
                        "name": "المرسلات"
                    },
                    "value": 1300
                },
                {
                    "area": {
                        "id": "8014f925-e0b7-4af1-9d9b-20c75afca882",
                        "name": "العليا - الملز والبطحاء"
                    },
                    "value": 1300
                },
                {
                    "area": {
                        "id": "cfa2d353-9107-4b34-bccf-533aac553ab4",
                        "name": "الزهراء"
                    },
                    "value": 1300
                },
                {
                    "area": {
                        "id": "ca70401b-2dbf-4153-afcf-35969ce14bfd",
                        "name": "الصحافة"
                    },
                    "value": 1289
                },
                {
                    "area": {
                        "id": "e9de74de-e178-4d06-856f-1689820e2c5a",
                        "name": "شبرا"
                    },
                    "value": 1289
                },
                {
                    "area": {
                        "id": "38434635-316c-4696-bf6e-0d350cf2e76a",
                        "name": "عليشة"
                    },
                    "value": 1276
                },
                {
                    "area": {
                        "id": "751de8ea-eab5-45f3-801f-6a969a57b4e7",
                        "name": "الفاروق"
                    },
                    "value": 1275
                },
                {
                    "area": {
                        "id": "e443160a-e66b-4369-a4bf-95f26060eccd",
                        "name": "الحزم"
                    },
                    "value": 1273
                },
                {
                    "area": {
                        "id": "c9fe42ca-2797-466e-b1d1-cb90c69a5605",
                        "name": "المروه"
                    },
                    "value": 1271
                },
                {
                    "area": {
                        "id": "8dba8acc-a41e-4473-8a52-10622bee365b",
                        "name": "الدريهمية"
                    },
                    "value": 1271
                },
                {
                    "area": {
                        "id": "b4aed3f7-045a-443e-b340-81043580d7b9",
                        "name": "هجرة وادي لبن"
                    },
                    "value": 1264
                },
                {
                    "area": {
                        "id": "7b5f813e-a731-40ef-b3a0-afac81467277",
                        "name": "نمار"
                    },
                    "value": 1250
                },
                {
                    "area": {
                        "id": "aa140531-ded7-47f4-b7d5-591930d0316b",
                        "name": "النهضة"
                    },
                    "value": 1239
                },
                {
                    "area": {
                        "id": "c37bc305-4ffc-4489-a6e3-9269b32edb1a",
                        "name": "الإسكان"
                    },
                    "value": 1239
                },
                {
                    "area": {
                        "id": "920c7560-2916-44ef-ac0e-f1baac271657",
                        "name": "ديراب"
                    },
                    "value": 1220
                },
                {
                    "area": {
                        "id": "1f314e74-fac1-4ebf-b83a-830ba70c09c3",
                        "name": "الدرعية"
                    },
                    "value": 1220
                },
                {
                    "area": {
                        "id": "c1df54b0-feac-4290-9e75-8afd9e313efb",
                        "name": "طويق - عتيقة"
                    },
                    "value": 1203
                },
                {
                    "area": {
                        "id": "6720febf-8019-40cf-9446-5b2c8474d04d",
                        "name": "الرماية"
                    },
                    "value": 1200
                },
                {
                    "area": {
                        "id": "2be8f71f-bb94-4702-87d6-a258a14df452",
                        "name": "الزهرة"
                    },
                    "value": 1184
                },
                {
                    "area": {
                        "id": "edd4c9b9-7053-48cf-983e-81c681aab6f8",
                        "name": "حطين"
                    },
                    "value": 1180
                },
                {
                    "area": {
                        "id": "14561646-f4ae-4c62-b7f1-8f95156cc0ef",
                        "name": "أحـد"
                    },
                    "value": 1175
                },
                {
                    "area": {
                        "id": "758da835-c682-46d6-82ad-0d9fb8442113",
                        "name": "العريجاء"
                    },
                    "value": 1160
                },
                {
                    "area": {
                        "id": "ce4632d7-923a-409e-864a-b9c0e25775b6",
                        "name": "العارض"
                    },
                    "value": 1157
                },
                {
                    "area": {
                        "id": "48539b17-54d3-4f28-968c-025684a0ceab",
                        "name": "الملك فيصل"
                    },
                    "value": 1109
                },
                {
                    "area": {
                        "id": "b7aeff04-e705-4a9b-ae9f-0da2ac5b3d9e",
                        "name": "القادسية"
                    },
                    "value": 1089
                },
                {
                    "area": {
                        "id": "b65ac3ce-46ab-419d-be64-7aa2761f4c28",
                        "name": "الجنادرية"
                    },
                    "value": 1050
                },
                {
                    "area": {
                        "id": "3b880a15-edb7-459d-817b-bbb4e5212ab9",
                        "name": "عكاظ"
                    },
                    "value": 1033
                },
                {
                    "area": {
                        "id": "7a9f08b6-502e-4300-87ac-3dc37a27e74c",
                        "name": "النظيم"
                    },
                    "value": 1019
                },
                {
                    "area": {
                        "id": "f659dd2c-ba77-464d-8a3d-70771ceda67c",
                        "name": "الصفاء"
                    },
                    "value": 1000
                },
                {
                    "area": {
                        "id": "7c07ad55-b15f-48f6-9aed-ebc1e67eff45",
                        "name": "الرمال"
                    },
                    "value": 1000
                },
                {
                    "area": {
                        "id": "e8c5f0cc-8565-4a1e-b40d-f1727489f6aa",
                        "name": "الخزامى"
                    },
                    "value": 1000
                },
                {
                    "area": {
                        "id": "febe47f1-831b-472c-a068-339a65069dd3",
                        "name": "المعزيلة"
                    },
                    "value": 967
                },
                {
                    "area": {
                        "id": "2fa38d65-6151-493e-98aa-c14c06a28197",
                        "name": "الفاخرية"
                    },
                    "value": 933
                },
                {
                    "area": {
                        "id": "9c5397a5-f624-4116-8db2-34ecf79e5315",
                        "name": "الفيصلية"
                    },
                    "value": 600
                }
            ]
        }
    }
}