import pandas as pd
import os

# analyze dining patterns from matched visits
def analyze_patterns():
    # Resolve paths relative to this script so running from anywhere works
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(base_dir, ".."))
    data_path = os.path.join(project_dir, "data", "matched_visits.csv")
    output_path = os.path.join(project_dir, "results", "summaries", "time_distribution.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"Required data file not found: {data_path}\n"
            "Run `match_restaurants.py` to generate `matched_visits.csv` before analyzing."
        )

    df = pd.read_csv(data_path, parse_dates=["datetime"])
    df["hour"] = df["datetime"].dt.hour
    df["weekday"] = df["datetime"].dt.day_name()
    df["day_type"] = df["weekday"].apply(lambda d: "Weekend" if d in ["Saturday", "Sunday"] else "Weekday")

    def categorize_time(h):
        if 5 <= h < 11:
            return "Breakfast"
        elif 11 <= h < 16:
            return "Lunch"
        elif 16 <= h < 22:
            return "Dinner"
        else:
            return "Late-night"

    df["meal_time"] = df["hour"].apply(categorize_time)

    summary = df.groupby(["day_type", "meal_time"]).size().reset_index(name="visit_count")
    summary.to_csv(output_path, index=False)
    print(f"Summary saved to {output_path}")

if __name__ == "__main__":
    analyze_patterns()
