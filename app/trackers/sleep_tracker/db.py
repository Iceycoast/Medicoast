import sqlite3
from typing import Optional
from app.db.database import get_connection
from .models import SleepLogCreate

def insert_sleep_log(log: SleepLogCreate, duration: float, created_at: str) -> int:
    
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
                INSERT INTO sleep_logs(user_id, date, sleep_time, wake_time, duration, created_at)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (log.user_id, log.date, log.sleep_time, log.wake_time, duration, created_at))
        conn.commit()
        log_id = cursor.lastrowid

        if log_id is None:
            raise sqlite3.DatabaseError("Failed to retrieve the Log ID.")
        
        return log_id
    except sqlite3.IntegrityError:
        raise ValueError("Invalid User ID or duplicate log. Please check your input.")

    except sqlite3.DatabaseError as e:
        raise RuntimeError(f"Database error while inserting sleep log: {e}")
    
    finally:
        conn.close()


def fetch_sleep_logs_by_user(user_id: int, date: Optional[str] = None  ) -> list[sqlite3.Row]:

    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if date: 
            cursor.execute("SELECT * FROM sleep_logs WHERE user_id = ? AND date = ?", (user_id,date))
        else:
            cursor.execute("SELECT * FROM sleep_logs WHERE user_id = ?", (user_id,))

        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def delete_sleep_log(log_id: int, user_id: int) -> bool:

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM sleep_logs WHERE log_id = ? AND user_id = ?", (log_id, user_id))
        conn.commit()
        return cursor.rowcount > 0 
    finally:
        conn.close()