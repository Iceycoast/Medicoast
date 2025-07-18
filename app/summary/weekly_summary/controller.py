from typing import Any
from fastapi import HTTPException, status
from .db import fetch_logs_for_week
from app.summary.constants import TRACKER_TABLES
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

def extract_weekly_summary(table: str, logs: list[dict[str,Any]]) -> dict[str,Any]:

    if not logs:
        return {}
    
    match table:
        case "bmi_logs":
            bmi_values = [log.get("bmi") for log in logs if log.get("bmi") is not None]
            latest_log = max(logs, key=lambda x: x["created_at"])
            return {
                "latest_bmi": latest_log.get("bmi"),
                "bmi_values": bmi_values
            }

        case "water_logs":
            total_water = sum(log.get('quantity_ml', 0) for log in logs)
            return {
                "total_water_ml": total_water
            }

        case "meals_logs":
            total_calories = sum(log.get("calories", 0) for log in logs)
            return {
                "meals": [{"meal": log["meal_name"], "calories": log["calories"]} for log in logs],
                "total_calories": total_calories
            }

        case "sleep_logs":
            durations = [log.get("duration", 0) for log in logs]
            return {
                "sleep_sessions": [{"sleep_time": log["sleep_time"], "wake_time": log["wake_time"], "duration": log["duration"]} for log in logs],
                "sleep_durations": durations
            }

        
        case "mood_logs":
            return {"moods": [{"mood": log["mood"], "note": log["note"]} for log in logs]}
        
        case "medication_logs":
            return {"medications": [{"medication_name": log["medication_name"], "dosage": log["dosage"]} for log in logs]}
        
        case _:
            return {}
        


def get_weekly_summary(user_id: int, start_date: str) -> dict[str, Any]:
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Date format. Must be YYYY-MM-DD")

    end_dt = start_dt + timedelta(days=6)
    start_str, end_str = start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d")

    summary = {}
    bmi_values = []
    total_water = 0
    total_calories = 0
    sleep_durations = []

    for table in TRACKER_TABLES:
        try:
            logs = fetch_logs_for_week(table, user_id, start_str, end_str)
            data = extract_weekly_summary(table, logs)
            summary[table] = data

            match table:
                case "bmi_logs":
                    bmi_values.extend(data.get("bmi_values", []))
                case "water_logs":
                    total_water = data.get("total_water_ml", 0)
                case "meals_logs":
                    total_calories = data.get("total_calories", 0)
                case "sleep_logs":
                    sleep_durations.extend(data.get("sleep_durations", []))

        except Exception as e:
            logger.error(f"Error in processing {table} logs: {e}")
            summary[table] = {}

    # Final averages (all divided by 7 since it’s a fixed week span)
    avg_bmi = round(sum(bmi_values) / len(bmi_values), 2) if bmi_values else 0
    avg_sleep = round(sum(sleep_durations) / len(sleep_durations), 2) if sleep_durations else 0
    avg_water = round(total_water / 7, 2) if total_water else 0
    avg_calories = round(total_calories / 7, 2) if total_calories else 0 

    return {
        "start_date": start_str,
        "end_date": end_str,
        "summary": summary,
        "weekly_stats": {
            "average_bmi": avg_bmi,
            "average_water_ml": avg_water,
            "average_calories": avg_calories,
            "average_sleep_duration": avg_sleep
        }
    }
