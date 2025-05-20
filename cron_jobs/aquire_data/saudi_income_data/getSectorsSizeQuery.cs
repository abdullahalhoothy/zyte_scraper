{
  "operationName": "getSectorsSizeQuery",
  "variables": {
    "minLat": 24.60439987071683,
    "maxLat": 24.744788621363405,
    "minLng": 46.728102507324195,
    "maxLng": 46.89083749267576,
    "areas": ["86cdd3cf-82dd-461a-8764-5778344f1666"]
  },
  "query": "..."
}

query getSectorsSizeQuery($areas: [String]) {
  businesses {
    aggregationByIsic(areas: $areas) {
      isicBuckets {
        isic {
          id
        }
        size
      }
    }
    size(areas: $areas)
  }
}

# response

{
    "data": {
        "businesses": {
            "aggregationByIsic": {
                "isicBuckets": [
                    {
                        "isic": {
                            "id": "94cb2323-11ed-4bde-8dca-1a5925aec321"
                        },
                        "size": 372
                    },
                    {
                        "isic": {
                            "id": "e0493032-eaed-4f12-bbcf-b7a47de0e04e"
                        },
                        "size": 355
                    },
                    {
                        "isic": {
                            "id": "e8eb3aec-c720-44c0-a533-1515592bd7f0"
                        },
                        "size": 59
                    },
                    {
                        "isic": {
                            "id": "0764ae2d-772e-4a54-99ee-a899ec4b13d3"
                        },
                        "size": 55
                    },
                    {
                        "isic": {
                            "id": "60131ab6-c6bd-430d-98a6-566e438e7352"
                        },
                        "size": 54
                    },
                    {
                        "isic": {
                            "id": "a6ec01f1-7b44-4e36-ad2a-c2dd3bbf1247"
                        },
                        "size": 50
                    },
                    {
                        "isic": {
                            "id": "73ff1100-cef1-4135-aca8-87fb209aaea8"
                        },
                        "size": 42
                    },
                    {
                        "isic": {
                            "id": "08275155-61ed-42bf-a4c1-de4e3da8cc0b"
                        },
                        "size": 37
                    },
                    {
                        "isic": {
                            "id": "7b7dfd80-1a4b-45e7-9437-26572c459ebc"
                        },
                        "size": 37
                    },
                    {
                        "isic": {
                            "id": "4bd17b42-dad0-457c-a0f6-9e256fe274a6"
                        },
                        "size": 35
                    },
                    {
                        "isic": {
                            "id": "842b8326-6677-48e4-b911-a378eeceb60c"
                        },
                        "size": 35
                    },
                    {
                        "isic": {
                            "id": "274e24e0-b2d8-4886-9fdb-9ce7742515ff"
                        },
                        "size": 33
                    },
                    {
                        "isic": {
                            "id": "0cbc9359-7f7f-4994-b16c-837f6ac4e35c"
                        },
                        "size": 27
                    },
                    {
                        "isic": {
                            "id": "4eb78773-38e4-4e09-8a60-425024f65a72"
                        },
                        "size": 26
                    },
                    {
                        "isic": {
                            "id": "1d3b312d-282f-4620-827e-a81e8e7a25b9"
                        },
                        "size": 23
                    },
                    {
                        "isic": {
                            "id": "aec93087-9aaa-4b9f-9e4e-4ce4a87f9973"
                        },
                        "size": 22
                    },
                    {
                        "isic": {
                            "id": "b406f2ed-73f2-46db-9cde-139b899ffb43"
                        },
                        "size": 22
                    },
                    {
                        "isic": {
                            "id": "82f0b72a-e794-4ad2-ad15-63f60a518b4e"
                        },
                        "size": 21
                    },
                    {
                        "isic": {
                            "id": "b06cd56e-3e71-4381-b93d-058a5fcd0b90"
                        },
                        "size": 21
                    },
                    {
                        "isic": {
                            "id": "3a3f65c1-3f4a-4d42-8635-d76d82462001"
                        },
                        "size": 18
                    },
                    {
                        "isic": {
                            "id": "ab0f96d1-253a-491b-a7aa-016d92b5ae55"
                        },
                        "size": 18
                    },
                    {
                        "isic": {
                            "id": "2425b2ab-8699-46b8-8d95-448adc6edcf1"
                        },
                        "size": 15
                    },
                    {
                        "isic": {
                            "id": "4c85bb53-eb91-47a3-bd26-ad1703f0b856"
                        },
                        "size": 15
                    },
                    {
                        "isic": {
                            "id": "5d1f9726-fba3-4d2a-b1dc-540ff9a186e0"
                        },
                        "size": 15
                    },
                    {
                        "isic": {
                            "id": "7642bf48-338d-4a8f-b7ef-9abb33a3f2b3"
                        },
                        "size": 13
                    },
                    {
                        "isic": {
                            "id": "925ceb56-5323-43dd-9416-816aa536b23e"
                        },
                        "size": 13
                    },
                    {
                        "isic": {
                            "id": "c34f32de-a989-4b15-a2b2-9804d1023c27"
                        },
                        "size": 13
                    },
                    {
                        "isic": {
                            "id": "1f8d0d4e-3931-41ff-93c8-870177be798e"
                        },
                        "size": 11
                    },
                    {
                        "isic": {
                            "id": "71997f77-9e50-4396-89e9-bb44bd8cd5da"
                        },
                        "size": 11
                    },
                    {
                        "isic": {
                            "id": "8e931b3f-597d-4e87-b046-92c28147c156"
                        },
                        "size": 11
                    },
                    {
                        "isic": {
                            "id": "e143aab6-87f6-4df7-9675-7acefaaf5e8d"
                        },
                        "size": 11
                    },
                    {
                        "isic": {
                            "id": "26c7ac7d-1252-4659-8763-0ad5218b4628"
                        },
                        "size": 10
                    },
                    {
                        "isic": {
                            "id": "38f8cdf5-f5f2-4cfd-966f-675151e14a99"
                        },
                        "size": 10
                    },
                    {
                        "isic": {
                            "id": "4078b5b2-ecfe-4c18-be35-3efbff4e6e5b"
                        },
                        "size": 10
                    },
                    {
                        "isic": {
                            "id": "c11f83f3-7091-461a-8fc6-0bd76175f8fe"
                        },
                        "size": 10
                    },
                    {
                        "isic": {
                            "id": "367f8501-3324-4ea6-8d3e-5a4fedde1b11"
                        },
                        "size": 9
                    },
                    {
                        "isic": {
                            "id": "751ab4b6-289e-462c-ba35-a760b4799ae8"
                        },
                        "size": 9
                    },
                    {
                        "isic": {
                            "id": "e9b30a10-d85f-4625-9977-fadb61cdabd5"
                        },
                        "size": 9
                    },
                    {
                        "isic": {
                            "id": "f542b929-4f5b-44eb-9236-ebd93d22fc15"
                        },
                        "size": 9
                    },
                    {
                        "isic": {
                            "id": "3f852951-674f-47b2-a100-053e450272bf"
                        },
                        "size": 8
                    },
                    {
                        "isic": {
                            "id": "0d173f08-5210-42c9-b751-3e7d6c8813b7"
                        },
                        "size": 7
                    },
                    {
                        "isic": {
                            "id": "20d1b0f2-235c-49c5-bde2-ebff18fe87a6"
                        },
                        "size": 7
                    },
                    {
                        "isic": {
                            "id": "54c2a843-aea1-483d-a0d5-8863f5b61a6e"
                        },
                        "size": 7
                    },
                    {
                        "isic": {
                            "id": "caab0604-f25c-47e8-801e-f921b59d5848"
                        },
                        "size": 7
                    },
                    {
                        "isic": {
                            "id": "23a7d054-a988-46fa-b4f8-3721b240caa9"
                        },
                        "size": 6
                    },
                    {
                        "isic": {
                            "id": "7fda16b3-dc27-4d43-98c2-576262f31d02"
                        },
                        "size": 6
                    },
                    {
                        "isic": {
                            "id": "9e0713b9-03fd-4750-a3ec-40813b3b0a64"
                        },
                        "size": 6
                    },
                    {
                        "isic": {
                            "id": "c3f2d83c-f80f-4baa-9a90-a3908fdccd4c"
                        },
                        "size": 6
                    },
                    {
                        "isic": {
                            "id": "9adb4efd-ccbf-477d-930b-f176a401d170"
                        },
                        "size": 5
                    },
                    {
                        "isic": {
                            "id": "25e6a113-3203-4477-ad7c-7a663f8ee454"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "6f429007-94ed-4dcf-8533-e6effae00d68"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "81cef395-50e2-4b80-8d5e-714deeb66d71"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "836e4bd8-4bb1-46b9-bc5b-5aec23cb2cb3"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "af24f64f-b19d-4ec9-815e-c599507ee649"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "d258fe31-f7c6-4cfb-bbef-488bef1f64c1"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "d40c7727-81f1-44e0-bade-9eac6812c6c7"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "f5bbf33c-2987-4064-8067-c340eafdf848"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "f6a1c598-6106-4e37-8245-e5d2fdb6ba27"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "f89e6a5e-0607-46f0-9ae7-05838253ccba"
                        },
                        "size": 4
                    },
                    {
                        "isic": {
                            "id": "1bb364ea-a9e7-4fb6-bab1-71674a11adb8"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "2accd954-117c-49ca-a765-1692ec7329dc"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "2ec9a9d7-fe2e-4658-8ed4-a00cb4fe7ed3"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "46ad5e95-b19d-4ca7-ace0-600dd5b475fa"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "728eed8b-6fce-40fb-a203-476b92cdcc07"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "73a91dde-cfbe-443c-914e-a5aaafe32ea1"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "a60d0fa0-25de-4d63-84ab-a5429c46083c"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "bda5ce02-3fe1-443f-a45d-8927a4b1d9c9"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "dc428b64-ad4f-4191-8d56-ac40f743abbe"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "e9618fe9-ff4b-434a-a6c6-5f851f78ee83"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "f0b8f8cd-5396-43c5-ad0f-169f9b8227f2"
                        },
                        "size": 3
                    },
                    {
                        "isic": {
                            "id": "0c79971f-9109-44ef-8f3c-d69d372ac184"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "1a27279f-16d6-488a-ba8a-f4f27b2ddbfc"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "275e46ce-77ae-4bf9-af19-b13c1bc9a843"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "6476a35b-7e75-4cb3-be5a-0ce4445d9809"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "68b058b3-c2cb-4d5b-a89f-708dc2b952d3"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "6b234d08-5f2f-4c10-ad57-a63a9a6cd5d2"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "7acc4962-eccf-4a81-a064-d948238c4695"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "7dbad637-4e08-4ad4-bc21-8e87bd3017a6"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "801c482b-3aa9-4780-910c-3461b39af63c"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "82c997f6-37bd-4594-96b7-f70c461edaa4"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "8589eb4d-72a1-498b-8ed2-c88170ee088c"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "a2103c0e-ad42-4c7c-8aa2-a840caa20b4d"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "a597fb03-1166-49f7-82fe-e72b45823819"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "b15b5984-6ccb-43ae-b2df-1944407b7c8e"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "b83ca2c4-a613-4d4e-8bcc-134cff4234e5"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "c7b46288-0c60-4660-8660-96c281263c4e"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "c7d89582-81e8-40bd-8a0d-9d9af447510c"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "d1965e3b-1931-41aa-b323-cff0fd44f453"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "dc097266-dac5-42c0-9935-adf350fb9dc7"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "e6da9847-54fd-4461-96dc-e2a126f04266"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "ff8f5127-d5e7-451a-b1f6-402174fc1858"
                        },
                        "size": 2
                    },
                    {
                        "isic": {
                            "id": "02b67111-9a8e-424e-a6a0-ce8f83078ae8"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "0a33480e-2cec-461e-8823-ca5ea47c74b3"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "0ca9f944-a2a7-42ae-95d1-522620c27560"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "116a1313-d325-411a-8594-03f57856c36a"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "142be633-a78c-4117-91a2-c321b700222d"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "1960f0b3-56c3-46c6-962d-5311cbcfc2a8"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "1d369487-f60a-4475-beb4-5390e9f0b7bb"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "22d967fd-a067-43d4-9e16-0da514a89d64"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "277a48f4-2ef7-44fa-9c2b-238d28783b55"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "2dcf2b70-08fc-47e5-b530-611b22ac728d"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "2f5de16e-0fa5-4380-8d90-0e66d0d3787c"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "2f82b6b3-dffa-4f4f-86dd-059d83aca195"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "2fcd6b4c-60ee-4dd9-8c09-37f0af3329bc"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "35092fa1-7f6f-4e05-8682-343d027731b0"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "42b36ef1-02b6-47dd-a057-bc6aeac9fc8d"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "493f492b-8ee0-478e-a0b6-b44cd0e8f6c4"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "4ec33a4a-099b-4575-9fd3-1935e7fa9b05"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "53fcaf6c-528a-4279-a64c-24067157cfae"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "5987869b-cae4-47f1-b1a0-2d94a7625d03"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "639a411f-162e-4905-8aa6-f4f74d112dd2"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "6d982cfc-d81d-45a3-a78e-4bc709ea8b93"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "73a1e722-5068-43b0-83c1-99cdbf85e1e9"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "74d149cc-c613-4fa3-8bfd-be299d5adbb5"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "754dd99c-959b-424c-9207-da2418650b61"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "7be91a31-8367-4797-9323-3495fd53824b"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "858fba78-dec8-4065-98c6-9649426fffe5"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "8cbcf6a8-9283-406f-bbb8-1ed575e1d24b"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "9b3c7b1e-89a6-4f0e-86bb-5f73ea9a964a"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "a9d7c189-5de6-4114-b7a3-f6ec74a10c07"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "ad382eae-ae95-4066-ba4c-349a87926399"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "ad3b9628-3ff8-4bd2-b1b0-a8a26ab68fab"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "b263bcac-9690-4936-acd5-def77031da18"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "b5516ebd-c8cf-4640-a775-d57a98b0fbda"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "bb0403ca-d364-46ec-8d31-a666fefb6ec7"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "bfb1dc7e-07ba-41b5-a62b-29414710c589"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "c1a99483-8f6e-4ea7-8ed3-bb4e27825a17"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "c5d1e31e-7ade-4273-9eb2-a554a712ccdb"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "cbd0385e-0d22-4d59-bd86-6556cccf477c"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "cd0098b6-0324-4f31-93ce-edb9787aecee"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "ce688146-7ea4-4d3e-aaaa-a3f9efa900a4"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "d69dc7ed-4086-4532-910f-5f5507148ac6"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "d6f5146b-044e-4ba0-b6ba-ac702a7134e3"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "d707de10-d219-4b73-8a8a-452973a1f7ea"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "e393e9d0-cb28-446e-8a8c-8a69d58f9d76"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "ed062c78-284d-4218-8cef-e20af5bf9679"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "ede0c91a-653d-4c41-9fc9-aac53de1294f"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "f95847da-5936-478d-90af-3d72eb26c967"
                        },
                        "size": 1
                    },
                    {
                        "isic": {
                            "id": "fcba2874-1621-4b42-bb57-1abf88ea73e6"
                        },
                        "size": 1
                    }
                ]
            },
            "size": 897
        }
    }
}
