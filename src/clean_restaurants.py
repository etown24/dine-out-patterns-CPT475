import pandas as pd

# Function to clean restaurant data 
def clean_restaurant_data(input_path="data/restaurants.csv", output_path="data/restaurants_clean.csv"):
    print("Loading restaurant data...")
    df = pd.read_csv(input_path, low_memory=False)

    # Keep only relevant columns
    keep_cols = [
        "COMPANY NAME",
        "CITY",
        "STATE",
        "LATITUDE",
        "LONGITUDE",
        "PRIMARY NAICS DESCRIPTION",
        "FastFood"
    ]

    df = df[keep_cols].rename(columns={
        "COMPANY NAME": "name",
        "CITY": "city",
        "STATE": "state",
        "LATITUDE": "latitude",
        "LONGITUDE": "longitude",
        "PRIMARY NAICS DESCRIPTION": "category",
        "FastFood": "fast_food"
    })

    # Drop rows missing coordinates
    df = df.dropna(subset=["latitude", "longitude"])

    # Convert integers into decimal degrees
    df["latitude"] = df["latitude"].astype(float) / 1_000_000
    df["longitude"] = df["longitude"].astype(float) / 1_000_000

    # Make longitude negative for USA (Western Hemisphere)
    # Your dataset stores positive longitudes, but actual WA = -122.x
    df["longitude"] = -df["longitude"]

    # Keep only valid geographic ranges
    df = df[
        (df["latitude"].between(-90, 90)) &
        (df["longitude"].between(-180, 180))
    ]

    df.to_csv(output_path, index=False)
    print(f"Cleaned restaurant data saved to {output_path}")
    print(f"Total restaurants: {len(df)}")

if __name__ == "__main__":
    clean_restaurant_data()
