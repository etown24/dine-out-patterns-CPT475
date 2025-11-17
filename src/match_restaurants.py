import pandas as pd
import os
import numpy as np
from scipy.spatial import cKDTree
from geopy.distance import geodesic

def match_user_visits(radius_meters=50):

    # Fix the working directory issue
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))

    user_path = os.path.join(DATA_DIR, "combined_users.csv")
    rest_path = os.path.join(DATA_DIR, "restaurants_clean.csv")
    output_path = os.path.join(DATA_DIR, "matched_visits.csv")

    print("Loading users from:", user_path)
    print("Loading restaurants from:", rest_path)

    # Load data
    users = pd.read_csv(user_path)
    rests = pd.read_csv(rest_path)

    # Standardize column names
    users.columns = users.columns.str.lower()
    rests.columns = rests.columns.str.lower()

    # Check required fields
    for col in ["client_id", "datetime", "latitude", "longitude"]:
        if col not in users.columns:
            raise ValueError(f"Missing user column: {col}")

    for col in ["name", "city", "latitude", "longitude"]:
        if col not in rests.columns:
            raise ValueError(f"Missing restaurant column: {col}")

    # Build KDTree from restaurant coordinates (in radians for haversine)
    print("Building spatial index...")
    rest_coords_rad = np.radians(rests[["latitude", "longitude"]].values)
    tree = cKDTree(rest_coords_rad)

    # Convert radius to radians (Earth radius ≈ 6371km)
    radius_rad = radius_meters / 6371000

    matches = []
    total_users = len(users)

    print(f"Matching {total_users} users to restaurants within {radius_meters}m...")
    for i, u in users.iterrows():
        if i % 1000 == 0:
            print(f"Processed {i}/{total_users}")

        user_loc_rad = np.radians([u["latitude"], u["longitude"]])

        # Query KDTree for nearby restaurants
        nearby_indices = tree.query_ball_point(user_loc_rad, radius_rad)

        for rest_idx in nearby_indices:
            r = rests.iloc[rest_idx]
            user_loc = (u["latitude"], u["longitude"])
            rest_loc = (r["latitude"], r["longitude"])
            dist = geodesic(user_loc, rest_loc).meters

            if dist <= radius_meters:
                matches.append({
                    "client_id": u["client_id"],
                    "datetime": u["datetime"],
                    "restaurant": r["name"],
                    "city": r["city"],
                    "distance_m": round(dist, 1)
                })

    matched_df = pd.DataFrame(matches)
    matched_df.to_csv(output_path, index=False)

    print("\nDone!")
    print(f"Saved {len(matched_df)} matches to {output_path}")


if __name__ == "__main__":
    match_user_visits()
