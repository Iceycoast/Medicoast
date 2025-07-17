from typing import Any

def extract_summary_from_logs(table: str, logs: list[Any]) -> dict[str, Any]:
    """
    Extract summary data from logs of a specific tracker.
    Returns a dictionary with the summary data.
    """

    if not logs:
        return {}

    if table == "water_logs":
        total_water = sum(log.quantity_ml for log in logs if getattr(log, "quantity_ml", None) is not None)
        return {"water_ml": total_water}

    elif table == "meals_logs":
        total_calories = sum(log.calories for log in logs if getattr(log, "calories", None) is not None)
        return {"calories": total_calories}

    elif table == "sleep_logs":
        total_sleep = sum(log.duration for log in logs if getattr(log, "duration", None) is not None)
        return {"sleep_hours": total_sleep}

    elif table == "bmi_logs":
        # Get the most recent BMI based on created_at
        latest_log = max(logs, key=lambda log: getattr(log, "created_at", ""), default=None)
        return {"latest_bmi": getattr(latest_log, "bmi", None) if latest_log else None}

    elif table == "mood_logs":
        moods = [log.mood for log in logs if getattr(log, "mood", None)]
        return {"mood": moods}

    elif table == "medication_logs":
        meds = [log.medication_name for log in logs if getattr(log, "medication_name", None)]
        return {"medications": meds}

    return {}
