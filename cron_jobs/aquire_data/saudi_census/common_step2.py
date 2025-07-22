import os
import json
import random
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from scipy import ndimage
from sklearn.cluster import DBSCAN
from geopy.distance import geodesic
import geopandas as gpd


def update_keys(data, column_mapping):
    """Update keys in the data based on the provided column mapping."""
    for feature in data.get("features", []):
        if "properties" in feature:
            updated_props = {}
            for k, v in feature["properties"].items():
                # Use .upper() on the original key for case-insensitive matching with column_mapping
                updated_key = column_mapping.get(k.upper(), k)
                updated_props[updated_key] = v
            feature["properties"] = updated_props
    return data


def process_json_files(
    folder_path, column_mapping, primary_density_key, fallback_density_key=None
):
    """
    Update keys in ALL JSON files and calculate normalized density based on available data.
    Normalization is done per zoom level (0-100 scale based on min/max within each level).

    Args:
        folder_path (str): Path to the folder containing JSON files
        column_mapping (dict): Dictionary mapping original keys to new keys (keys should be uppercase)
        primary_density_key (str): The primary key to use for density calculation (after mapping)
        fallback_density_key (str, optional): Fallback key if primary key has no valid values
    """
    if fallback_density_key is None:
        fallback_density_key = primary_density_key

    # First pass: collect all data and organize by zoom level
    files_data = {}
    zoom_level_values = defaultdict(list)  # zoom_level -> list of values

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith("json"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    updated_data = update_keys(data, column_mapping)

                    # Determine which key to use for density calculation
                    key_for_density_calculation = primary_density_key
                    features_list = updated_data.get("features", [])

                    if features_list:
                        # Sample to check if primary key has valid values
                        sample_size = min(50, len(features_list))
                        sampled_features = random.sample(
                            features_list, k=sample_size
                        )
                        has_primary_key = any(
                            feature.get("properties", {}).get(
                                primary_density_key
                            )
                            is not None
                            for feature in sampled_features
                        )

                        if (
                            not has_primary_key
                            and fallback_density_key != primary_density_key
                        ):
                            key_for_density_calculation = fallback_density_key
                            print(
                                f"Info: In '{file_path}', using fallback key '{fallback_density_key}'."
                            )

                    # Store file data for second pass
                    files_data[file_path] = {
                        "data": updated_data,
                        "density_key": key_for_density_calculation,
                    }

                    # Collect values by zoom level
                    for feature in features_list:
                        properties = feature.get("properties", {})
                        zoom_level = properties.get("Level")
                        density_value_str = properties.get(
                            key_for_density_calculation
                        )

                        if (
                            zoom_level is not None
                            and density_value_str is not None
                        ):
                            try:
                                density_value = float(density_value_str)
                                zoom_level_values[zoom_level].append(
                                    density_value
                                )
                            except ValueError:
                                pass  # Skip invalid values

                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Calculate min/max for each zoom level
    zoom_level_ranges = {}
    for zoom_level, values in zoom_level_values.items():
        if values:
            zoom_level_ranges[zoom_level] = {
                "min": min(values),
                "max": max(values),
            }
            print(
                f"Zoom Level {zoom_level}: min={zoom_level_ranges[zoom_level]['min']}, max={zoom_level_ranges[zoom_level]['max']}, count={len(values)}"
            )

    # Second pass: normalize and write files
    for file_path, file_info in files_data.items():
        try:
            updated_data = file_info["data"]
            key_for_density_calculation = file_info["density_key"]
            features_list = updated_data.get("features", [])

            if features_list:
                # Normalize density for each feature based on its zoom level
                for feature in features_list:
                    properties = feature.get("properties", {})
                    zoom_level = properties.get("Level")
                    current_value_str = properties.get(
                        key_for_density_calculation
                    )
                    normalized_density_value = 0.0

                    if (
                        zoom_level is not None
                        and current_value_str is not None
                        and zoom_level in zoom_level_ranges
                    ):

                        try:
                            current_value_float = float(current_value_str)
                            min_val = zoom_level_ranges[zoom_level]["min"]
                            max_val = zoom_level_ranges[zoom_level]["max"]

                            if max_val == min_val:
                                # All values at this zoom level are the same
                                normalized_density_value = 0.0  # Middle value
                            else:
                                # Normalize to 0-100 scale
                                normalized_density_value = (
                                    (current_value_float - min_val)
                                    / (max_val - min_val)
                                ) * 100

                            properties["density"] = round(
                                normalized_density_value, 4
                            )
                        except ValueError:
                            properties["density"] = 0.0
                    else:
                        properties["density"] = 0.0

                    feature["properties"] = properties

                print(
                    f"Processed: {file_path}. Keys updated. Density normalized by zoom level using '{key_for_density_calculation}'."
                )
            else:
                print(
                    f"Info: No features found in {file_path}. Only top-level keys updated."
                )

            # Write back to the SAME file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


def make_json_serializable(obj):
    """Convert numpy types and other non-serializable objects to JSON-compatible types."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif obj is None:
        return None
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {
            key: make_json_serializable(value) for key, value in obj.items()
        }
    else:
        return obj


def clean_feature_properties(feature):
    """Clean feature properties to ensure JSON serialization."""
    cleaned_feature = feature.copy()

    # Clean properties
    if "properties" in cleaned_feature:
        cleaned_props = {}
        for key, value in cleaned_feature["properties"].items():
            cleaned_props[key] = make_json_serializable(value)
        cleaned_feature["properties"] = cleaned_props

    return cleaned_feature


# City bounding boxes (50km square around each city center)
CITY_BOUNDING_BOXES = {
    "Riyadh": {
        "center": (46.6753, 24.7136),  # Riyadh coordinates
        "bounds": {
            "min_lon": 46.2253,
            "max_lon": 47.1253,  # ~50km wide
            "min_lat": 24.2636,
            "max_lat": 25.1636,  # ~50km tall
        },
    },
    "Mecca": {
        "center": (39.8579, 21.3891),  # Mecca coordinates
        "bounds": {
            "min_lon": 39.4079,
            "max_lon": 40.3079,
            "min_lat": 20.9391,
            "max_lat": 21.8391,
        },
    },
    "Jeddah": {
        "center": (39.1948, 21.4858),  # Jeddah coordinates
        "bounds": {
            "min_lon": 38.7448,
            "max_lon": 39.6448,
            "min_lat": 21.0358,
            "max_lat": 21.9358,
        },
    },
}


def extract_coordinates_from_geometry(feature):
    """
    Extract centroid coordinates from polygon geometry.
    """
    geometry = feature.get("geometry", {})

    if geometry.get("type") == "Polygon":
        # Get polygon coordinates
        coordinates = geometry.get("coordinates", [])
        if coordinates and len(coordinates) > 0:
            # Get the exterior ring (first array)
            exterior_ring = coordinates[0]

            # Calculate centroid
            lons = [coord[0] for coord in exterior_ring]
            lats = [coord[1] for coord in exterior_ring]

            centroid_lon = sum(lons) / len(lons)
            centroid_lat = sum(lats) / len(lats)

            return centroid_lat, centroid_lon

    return None, None


def filter_features_by_city_bounds(features, city_bounds):
    """Updated to extract coordinates from geometry."""
    filtered_features = []

    for feature in features:
        # Extract coordinates from geometry instead of properties
        centroid_lat, centroid_lon = extract_coordinates_from_geometry(feature)

        if centroid_lat is None or centroid_lon is None:
            continue

        # Check if centroid is within city bounds
        if (
            city_bounds["min_lon"] <= centroid_lon <= city_bounds["max_lon"]
            and city_bounds["min_lat"] <= centroid_lat <= city_bounds["max_lat"]
        ):

            # Add calculated coordinates to properties for later use
            feature["properties"]["calculated_latitude"] = centroid_lat
            feature["properties"]["calculated_longitude"] = centroid_lon
            filtered_features.append(feature)

    return filtered_features


def identify_urban_population_centers(
    features, max_centers=4, min_distance_km=3
):
    """
    Identify population centers focusing on urban density patterns.
    Returns Point geometries instead of Polygons.
    """
    print(f"\n=== URBAN POPULATION CENTER IDENTIFICATION ===")
    print(
        f"Input: {len(features)} features, max_centers={max_centers}, min_distance_km={min_distance_km}"
    )

    if len(features) == 0:
        return []

    # ... (all the same logic for finding centers) ...

    # Step 1-5: Same as before (finding valid features, clustering, etc.)
    valid_features = []
    for i, feature in enumerate(features):
        props = feature.get("properties", {})

        centroid_lat = props.get("calculated_latitude")
        centroid_lon = props.get("calculated_longitude")

        if centroid_lat is None or centroid_lon is None:
            centroid_lat, centroid_lon = extract_coordinates_from_geometry(
                feature
            )

        if centroid_lat is None or centroid_lon is None:
            continue

        population_count = props.get("Population_Count", 0)
        population_density = props.get("Population_Density_KM2", 0)

        try:
            lat_float = float(centroid_lat)
            lon_float = float(centroid_lon)
            pop_float = float(population_count) if population_count else 0
            density_float = (
                float(population_density) if population_density else 0
            )
        except (ValueError, TypeError):
            continue

        if pop_float <= 10 or density_float <= 100:
            continue

        urban_score = density_float * (1 + np.log(1 + pop_float))

        valid_features.append(
            {
                "feature": feature,
                "index": int(i),
                "lon": float(lon_float),
                "lat": float(lat_float),
                "population": float(pop_float),
                "density": float(density_float),
                "urban_score": float(urban_score),
            }
        )

    print(f"Valid urban features: {len(valid_features)}")

    if len(valid_features) == 0:
        return []

    # Steps 2-5: Same clustering logic as before...
    densities = [f["density"] for f in valid_features]
    high_density_threshold = float(np.percentile(densities, 85))

    high_density_candidates = [
        f for f in valid_features if f["density"] >= high_density_threshold
    ]

    if len(high_density_candidates) < max_centers:
        moderate_density_threshold = float(np.percentile(densities, 70))
        high_density_candidates = [
            f
            for f in valid_features
            if f["density"] >= moderate_density_threshold
        ]

    if len(high_density_candidates) == 0:
        high_density_candidates = valid_features

    # DBSCAN clustering (same logic)
    if len(high_density_candidates) > 1:
        coords = np.array(
            [[f["lat"], f["lon"]] for f in high_density_candidates]
        )

        from sklearn.cluster import DBSCAN

        dbscan = DBSCAN(eps=0.02, min_samples=3)
        cluster_labels = dbscan.fit_predict(coords)

        clusters = {}
        for i, label in enumerate(cluster_labels):
            label_int = int(label)
            if label_int not in clusters:
                clusters[label_int] = []
            clusters[label_int].append(high_density_candidates[i])

        cluster_centers = []
        for cluster_id, cluster_members in clusters.items():
            if cluster_id == -1:
                continue

            best_in_cluster = max(
                cluster_members, key=lambda x: x["urban_score"]
            )
            best_in_cluster["cluster_id"] = int(cluster_id)
            best_in_cluster["cluster_size"] = len(cluster_members)
            cluster_centers.append(best_in_cluster)

        # Handle noise points (same logic)
        noise_points = clusters.get(-1, [])
        if len(cluster_centers) < max_centers and noise_points:
            noise_points.sort(key=lambda x: x["urban_score"], reverse=True)
            needed = max_centers - len(cluster_centers)

            for noise_point in noise_points[:needed]:
                noise_coord = (noise_point["lat"], noise_point["lon"])
                too_close = False

                for center in cluster_centers:
                    center_coord = (center["lat"], center["lon"])
                    if (
                        geodesic(noise_coord, center_coord).kilometers
                        < min_distance_km
                    ):
                        too_close = True
                        break

                if not too_close:
                    noise_point["cluster_id"] = "isolated"
                    noise_point["cluster_size"] = 1
                    cluster_centers.append(noise_point)

        final_centers = cluster_centers[:max_centers]

    else:
        # Fallback method (same logic)
        sorted_candidates = sorted(
            high_density_candidates,
            key=lambda x: x["urban_score"],
            reverse=True,
        )

        final_centers = []
        for candidate in sorted_candidates:
            if len(final_centers) >= max_centers:
                break

            candidate_coord = (candidate["lat"], candidate["lon"])
            too_close = False

            for center in final_centers:
                center_coord = (center["lat"], center["lon"])
                if (
                    geodesic(candidate_coord, center_coord).kilometers
                    < min_distance_km
                ):
                    too_close = True
                    break

            if not too_close:
                candidate["cluster_id"] = len(final_centers)
                candidate["cluster_size"] = 1
                final_centers.append(candidate)

    # Step 6: Create POINT features instead of keeping polygon geometry
    result_features = []
    for i, center in enumerate(final_centers):
        # Get original properties from the source feature
        original_props = center["feature"].get("properties", {}).copy()

        # Add/update properties with center-specific data
        original_props["calculated_latitude"] = float(center["lat"])
        original_props["calculated_longitude"] = float(center["lon"])
        original_props["population_center_rank"] = int(i + 1)
        original_props["urban_score"] = round(float(center["urban_score"]), 2)
        original_props["cluster_id"] = center.get("cluster_id", int(i))
        original_props["cluster_size"] = int(center.get("cluster_size", 1))
        original_props["is_population_center"] = True
        original_props["selection_method"] = "urban_density_clustering"

        # Create new Point feature
        point_feature = {
            "type": "Feature",
            "id": original_props.get("Main_ID", f"center_{i}"),
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(center["lon"]),
                    float(center["lat"]),
                ],  # [longitude, latitude]
            },
            "properties": original_props,
        }

        # Clean the feature for JSON serialization
        cleaned_feature = clean_feature_properties(point_feature)
        result_features.append(cleaned_feature)

        print(
            f"  Final center {i+1}: Point({center['lon']:.4f}, {center['lat']:.4f}) "
            f"pop={center['population']:.0f}, density={center['density']:.0f}"
        )

    print(
        f"Selected {len(result_features)} urban population centers as Point geometries"
    )
    return result_features


def create_population_centers_geojson_urban(folder_path):
    """Urban-focused population center identification with robust file writing."""
    print("Starting URBAN-FOCUSED population centers identification...")

    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            if dir_name.startswith("v") and dir_name[1:].isdigit():
                zoom_level = dir_name
                zoom_path = os.path.join(root, dir_name)
                geojson_path = os.path.join(zoom_path, "all_features.geojson")

                if not os.path.exists(geojson_path):
                    continue

                print(f"\nProcessing zoom level {zoom_level}...")

                try:
                    with open(geojson_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    features = data.get("features", [])
                    all_population_centers = []
                    city_stats = {}

                    for city_name, city_info in CITY_BOUNDING_BOXES.items():
                        print(f"  Processing {city_name}...")

                        city_features = filter_features_by_city_bounds(
                            features, city_info["bounds"]
                        )

                        print(
                            f"    Found {len(city_features)} features in {city_name}"
                        )

                        if len(city_features) == 0:
                            city_stats[city_name] = {"centers": 0}
                            continue

                        centers = identify_urban_population_centers(
                            city_features, max_centers=4, min_distance_km=3
                        )

                        # Add city metadata and ensure clean data
                        for center in centers:
                            center["properties"]["city"] = str(city_name)
                            center["properties"]["zoom_level"] = str(zoom_level)

                        all_population_centers.extend(centers)
                        city_stats[city_name] = {"centers": len(centers)}

                        print(
                            f"    Selected {len(centers)} urban centers for {city_name}"
                        )

                    # Create output data with clean, JSON-serializable values
                    output_data = {
                        "type": "FeatureCollection",
                        "metadata": {
                            "zoom_level": str(zoom_level),
                            "algorithm": "urban_density_clustering",
                            "min_separation_km": 3,
                            "density_threshold": "85th_percentile",
                            "clustering_method": "DBSCAN",
                            "focus": "urban_core_over_geographic_distribution",
                            "total_centers": len(all_population_centers),
                            "city_statistics": city_stats,
                        },
                        "features": all_population_centers,
                    }

                    # Clean the entire output data
                    clean_output_data = make_json_serializable(output_data)

                    # Save with error handling
                    output_path = os.path.join(
                        zoom_path, "population_centers.geojson"
                    )

                    try:
                        with open(output_path, "w", encoding="utf-8") as f:
                            json.dump(
                                clean_output_data,
                                f,
                                ensure_ascii=False,
                                indent=2,
                            )

                        print(
                            f"  Successfully created {output_path} with {len(all_population_centers)} urban centers"
                        )

                        # Verify the file was written completely
                        with open(output_path, "r", encoding="utf-8") as f:
                            verification = json.load(f)
                            if len(verification.get("features", [])) == len(
                                all_population_centers
                            ):
                                print(
                                    f"  File verification successful: {len(verification['features'])} features written"
                                )
                            else:
                                print(f"  WARNING: File verification failed!")

                    except Exception as write_error:
                        print(
                            f"  ERROR writing file {output_path}: {write_error}"
                        )

                        # Try writing a simpler version for debugging
                        debug_output = {
                            "type": "FeatureCollection",
                            "features": all_population_centers[
                                :1
                            ],  # Just first feature
                            "debug": "partial_write_test",
                        }
                        debug_path = os.path.join(
                            zoom_path, "debug_centers.geojson"
                        )
                        with open(debug_path, "w", encoding="utf-8") as f:
                            json.dump(
                                make_json_serializable(debug_output),
                                f,
                                indent=2,
                            )
                        print(f"  Created debug file: {debug_path}")

                except Exception as e:
                    print(f"Error processing {zoom_level}: {e}")
                    import traceback

                    traceback.print_exc()
