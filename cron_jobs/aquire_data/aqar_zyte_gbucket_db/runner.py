from step1_aquire_data import  aquire_data,asyncio
from step2_transform_to_csv import transform_to_csv
from step3_upload_csv_to_gbucket import upload_csv
if __name__ == "__main__":
    asyncio.run(aquire_data())
    transform_to_csv()
    upload_csv()