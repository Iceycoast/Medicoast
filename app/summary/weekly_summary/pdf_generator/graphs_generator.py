import os
import matplotlib.pyplot as plt
from typing import Any

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def _save_plot(fig, name: str) -> str:
    path = os.path.join(TEMP_DIR, f"{name}.png")
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    return path

def _clear_old_graphs():
    for file in os.listdir(TEMP_DIR):
        if file.endswith(".png"):
            os.remove(os.path.join(TEMP_DIR, file))

def generate_weekly_graphs(summary: dict[str, Any]) -> dict[str, str]:
    graphs: dict[str, str] = {}
    _clear_old_graphs()

    # Water Intake Graph
    water_logs = summary.get("water_logs", [])
    if water_logs:
        sorted_logs = sorted(water_logs, key=lambda x: x["date"])
        dates = [log["date"] for log in sorted_logs]
        values = [log["amount_ml"] for log in sorted_logs]
        fig, ax = plt.subplots()
        ax.bar(dates, values, color="skyblue")
        ax.set_title("Daily Water Intake (ml)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Water Intake")
        graphs["water"] = _save_plot(fig, "water_intake")

    # BMI Trend Graph
    bmi_logs = summary.get("bmi_logs", [])
    if bmi_logs:
        sorted_logs = sorted(bmi_logs, key=lambda x: x["date"])
        dates = [log["date"] for log in sorted_logs]
        values = [log["bmi"] for log in sorted_logs]
        fig, ax = plt.subplots()
        ax.plot(dates, values, marker="o", color="green")
        ax.set_title("BMI Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI")
        graphs["bmi"] = _save_plot(fig, "bmi_trend")

    # Sleep Duration Graph
    sleep_logs = summary.get("sleep_logs", [])
    if sleep_logs:
        sorted_logs = sorted(sleep_logs, key=lambda x: x["date"])
        dates = [log["date"] for log in sorted_logs]
        values = [log["duration_hours"] for log in sorted_logs]
        fig, ax = plt.subplots()
        ax.plot(dates, values, marker="o", color="purple")
        ax.set_title("Sleep Duration (hrs)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Hours Slept")
        graphs["sleep"] = _save_plot(fig, "sleep_duration")

    # Calorie Graph
    meal_logs = summary.get("meals_logs", [])
    if meal_logs:
        calorie_map: dict[str, int] = {}
        for log in meal_logs:
            date = log["date"]
            calories = log.get("calories", 0)
            calorie_map[date] = calorie_map.get(date, 0) + calories
        if calorie_map:
            sorted_items = sorted(calorie_map.items())
            dates = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]
            fig, ax = plt.subplots()
            ax.bar(dates, values, color="orange")
            ax.set_title("Total Calories Consumed")
            ax.set_xlabel("Date")
            ax.set_ylabel("Calories")
            graphs["calories"] = _save_plot(fig, "calories")

    return graphs
