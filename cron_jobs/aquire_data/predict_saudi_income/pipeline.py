import os
import numpy as np
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry import box
from scipy.spatial import cKDTree

import logging
from sklearn.model_selection import RepeatedKFold
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_absolute_error, r2_score

import os
import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedKFold
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import (
    RandomForestRegressor,
    StackingRegressor,

)
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
import joblib


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

    dental_clinic = (
        gpd.read_file("cache/geojson_saudi_dental_clinic_20250512_110022.geojson")
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )
    electrician = (
        gpd.read_file("cache/geojson_saudi_electrician_20250512_122401.geojson")
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )
    plumber = (
        gpd.read_file("cache/geojson_saudi_plumber_20250512_123014.geojson")
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )
    police = (
        gpd.read_file("cache/geojson_saudi_police_20250512_103953.geojson")
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )
    embassy = (
        gpd.read_file("cache/geojson_saudi_embassy_20250512_102151.geojson")
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )
    university = (
        gpd.read_file("cache/geojson_saudi_university_20250512_011237.geojson")
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    return (
        real_estate_data,
        housing_data,
        population_data,
        restaurants_data,
        royal_houses,
        luxury_hotels,
        gyms,
        luxurious_areas,
        dental_clinic,
        electrician,
        plumber,
        police,
        embassy,
        university,
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
    dental_clinic,
    electrician,
    plumber,
    police,
    embassy,
    university,
    city,
    is_training=True
):
    if is_training:
        grid_size = 0.01
    else:
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
    real_estate_data = (
        gpd.GeoDataFrame(
            real_estate_data,
            geometry=gpd.points_from_xy(
                real_estate_data.longitude, real_estate_data.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
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
    population_data = (
        gpd.GeoDataFrame(
            population_data,
            geometry=gpd.points_from_xy(
                population_data.longitude, population_data.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Prepare housing data
    housing_data = housing_data.loc[housing_data.Location == city[-1]]
    degree_split = housing_data.Degree.str.split(" ")
    housing_data = housing_data.assign(
        latitude=degree_split.map(lambda x: float(x[1])),
        longitude=degree_split.map(lambda x: float(x[0])),
    )[["latitude", "longitude", "TotalDwellings"]]
    housing_data = (
        gpd.GeoDataFrame(
            housing_data,
            geometry=gpd.points_from_xy(housing_data.longitude, housing_data.latitude),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Prepare restaurant data
    restaurants_data = (
        gpd.GeoDataFrame(
            restaurants_data[["rating", "longitude", "latitude"]],
            geometry=gpd.points_from_xy(
                restaurants_data.longitude, restaurants_data.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Prepare royal houses data
    royal_houses = royal_houses[["name", "longitude", "latitude"]]
    royal_houses = (
        gpd.GeoDataFrame(
            royal_houses,
            geometry=gpd.points_from_xy(royal_houses.longitude, royal_houses.latitude),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Prepare luxury hotels data
    luxury_hotels = luxury_hotels[["name", "longitude", "latitude"]]
    luxury_hotels = (
        gpd.GeoDataFrame(
            luxury_hotels,
            geometry=gpd.points_from_xy(
                luxury_hotels.longitude, luxury_hotels.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Prepare gyms data
    gyms = gyms[["name", "longitude", "latitude"]]
    gyms = (
        gpd.GeoDataFrame(
            gyms, geometry=gpd.points_from_xy(gyms.longitude, gyms.latitude)
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
    )

    # Prepare luxurious areas data
    luxurious_areas = luxurious_areas[["name", "longitude", "latitude"]]
    luxurious_areas = (
        gpd.GeoDataFrame(
            luxurious_areas,
            geometry=gpd.points_from_xy(
                luxurious_areas.longitude, luxurious_areas.latitude
            ),
        )
        .set_crs(epsg=4326)
        .to_crs(epsg=4326)
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
    dental_clinic = dental_clinic.loc[dental_clinic.within(city_boundaries)]
    electrician = electrician.loc[electrician.within(city_boundaries)]
    plumber = plumber.loc[plumber.within(city_boundaries)]
    police = police.loc[police.within(city_boundaries)]
    embassy = embassy.loc[embassy.within(city_boundaries)]
    university = university.loc[university.within(city_boundaries)]

    return (
        real_estate_data,
        housing_data,
        population_data,
        restaurants_data,
        royal_houses,
        luxury_hotels,
        gyms,
        luxurious_areas,
        dental_clinic,
        electrician,
        plumber,
        police,
        embassy,
        university,
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
    dental_clinic,
    electrician,
    plumber,
    police,
    embassy,
    university,
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

    joined_dental_clinic = gpd.sjoin(
        dental_clinic, grid, how="inner", predicate="within"
    )
    joined_electrician = gpd.sjoin(electrician, grid, how="inner", predicate="within")
    joined_plumber = gpd.sjoin(plumber, grid, how="inner", predicate="within")
    joined_police = gpd.sjoin(police, grid, how="inner", predicate="within")
    joined_embassy = gpd.sjoin(embassy, grid, how="inner", predicate="within")
    joined_university = gpd.sjoin(university, grid, how="inner", predicate="within")

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
            joined_dental_clinic.groupby("index_right")["name"]
            .count()
            .rename("joined_dental_clinic"),
            joined_electrician.groupby("index_right")["name"]
            .count()
            .rename("joined_electrician"),
            joined_plumber.groupby("index_right")["name"]
            .count()
            .rename("joined_plumber"),
            joined_police.groupby("index_right")["name"]
            .count()
            .rename("joined_police"),
            joined_embassy.groupby("index_right")["name"]
            .count()
            .rename("joined_embassy"),
            joined_university.groupby("index_right")["name"]
            .count()
            .rename("joined_university"),
        ],
        axis=1,
    )

    grid["villa_to_apartment_ratio"] = grid["villa_count"] / (
        grid["villa_count"] + grid["apartment_count"]
    )

    return grid


def idw_interpolation(xy_points, values, xy_targets, k=6, power=2):
    tree = cKDTree(xy_points)
    dists, idxs = tree.query(xy_targets, k=k)
    dists = np.maximum(dists, 1e-12)  # avoid division by zero
    weights = 1 / (dists**power)
    weights /= weights.sum(axis=1, keepdims=True)
    interpolated = np.sum(values[idxs] * weights, axis=1)
    return interpolated


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
        pd.read_json("cache/ignore_zad_Output_data.json").features
    )

    bounds = grid[["geometry", "TotalPopulation"]].dropna().union_all().convex_hull
    mask = income_data[["geometry", "Average Male Income"]].within(bounds)
    income_data = income_data.loc[mask][["geometry", "Average Male Income"]]

    bounds = income_data.union_all().convex_hull
    mask = grid.within(bounds)
    grid = grid.loc[mask]

    income_data = income_data[["geometry", "Average Male Income"]].assign(
        geometry=lambda x: x.geometry.centroid
    )
    mask = ~grid[["geometry", "TotalPopulation"]].isna().any(axis=1)
    grid = grid.loc[mask]

    xy_points = np.array([(point.x, point.y) for point in income_data.geometry])
    values = income_data["Average Male Income"].values
    xy_targets = np.array(
        [(poly.centroid.x, poly.centroid.y) for poly in grid.geometry]
    )
    interpolated_values = idw_interpolation(xy_points, values, xy_targets, k=6, power=2)
    grid["income"] = interpolated_values

    income_data = gpd.GeoDataFrame(grid.reset_index(drop=True)).set_crs(epsg=4326)

    mask = ~income_data.income.isna()
    income_data = income_data.loc[mask]
    city_center = income_data.union_all().convex_hull.centroid
    income_data["euc_distance_from_center"] = income_data.geometry.map(
        lambda x: x.centroid.distance(city_center)
    )

    return income_data


def train_model(income_data):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger()
    X = income_data.drop("geometry", axis=1).sort_index(axis=1).fillna(0.0)
    y = X.pop("income").copy()
    mask = y > 0
    y.loc[~mask] = y.loc[mask].mean()
    # y = np.log1p(y)
    scaler = RobustScaler().fit(X.values)

    kf = RepeatedKFold(n_splits=5, n_repeats=10, random_state=42)
    n_estimators = 350
    depth = 8
    lr = 0.05

    base_learners = {
        "xgb": XGBRegressor(
            objective="reg:squarederror",
            learning_rate=lr,
            max_depth=depth,
            n_estimators=n_estimators,
            subsample=0.85,
            colsample_bytree=0.85,
            gamma=0.25,
            reg_alpha=0.35,
            reg_lambda=0.65,
            tree_method="hist",
            verbosity=0,
        ),
        "cat": CatBoostRegressor(
            iterations=n_estimators,
            learning_rate=lr,
            depth=depth,
            l2_leaf_reg=6.5,
            subsample=0.85,
            verbose=0,
            random_seed=42,
        ),
        "rf": RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=None,
            min_samples_split=3,
            bootstrap=True,
            random_state=42,
        ),
    }

    metrics = {
        m: {"train_mae": [], "val_mae": [], "train_r2": [], "val_r2": []}
        for m in base_learners
    }

    os.makedirs("models", exist_ok=True)

    for fold, (train_idx, val_idx) in enumerate(kf.split(X), start=1):
        logger.info(f"=== Fold {fold} ===")
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        X_train_s = scaler.transform(X_train.values)
        X_val_s = scaler.transform(X_val.values)

        for name, model in base_learners.items():
            mdl = model.__class__(**model.get_params())
            mdl.fit(X_train_s, y_train.values)
            y_train_pred = mdl.predict(X_train_s)
            y_val_pred = mdl.predict(X_val_s)

            t_mae = mean_absolute_error(y_train, y_train_pred)
            v_mae = mean_absolute_error(y_val, y_val_pred)
            t_r2 = r2_score(y_train, y_train_pred)
            v_r2 = r2_score(y_val, y_val_pred)

            metrics[name]["train_mae"].append(t_mae)
            metrics[name]["val_mae"].append(v_mae)
            metrics[name]["train_r2"].append(t_r2)
            metrics[name]["val_r2"].append(v_r2)

            logger.info(
                f"{name.upper():<5}  Train MAE: {t_mae:.4f}, R2: {t_r2:.4f} | "
                f"Val MAE: {v_mae:.4f}, R2: {v_r2:.4f}"
            )
            joblib.dump(mdl, f"models/{name}_fold{fold}.joblib")
        logger.info("")

    logger.info("=== CV Summary ===")
    for name in base_learners:
        logger.info(
            f"{name.upper():<5} Mean Train MAE: {np.mean(metrics[name]['train_mae']):.4f}, "
            f"Mean Val MAE: {np.mean(metrics[name]['val_mae']):.4f}, "
            f"Mean Val R2: {np.mean(metrics[name]['val_r2']):.4f}"
        )

    logger.info("Training stacking ensemble on full dataset...")
    X_full_s = scaler.transform(X)
    estimators = [(name, base_learners[name]) for name in base_learners]
    stack = StackingRegressor(
        estimators=estimators,
        final_estimator=LinearRegression(),
        passthrough=True,
        n_jobs=-1,
    )
    stack.fit(X_full_s, y)
    joblib.dump(stack, "models/stacking_ensemble.joblib")

    logger.info("Ensemble saved as models/stacking_ensemble.joblib")
    return metrics, base_learners, stack


def get_saved_models():
    """Load saved models from the 'models' directory."""
    models = []
    for path in os.listdir("models"):
        if path.endswith(".joblib"):
            with open(os.path.join("models", path), "rb") as f:
                model = joblib.load(f)
                models.append(model)
    return models


def predict_income(income_data, models):
    """Predict income using the loaded models."""
    X = income_data.drop("geometry", axis=1).sort_index(axis=1).fillna(0.0)
    scaler = RobustScaler().fit(X)

    X_scaled = scaler.transform(X.values)

    predictions = []
    for model in models:
        pred = model.predict(X_scaled)
        predictions.append(pred.squeeze())

    y = np.mean(np.stack(predictions, axis=0), axis=0)
    return y #np.expm1(y)


def get_predicted_income(
    db_access_key,
    city,
    dir="",
):

    data_ = load_data(
        db_access_key,
        city,
    )

    data = get_geodataframes(*data_, city)
    grid = make_grids(*data)
    mask = ~grid["TotalPopulation"].isna()
    grid = grid.loc[mask]

    income_data = grid.set_crs(epsg=4326).to_crs(epsg=4326)
    city_center = income_data.union_all().convex_hull.centroid
    income_data["euc_distance_from_center"] = income_data.geometry.centroid.distance(
        city_center
    )

    models = get_saved_models()
    y = predict_income(income_data, models)
    income_data["income"] = y

    data = get_geodataframes(*data_, city, is_training=False)
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
