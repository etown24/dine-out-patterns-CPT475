import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# preliminary visualization of dining patterns
def visualize_patterns():
    # Resolve paths relative to this script so running from anywhere works
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(base_dir, ".."))
    summary_path = os.path.join(project_dir, "results", "summaries", "time_distribution.csv")
    chart_dir = os.path.join(project_dir, "results", "charts")
    os.makedirs(chart_dir, exist_ok=True)

    if not os.path.exists(summary_path):
        raise FileNotFoundError(
            f"Required summary file not found: {summary_path}\n"
            "Run `analyze_patterns.py` to generate this summary (which itself requires `matched_visits.csv`)."
        )

    df = pd.read_csv(summary_path)

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="meal_time", y="visit_count", hue="day_type")
    plt.title("Meal Time Visits: Weekday vs Weekend")
    plt.savefig(os.path.join(chart_dir, "weekday_vs_weekend.png"))
    plt.close()

    pivot = df.pivot(index="meal_time", columns="day_type", values="visit_count").fillna(0)
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
    plt.title("Heatmap of Dining Frequency")
    plt.savefig(os.path.join(chart_dir, "dining_heatmap.png"))
    plt.close()

    print(f"Charts saved in {chart_dir}")

if __name__ == "__main__":
    visualize_patterns()
