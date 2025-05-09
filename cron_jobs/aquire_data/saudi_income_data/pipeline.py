import os
import numpy as np
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry import box

import logging
from sklearn.model_selection import RepeatedKFold
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb


def load_data(db_access_key, city):
    os.makedirs("cache", exist_ok=True)

    if os.path.isfile("cache/real_estate_data.csv"):
        real_estate_data = pd.read_csv("cache/real_estate_data.csv")
    else:
        engine = create_engine(db_access_key)
        real_estate_data = pd.read_sql(
            """
              SELECT url, price, latitude, longitude, category_ar, category_id, city, city_id, title, address, rent_period, category, price_description
              FROM raw_schema_marketplace.saudi_real_estate;
          """,
            engine,
        )
        real_estate_data.to_csv("cache/real_estate_data.csv", index=False)

    if os.path.isfile("cache/housing_data.csv"):
        housing_data = pd.read_csv("cache/housing_data.csv")
    else:
        engine = create_engine(db_access_key)
        housing_data = pd.read_sql(
            f"""
                    SELECT "Location", "Selector", "Degree", "TotalDwellings", "ResidentialDwellings", "OwnedDwellings", "RentedDwellings", "ProvidedDwellings", "OtherResidentialDwellings", "Non-ResidentialDwellings", "PublicHousing", "WorkCamps", "CommercialDwellings", "OtherDwellings", "ZoomLevel", "TopLeftDegree", "BottomRightDegree", "ID", "Parent"
                    FROM raw_schema_marketplace.housing;
                        """,
            engine,
        )
        housing_data.to_csv("cache/housing_data.csv", index=False)

    population_data = gpd.GeoDataFrame.from_features(
        pd.read_json("cache/all_features.json").features
    )

    restaurants_data = pd.read_csv(
        f"cache/restaurants_{city[-1].lower()}_full.csv"
    ).rename(columns={"lat": "latitude", "lng": "longitude"})

    royal_houses = pd.read_csv(f"cache/{city[-1].lower()}_royal_houses.csv").rename(
        columns={"lat": "latitude", "lng": "longitude"}
    )

    luxury_hotels = pd.read_csv(f"cache/{city[-1].lower()}_luxury hotel.csv").rename(
        columns={"lat": "latitude", "lng": "longitude"}
    )

    gyms = pd.read_csv(f"cache/{city[-1].lower()}_gym.csv").rename(
        columns={"lat": "latitude", "lng": "longitude"}
    )

    luxurious_areas = pd.read_csv(
        f"cache/{city[-1].lower()}_luxurious_areas.csv"
    ).rename(columns={"lat": "latitude", "lng": "longitude"})

    return (
        real_estate_data,
        housing_data,
        population_data,
        restaurants_data,
        royal_houses,
        luxury_hotels,
        gyms,
        luxurious_areas,
    )


def get_geodataframes(
    real_estate_data,
    housing_data,
    population_data,
    restaurants_data,
    royal_houses,
    luxury_hotels,
    gyms,
    luxurious_areas,
    city,
):

    grid_size = np.round((population_data.geometry.area.max()) ** 0.5, 5) * 2.5
    points = population_data.geometry.map(lambda x: x.centroid)
    population_data["longitude"] = points.map(lambda x: x.x)
    population_data["latitude"] = points.map(lambda x: x.y)
    population_data = pd.DataFrame(population_data.drop("geometry", axis=1)).rename(
        columns={"PCNT": "TotalPopulation", "GLEVEL": "zoom_level"}
    )

    x = real_estate_data.category.str.split(
        "_for_"
    )  # villa_for_sale so "villa" is building type and "sale" is trade type
    real_estate_data["building_type"] = x.map(lambda x: x[0])
    real_estate_data["trade_type"] = x.map(lambda x: x[1])

    housing_data["Location"] = housing_data.Location.str.split("-").map(
        lambda x: x[-1]
    )  # some cities have '-' in them like Al-Riyadh but this is not consistently present in other datasets so removing this "-"

    real_estate_data = real_estate_data.loc[real_estate_data.city.isin(city)]
    real_estate_data = gpd.GeoDataFrame(
        real_estate_data,
        geometry=gpd.points_from_xy(
            real_estate_data.longitude, real_estate_data.latitude
        ),
    )

    real_estate_data = real_estate_data.assign(
        is_villa=lambda df: df.building_type == "villa",
        is_apartment=lambda df: df.building_type == "apartment",
        is_above_average=lambda df: df.price > df.price.median(),
        selling_price=lambda df: np.where(df.trade_type == "sale", df.price, np.nan),
        renting_price=lambda df: np.where(
            df.trade_type == "rent", df.price / df.rent_period, np.nan
        ),
    )

    # Prepare census data with age calculation
    population_data = population_data[["TotalPopulation", "longitude", "latitude"]]
    population_data = gpd.GeoDataFrame(
        population_data,
        geometry=gpd.points_from_xy(
            population_data.longitude, population_data.latitude
        ),
    )

    # Prepare housing data
    housing_data = housing_data.loc[housing_data.Location == city[-1]]
    degree_split = housing_data.Degree.str.split(" ")
    housing_data = housing_data.assign(
        latitude=degree_split.map(lambda x: float(x[1])),
        longitude=degree_split.map(lambda x: float(x[0])),
    )[["latitude", "longitude", "TotalDwellings"]]
    housing_data = gpd.GeoDataFrame(
        housing_data,
        geometry=gpd.points_from_xy(housing_data.longitude, housing_data.latitude),
    )

    # Prepare restaurant data
    restaurants_data = gpd.GeoDataFrame(
        restaurants_data[["rating", "longitude", "latitude"]],
        geometry=gpd.points_from_xy(
            restaurants_data.longitude, restaurants_data.latitude
        ),
    )

    # Prepare royal houses data
    royal_houses = royal_houses[["name", "longitude", "latitude"]]
    royal_houses = gpd.GeoDataFrame(
        royal_houses,
        geometry=gpd.points_from_xy(royal_houses.longitude, royal_houses.latitude),
    )

    # Prepare luxury hotels data
    luxury_hotels = luxury_hotels[["name", "longitude", "latitude"]]
    luxury_hotels = gpd.GeoDataFrame(
        luxury_hotels,
        geometry=gpd.points_from_xy(luxury_hotels.longitude, luxury_hotels.latitude),
    )

    # Prepare gyms data
    gyms = gyms[["name", "longitude", "latitude"]]
    gyms = gpd.GeoDataFrame(
        gyms, geometry=gpd.points_from_xy(gyms.longitude, gyms.latitude)
    )

    # Prepare luxurious areas data
    luxurious_areas = luxurious_areas[["name", "longitude", "latitude"]]
    luxurious_areas = gpd.GeoDataFrame(
        luxurious_areas,
        geometry=gpd.points_from_xy(
            luxurious_areas.longitude, luxurious_areas.latitude
        ),
    )

    city_boundaries = real_estate_data.union_all().convex_hull

    real_estate_data = real_estate_data.loc[real_estate_data.within(city_boundaries)]
    population_data = population_data.loc[population_data.within(city_boundaries)]
    restaurants_data = restaurants_data.loc[restaurants_data.within(city_boundaries)]
    housing_data = housing_data.loc[housing_data.within(city_boundaries)]
    royal_houses = royal_houses.loc[royal_houses.within(city_boundaries)]
    luxurious_areas = luxurious_areas.loc[luxurious_areas.within(city_boundaries)]
    gyms = gyms.loc[gyms.within(city_boundaries)]
    luxurious_areas = luxurious_areas.loc[luxurious_areas.within(city_boundaries)]

    return (
        real_estate_data,
        housing_data,
        population_data,
        restaurants_data,
        royal_houses,
        luxury_hotels,
        gyms,
        luxurious_areas,
        grid_size,
    )


def make_grids(
    real_estate_data,
    housing_data,
    population_data,
    restaurants_data,
    royal_houses,
    luxury_hotels,
    gyms,
    luxurious_areas,
    grid_size,
):
    # Create grid cells
    minx, miny, maxx, maxy = population_data.total_bounds
    grid_cells = [
        box(x, y, x + grid_size, y + grid_size)
        for x in np.arange(minx, maxx, grid_size)
        for y in np.arange(miny, maxy, grid_size)
    ]
    grid = gpd.GeoDataFrame(geometry=grid_cells, crs=population_data.crs)

    # Perform spatial joins
    joined_population = gpd.sjoin(
        population_data, grid, how="inner", predicate="within"
    )
    joined_real_estate = gpd.sjoin(
        real_estate_data, grid, how="inner", predicate="within"
    )
    joined_restaurants = gpd.sjoin(
        restaurants_data, grid, how="inner", predicate="within"
    )
    joined_housing = gpd.sjoin(housing_data, grid, how="inner", predicate="within")
    joined_royal_houses = gpd.sjoin(royal_houses, grid, how="inner", predicate="within")
    joined_luxury_hotels = gpd.sjoin(
        luxury_hotels, grid, how="inner", predicate="within"
    )
    joined_gyms = gpd.sjoin(gyms, grid, how="inner", predicate="within")
    joined_luxurious_areas = gpd.sjoin(
        luxurious_areas, grid, how="inner", predicate="within"
    )

    # Aggregate data into the grid
    grid = pd.concat(
        [
            grid,
            joined_population.groupby("index_right")["TotalPopulation"].sum(),
            joined_real_estate.groupby("index_right")["selling_price"].mean(),
            joined_real_estate.groupby("index_right")["renting_price"].mean(),
            joined_real_estate.groupby("index_right")["is_villa"]
            .sum()
            .rename("villa_count"),
            joined_real_estate.groupby("index_right")["is_apartment"]
            .sum()
            .rename("apartment_count"),
            joined_real_estate.groupby("index_right")["is_above_average"]
            .sum()
            .rename("number_of_properties_above_average_price"),
            joined_restaurants.groupby("index_right")["rating"]
            .count()
            .rename("restaurant_count"),
            joined_housing.groupby("index_right")["TotalDwellings"].sum(),
            joined_royal_houses.groupby("index_right")["name"]
            .count()
            .rename("royal_property_count"),
            joined_luxury_hotels.groupby("index_right")["name"]
            .count()
            .rename("luxury_hotel_count"),
            joined_gyms.groupby("index_right")["name"].count().rename("gym_count"),
            joined_luxurious_areas.groupby("index_right")["name"]
            .count()
            .rename("luxury_area_count"),
        ],
        axis=1,
    )

    grid["villa_to_apartment_ratio"] = grid["villa_count"] / (
        grid["villa_count"] + grid["apartment_count"]
    )

    return grid


def get_dataset(
    db_access_key,
    city,
):

    data = load_data(
        db_access_key,
        city,
    )

    data = get_geodataframes(*data, city)

    grid = make_grids(*data)
    mask = ~grid["TotalPopulation"].isna()
    grid = grid.loc[mask]

    income_data = gpd.GeoDataFrame.from_features(
        pd.read_json("cache/Output_data_20250509_101734.json").features
    )

    income_data = gpd.sjoin(grid, income_data, how="right", predicate="within")
    income_data = (
        income_data.loc[:, grid.columns.to_list() + ["Average Male Income"]]
        .groupby("geometry", observed=False)
        .agg(
            {
                "TotalPopulation": "sum",
                "selling_price": "mean",
                "renting_price": "mean",
                "villa_count": "sum",
                "apartment_count": "sum",
                "number_of_properties_above_average_price": "sum",
                "restaurant_count": "sum",
                "TotalDwellings": "sum",
                "royal_property_count": "sum",
                "luxury_hotel_count": "sum",
                "gym_count": "sum",
                "luxury_area_count": "sum",
                "villa_to_apartment_ratio": "mean",
                "Average Male Income": "mean",
            }
        )
    )
    income_data = gpd.GeoDataFrame(income_data.reset_index()).set_crs(epsg=4326)
    income_data = income_data.rename(columns={"Average Male Income": "income"})

    mask = ~income_data.income.isna()
    income_data = income_data.loc[mask]
    city_center = income_data.union_all().convex_hull.centroid
    income_data["euc_distance_from_center"] = income_data.geometry.map(
        lambda x: x.centroid.distance(city_center)
    )
    income_data["x_distance_from_center"] = income_data.geometry.map(
        lambda x: x.centroid.x - city_center.x
    )
    income_data["y_distance_from_center"] = income_data.geometry.map(
        lambda x: x.centroid.y - city_center.y
    )

    return income_data


def train_model(income_data):

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger()

    X = income_data.drop("geometry", axis=1).sort_index(axis=1).fillna(0.0)
    y = X.pop("income")
    y = np.log1p(y)

    scaler = RobustScaler().fit(X)

    kf = RepeatedKFold(n_splits=5, n_repeats=10, random_state=42)

    train_mae_list, val_mae_list = [], []
    train_r2_list, val_r2_list = [], []

    models = []
    for fold, (train_idx, val_idx) in enumerate(kf.split(X), start=1):
        logger.info(f"Fold {fold}:")

        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        X_train_scaled = scaler.transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        dtrain = xgb.DMatrix(X_train_scaled, label=y_train)
        dval = xgb.DMatrix(X_val_scaled, label=y_val)

        params = {
            "objective": "reg:squarederror",
            "learning_rate": 0.02,
            "max_depth": 12,
            "min_child_weight": 2,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "gamma": 0.1,
            "reg_alpha": 0.1,
            "reg_lambda": 1.0,
            "tree_method": "hist",
            "eval_metric": "mae",
            "verbosity": 0,
        }

        evals = [(dtrain, "train"), (dval, "eval")]
        model = xgb.train(
            params,
            dtrain,
            num_boost_round=3000,
            evals=evals,
            early_stopping_rounds=10,
            verbose_eval=False,
        )

        y_train_pred = model.predict(dtrain)
        y_val_pred = model.predict(dval)

        train_mae = mean_absolute_error(y_train, y_train_pred)
        val_mae = mean_absolute_error(y_val, y_val_pred)
        train_r2 = r2_score(y_train, y_train_pred)
        val_r2 = r2_score(y_val, y_val_pred)

        train_mae_list.append(train_mae)
        val_mae_list.append(val_mae)
        train_r2_list.append(train_r2)
        val_r2_list.append(val_r2)

        logger.info(f"  Train MAE: {train_mae:.4f}, R²: {train_r2:.4f}")
        logger.info(f"  Val   MAE: {val_mae:.4f}, R²: {val_r2:.4f}\n")
        models.append(model)

    logger.info("=== Cross-Validation Summary ===")
    logger.info(
        f"Mean Train MAE: {np.mean(train_mae_list):.4f}, R²: {np.mean(train_r2_list):.4f}"
    )
    logger.info(
        f"Mean Val   MAE: {np.mean(val_mae_list):.4f}, R²: {np.mean(val_r2_list):.4f}"
    )
    os.makedirs("models", exist_ok=True)
    for i, model in enumerate(models):
        model.save_model(f"models/model_{i}.json")
    return models


def get_saved_models():
    """Load saved models from the 'models' directory."""
    models = []
    for path in os.listdir("models"):
        if path.endswith(".json"):
            model = xgb.Booster()
            model.load_model(os.path.join("models", path))
            models.append(model)
    return models


def predict_income(income_data, models):
    """Predict income using the loaded models."""
    X = income_data.drop("geometry", axis=1).sort_index(axis=1).fillna(0.0)
    scaler = RobustScaler().fit(X)

    X_scaled = scaler.transform(X)
    dtest = xgb.DMatrix(X_scaled)

    predictions = []
    for model in models:
        pred = model.predict(dtest)
        predictions.append(pred)

    y = np.mean(predictions, axis=0)
    return np.expm1(y)


def get_predicted_income(
    db_access_key,
    city,
    dir="",
):

    data = load_data(
        db_access_key,
        city,
    )

    data = get_geodataframes(*data, city)
    grid = make_grids(*data[:-1], 0.03408)
    mask = ~grid["TotalPopulation"].isna()
    grid = grid.loc[mask]

    income_data = grid

    city_center = income_data.union_all().convex_hull.centroid

    income_data["euc_distance_from_center"] = income_data.geometry.centroid.distance(
        city_center
    )
    income_data["x_distance_from_center"] = (
        income_data.geometry.centroid.x - city_center.x
    )
    income_data["y_distance_from_center"] = (
        income_data.geometry.centroid.y - city_center.y
    )

    models = get_saved_models()
    y = predict_income(income_data, models)
    income_data["income"] = y

    grid = make_grids(*data)
    mask = ~grid["TotalPopulation"].isna()
    grid = grid.loc[mask]

    income_data = (
        gpd.sjoin(
            grid,
            income_data[
                [
                    "geometry",
                    "income",
                    "euc_distance_from_center",
                    "x_distance_from_center",
                    "y_distance_from_center",
                ]
            ],
            how="inner",
            predicate=None,
        )
        .groupby(by="geometry", observed=False)
        .mean()
        .reset_index()
        .drop("index_right", axis=1)
    )

    income_data = gpd.GeoDataFrame(income_data)
    income_data.set_crs(epsg=4326).to_crs(epsg=4326).to_file(
        os.path.join(dir, "income_data.geojson"), driver="GeoJSON"
    )

    return income_data


def adapt(finner_data, coarser_grid):
    merged = (
        gpd.sjoin(
            finner_data.set_crs(epsg=4326).to_crs(epsg=4326),
            coarser_grid.set_crs(epsg=4326).to_crs(epsg=4326),
            how="right",
            predicate=None,
        )
        .groupby(by="geometry", observed=False)
        .mean()
        .reset_index()
    )

    merged = gpd.GeoDataFrame(merged)[
        [
            "geometry",
            "income",
            "euc_distance_from_center",
            "x_distance_from_center",
            "y_distance_from_center",
        ]
    ]

    merged = gpd.sjoin(
        coarser_grid.set_crs(epsg=4326).to_crs(epsg=4326),
        merged,
        how="inner",
        predicate="within",
    ).drop("index_right", axis=1)

    return merged

