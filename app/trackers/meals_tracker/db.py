from typing import Optional
from app.db.database import get_connection
from .models import MealLogCreate, MealLogResponse
import sqlite3


def insert_meal_log(log: MealLogCreate, created_at: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO meals_logs (user_id, meal_name, calories, meal_type, date, time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (log.user_id, log.meal_name, log.calories, log.meal_type, log.date, log.time, created_at))

        conn.commit()
        log_id = cursor.lastrowid

        if log_id is None:
            raise sqlite3.DatabaseError("Failed to retrieve log_id.")

        return log_id

    except sqlite3.IntegrityError:
        raise ValueError("Invalid user_id or constraint violation.")

    except sqlite3.DatabaseError as e:
        raise RuntimeError(f"Database error while inserting meal log: {e}")

    finally:
        conn.close()


def fetch_meal_logs_by_user(user_id: int, date: Optional[str] = None) -> list[MealLogResponse]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if date:
            cursor.execute(
                "SELECT * FROM meals_logs WHERE user_id = ? AND date = ? ORDER BY time ASC",
                (user_id, date)
            )
        else:
            cursor.execute(
                "SELECT * FROM meals_logs WHERE user_id = ? ORDER BY date DESC, time DESC",
                (user_id,)
            )

        rows = cursor.fetchall()
        return [MealLogResponse.model_validate(row) for row in rows]

    finally:
        conn.close()


def delete_meal_log(log_id: int, user_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM meals_logs WHERE log_id = ? AND user_id = ?", (log_id, user_id))
        conn.commit()
        return cursor.rowcount > 0

    finally:
        conn.close()
