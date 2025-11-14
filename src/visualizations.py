import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# preliminary visualization of dining patterns
def visualize_patterns():
    summary_path = os.path.join("..", "results", "summaries", "time_distribution.csv")
    chart_dir = os.path.join("..", "results", "charts")
    os.makedirs(chart_dir, exist_ok=True)

    df = pd.read_csv(summary_path)

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="meal_time", y="visit_count", hue="day_type")
    plt.title("Meal Time Visits: Weekday vs Weekend")
    plt.savefig(os.path.join(chart_dir, "weekday_vs_weekend.png"))
    plt.close()

    pivot = df.pivot("meal_time", "day_type", "visit_count")
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
    plt.title("Heatmap of Dining Frequency")
    plt.savefig(os.path.join(chart_dir, "dining_heatmap.png"))
    plt.close()

    print(f"Charts saved in {chart_dir}")

if __name__ == "__main__":
    visualize_patterns()
