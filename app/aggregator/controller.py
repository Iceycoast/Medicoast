from app.db.database import get_connection
from .constants import TRACKER_TABLES
import sqlite3
import logging

from app.trackers.bmi_tracker.models import BMILogsResponse
from app.trackers.water_tracker.models import WaterLogResponse
from app.trackers.meals_tracker.models import MealLogResponse
from app.trackers.sleep_tracker.models import SleepLogResponse
from app.trackers.mood_tracker.models import MoodLogResponse
from app.trackers.medication_tracker.models import MedicationLogResponse
from app.aggregator.models import DailySummary
from app.aggregator.utils import extract_summary_from_logs
from app.aggregator.ai_summary import generate_daily_summary
from typing import Any


def fetch_logs(table_name: str, user_id: int, date: str) -> list:
    """
    Fetch logs from a specific table for a user and date.
    Returns an empty list on failure and logs the error.
    """
    model_map = {
        "bmi_logs": BMILogsResponse,
        "water_logs": WaterLogResponse,
        "meals_logs": MealLogResponse,
        "sleep_logs": SleepLogResponse,
        "mood_logs": MoodLogResponse,
        "medication_logs": MedicationLogResponse,
    }

    model_class = model_map.get(table_name)
    if model_class is None:
        logging.error(f"Unknown table name: {table_name}")
        return []

    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT * FROM {table_name} WHERE user_id = ? AND date = ?",
            (user_id, date)
        )
        rows = cursor.fetchall()
        return [model_class.model_validate(dict(row)) for row in rows]

    except Exception as e:
        logging.error(f"Error fetching logs from {table_name}: {e}")
        return []
    finally:
        conn.close()
        


def get_daily_logs(user_id: int, date: str) -> dict[str, Any]:
    summary: dict[str, Any] = {"date": date}

    for table in TRACKER_TABLES:
        logs = fetch_logs(table, user_id, date)
        summary.update(extract_summary_from_logs(table, logs))

    # Convert to Pydantic model before passing to AI
    daily_summary_model = DailySummary(**summary)

    # Generate AI summary
    summary["ai_summary"] = generate_daily_summary(daily_summary_model)

    return summary
