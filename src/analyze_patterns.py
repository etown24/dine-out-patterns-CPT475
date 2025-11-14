import pandas as pd
import os

def analyze_patterns():
    data_path = os.path.join("..", "data", "matched_visits.csv")
    output_path = os.path.join("..", "results", "summaries", "time_distribution.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

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
