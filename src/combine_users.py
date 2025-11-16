import os
import glob
import pandas as pd

def combine_user_files():
    # Path to directory containing *this file*
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the data folder
    data_folder = os.path.join(script_dir, "..", "data", "users", "locations")

    print(f"Looking for files in: {os.path.abspath(data_folder)}")

    # Match all location CSV filenames
    csv_files = glob.glob(os.path.join(data_folder, "locations_*.csv"))

    if not csv_files:
        raise FileNotFoundError("No CSV files found in data folder!")

    all_data = []

    for f in csv_files:
        print(f"Reading: {f}")
        df = pd.read_csv(f)
        df["source_file"] = os.path.basename(f)
        all_data.append(df)

    combined = pd.concat(all_data, ignore_index=True)

    output_path = os.path.join(script_dir, "..", "data", "combined_users.csv")
    combined.to_csv(output_path, index=False)

    print(f"Combined CSV saved to: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    combine_user_files()
