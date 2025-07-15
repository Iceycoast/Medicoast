from typing import Optional
from app.db.database import get_connection
from .models import BMILogsCreate, BMILogsResponse
import sqlite3

def insert_bmi_log(log: BMILogsCreate, bmi: float, category: str, created_at: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO bmi_logs(user_id, weight_kg, height_cm, bmi, category, date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (log.user_id, log.weight_kg, log.height_cm, bmi, category, log.date, created_at))
        conn.commit()
        log_id = cursor.lastrowid
        if log_id is None:
            raise sqlite3.DatabaseError("Failed to retrieve the log_id")
        return log_id
    except sqlite3.IntegrityError:
        raise ValueError("Invalid user_id or duplicate log.")
    except sqlite3.DatabaseError as e:
        raise RuntimeError(f"Database error while inserting bmi log: {e}")
    finally:
        conn.close()

def fetch_bmi_logs_by_user(user_id: int, date: Optional[str]) -> list[BMILogsResponse]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        if date:
            cursor.execute("SELECT * FROM bmi_logs WHERE user_id = ? AND date = ?", (user_id, date))
        else:
            cursor.execute("SELECT * FROM bmi_logs WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        return [BMILogsResponse.model_validate(row) for row in rows]
    finally:
        conn.close()

def delete_bmi_log(log_id: int, user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM bmi_logs WHERE log_id = ? AND user_id = ?", (log_id, user_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close() 