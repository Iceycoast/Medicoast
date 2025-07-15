from typing import Optional
from app.db.database import get_connection
from .models import WaterLogCreate, WaterLogResponse
import sqlite3


def insert_into_water_log(log: WaterLogCreate, created_at:str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
                INSERT INTO water_logs(user_id, quantity_ml, date, time, created_at)
                VALUES (?, ?, ?, ?, ?)''',
                (log.user_id,log.quantity_ml, log.date, log.time, created_at))
        conn.commit()
        log_id = cursor.lastrowid
        if log_id is None:
            raise sqlite3.DatabaseError ("Failed to retrieve the log_id")
        return log_id
    
    except sqlite3.IntegrityError:
        raise ValueError ("Invalid user_id or duplicate log.")
    
    except sqlite3.DatabaseError as e:
        raise RuntimeError (f"Database error while inserting water log: {e}")
      
    finally:
        conn.close()

def fetch_logs_by_user(user_id: int, date: Optional[str]) -> list[WaterLogResponse]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try: 
        if date:
            cursor.execute("SELECT * FROM water_logs WHERE user_id = ? AND date = ?", (user_id, date))
        else:
            cursor.execute("SELECT * FROM water_logs WHERE user_id = ?", (user_id,))
        
        rows = cursor.fetchall()

        return [WaterLogResponse.model_validate(row) for row in rows]
    
    finally:
        conn.close()


def delete_water_log(log_id:int, user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("DELETE FROM water_logs WHERE log_id = ? AND user_id = ?",(log_id,user_id))
        conn.commit()

        return cursor.rowcount > 0
    
    finally:
        conn.close()