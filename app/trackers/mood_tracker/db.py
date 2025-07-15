from app.db.database import get_connection
from typing import Optional
from .models import MoodLogCreate, MoodLogResponse
import sqlite3

def insert_mood_log(log: MoodLogCreate, ai_sentiment: str, ai_suggestion: str, created_at: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
                INSERT INTO mood_logs (user_id, mood, note, ai_sentiment, ai_suggestion, date, time, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                (log.user_id, log.mood, log.note, ai_sentiment, ai_suggestion, log.date, log.time, created_at))
        conn.commit()
        log_id = cursor.lastrowid

        if log_id is None:
            raise sqlite3.DatabaseError("Failed to retrieve the log_id")
        return log_id
    
    except sqlite3.IntegrityError:
        raise ValueError ("Invalid user_id or Duplicate Log.")
    
    except sqlite3.DatabaseError as e:
        raise RuntimeError (f"Database error while inserting Mood Log: {e}")
    
    finally:
        conn.close()

def fetch_mood_logs_by_user(user_id: int, date: Optional[str]= None) -> list[MoodLogResponse]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if date:
            cursor.execute("SELECT * FROM mood_logs WHERE user_id = ? AND date = ?", (user_id, date))

        else:
            cursor.execute("SELECT * FROM mood_logs WHERE user_id = ?",(user_id,))

        rows = cursor.fetchall()

        return [MoodLogResponse.model_validate(row)for row in rows]
    
    finally:
        conn.close()

def delete_mood_log(log_id: int, user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM mood_logs WHERE log_id = ? AND user_id = ?",(log_id,user_id))
        conn.commit()

        return cursor.rowcount > 0
    
    finally:
        conn.close()