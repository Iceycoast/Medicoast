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
        case "water_logs":
            total_water = sum(log.get('quantity_ml',0) for log in logs)
            return {"total_water_ml": total_water}
        
        case "meals_logs":
            return {"meals": [{"meal":log["meal_name"], "calories":log["calories"]} for log in logs]}
        
        case "sleep_logs":
            return {"sleep_sessions": [{"sleep_time": log["sleep_time"], "wake_time": log["wake_time"], "duration": log["duration"]}for log in logs]}
        
        case "bmi_logs":
            latest_log = max(logs, key= lambda x: x["created_at"])
            return {"latest_bmi": latest_log.get("bmi")}
        
        case "mood_logs":
            return {"moods": [{"mood": log["mood"], "note": log["note"]} for log in logs]}
        
        case "medication_logs":
            return {"medications": [{"medication_name": log["medication_name"], "dosage": log["dosage"]} for log in logs]}
        
        case _:
            return {}
        


def get_weekly_summary(user_id: int, start_date: str) -> dict[str,Any]:
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Date format. Must be YYYY-MM-DD")
    
    end_dt = start_dt + timedelta(days=6)

    start_str = start_dt.strftime("%Y-%m-%d")
    end_str = end_dt.strftime("%Y-%m-%d")

    summary = {}

    for table in TRACKER_TABLES:
        try:
            logs = fetch_logs_for_week(table, user_id, start_str, end_str)
            summary[table] = extract_weekly_summary(table, logs)
        except Exception as e:
            logger.error(f"Error in processing {table} logs: {e}")
            summary[table] = []

    return {
        "start_date": start_str,
        "end_date": end_str,
        "summary": summary
    }