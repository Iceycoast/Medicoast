import sqlite3
import logging
from datetime import datetime, timezone
from typing import Any
from app.db.database import get_connection

logger = logging.getLogger(__name__)

from app.trackers.bmi_tracker.models import BMILogsResponse
from app.trackers.water_tracker.models import WaterLogResponse
from app.trackers.meals_tracker.models import MealLogResponse
from app.trackers.sleep_tracker.models import SleepLogResponse
from app.trackers.mood_tracker.models import MoodLogResponse
from app.trackers.medication_tracker.models import MedicationLogResponse


def save_ai_summary(user_id: int, date: str, ai_summary: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        created_at = datetime.now(timezone.utc).isoformat()
        cursor.execute("""
            INSERT INTO daily_ai_summaries (user_id, date, ai_summary, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, date) DO UPDATE SET ai_summary = excluded.ai_summary, created_at = excluded.created_at
        """, (user_id, date, ai_summary, created_at))
        conn.commit()
    finally:
        conn.close()

def get_ai_summary(user_id: int, date: str) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT ai_summary FROM daily_ai_summaries
            WHERE user_id = ? AND date = ?
        """, (user_id, date))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()

def fetch_logs(table_name: str, user_id: int, date: str) -> list[Any]:
    """
    Fetch logs from a specific tracker table.
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
        logger.error(f"Unknown table name: {table_name}")
        return []

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Safe because table_name is validated through model_map

        cursor.execute(
            f"SELECT * FROM {table_name} WHERE user_id = ? AND date = ?",
            (user_id, date)
        )
        rows = cursor.fetchall()
        return [model_class.model_validate(dict(row)) for row in rows]

    except Exception as e:
        logger.error(f"Error fetching logs from {table_name} for user_id={user_id} on {date}: {e}")
        return []
    finally:
        conn.close()
