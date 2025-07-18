from typing import Optional, Any
from app.db.database import get_connection
import logging

logger = logging.getLogger(__name__)


def fetch_logs_for_week(table: str, user_id: int, start_date: str, end_date:str) -> list[dict[str,Any]]:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT * FROM {table} WHERE user_id = ? AND date BETWEEN ? AND ?",
                       (user_id, start_date, end_date))
        rows = cursor.fetchall()

        return [dict(row) for row in rows]
    
    except Exception as e:
        logger.error(
            f"Failed to fetch weekly logs from {table} for user_id={user_id} "
            f"between {start_date} and {end_date}: {e}"
        )
        return []
    finally:
        conn.close()