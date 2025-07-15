from typing import Optional
from datetime import datetime
from app.db.database import get_connection
import sqlite3
from .models import MedicationLogCreate, MedicationLogResponse

def insert_medication_log(log:MedicationLogCreate, created_at: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
                INSERT INTO medication_logs (user_id, medication_name, dosage, date, time, created_at)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (log.user_id, log.medication_name, log.dosage, log.date, log.time, created_at))
        conn.commit()
        log_id = cursor.lastrowid

        if log_id is None:
            raise sqlite3.DatabaseError ("Failed to retrive Log ID")
        return log_id
    
    except sqlite3.IntegrityError:
        raise ValueError ("Invalid User ID or Duplicate Log.")
    
    except sqlite3.DatabaseError as e:
        raise RuntimeError (f"Database Error while inserting Medication log: {e}")
    
    finally:
        conn.close()

def fetch_medication_logs_by_user(user_id: int, date:Optional[str]=None) -> list[MedicationLogResponse]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if date:
            cursor.execute("SELECT * FROM medication_logs WHERE user_id = ? AND date = ? ORDER BY time  ASC", (user_id, date))
        else:
            cursor.execute("SELECT * FROM medication_logs WHERE user_id = ? ORDER BY date DESC, time DESC" , (user_id,))

        rows = cursor.fetchall()
        return [MedicationLogResponse.model_validate(row) for row in rows]
    
    finally:
        conn.close()

def delete_medication_log(log_id: int, user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM medication_logs WHERE log_id = ? AND user_id = ?", (log_id, user_id))
        conn.commit()

        return cursor.rowcount > 0
        
    finally:
        conn.close()