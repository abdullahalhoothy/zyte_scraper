from pipeline import *

# Training pipeline
# it requires the zad file to be in the cache
db_string, city = ("postgresql://scraper_user:scraper@37.27.195.216:5432/dbo_operational", ["الرياض", "Riyadh"])
income_data = get_dataset(db_string, city)
models = train_model(income_data) 
#it will save everything to the the model's directory