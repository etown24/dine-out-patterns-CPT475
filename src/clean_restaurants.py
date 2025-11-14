import pandas as pd

# Function to clean restaurant data 
# works
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

    df = df.dropna(subset=["latitude", "longitude"])

    df.to_csv(output_path, index=False)
    print(f"Cleaned restaurant data saved to {output_path}")
    print(f"Total restaurants: {len(df)}")

if __name__ == "__main__":
    clean_restaurant_data()
