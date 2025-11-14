import pandas as pd
import os
from geopy.distance import geodesic

# needs combine users to work so it can compile 
# trying to match user visits to restaurants 
def match_user_visits(radius_meters=50):
    user_path = os.path.join("..", "data", "combined_users.csv")
    rest_path = os.path.join("..", "data", "clean_restaurants.csv")
    output_path = os.path.join("..", "data", "matched_visits.csv")

    users = pd.read_csv(user_path)
    rests = pd.read_csv(rest_path)

    matches = []
    for _, u in users.iterrows():
        user_loc = (u["latitude"], u["longitude"])
        for _, r in rests.iterrows():
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
    print(f"Saved {len(matched_df)} matches to {output_path}")

if __name__ == "__main__":
    match_user_visits()
