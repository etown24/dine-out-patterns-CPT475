import os, glob
import pandas as pd

# does not work 
# trying to get all user location files and combine them into one csv
# needs more work
def combine_user_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join("..", "data", "users","locations")
    print(f"Looking for files in: {os.path.abspath(data_folder)}")

    csv_files = glob.glob(os.path.join(data_folder, "*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found in users folder!")

    all_data = []
    for f in csv_files:
        df = pd.read_csv(f)
        df["source_file"] = os.path.basename(f)
        all_data.append(df)

    combined = pd.concat(all_data, ignore_index=True)
    output_path = os.path.join("..", "data", "combined_users.csv")
    combined.to_csv(output_path, index=False)
    print(f"Combined user data saved to: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    combine_user_files()
