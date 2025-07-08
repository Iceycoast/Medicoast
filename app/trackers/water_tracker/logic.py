from pydantic import BaseModel, Field
from typing import Optional, final
from datetime import datetime, timezone
from fastapi import HTTPException, status
from pydantic_core.core_schema import none_schema
from app.db.database import get_connection
import sqlite3

from app.users.logic import UserResponse


class WaterLogBase(BaseModel):
    quantity_ml: int = Field(..., gt=0, description="Amount of water in milliliters")

class WaterLogCreate(WaterLogBase):
    user_id: int

class WaterLogResponse(WaterLogBase):
    log_id: int
    user_id: int
    date: str
    time: str
    created_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.isoformat()}



def add_water_log(log: WaterLogCreate) -> WaterLogResponse:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    date = datetime.now().strftime("%d-%m-%Y")
    time = datetime.now().strftime("%H:%M")
    created_at = datetime.now(timezone.utc).isoformat()
    try:
        cursor.execute('''
                INSERT INTO water_logs(user_id, quantity_ml, date, time, created_at)
                VALUES (?, ?, ?, ?, ?)''',
                (log.user_id,log.quantity_ml, date, time, created_at))
        conn.commit()
        log_id = cursor.lastrowid
        if log_id is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve log_id")

        return WaterLogResponse(
            log_id= log_id,
            user_id= log.user_id,
            quantity_ml= log.quantity_ml,
            date = date, 
            time = time,
            created_at= datetime.fromisoformat(created_at))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid data or user_id does not exist")
    finally:
        conn.close()


def get_water_logs_by_user(user_id:int, date:Optional[str]= None) -> list[WaterLogResponse]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if date:
            cursor.execute("SELECT * FROM water_logs WHERE user_id = ? AND date = ?", (user_id, date))
        else:
            cursor.execute("SELECT * FROM water_logs WHERE user_id = ?", (user_id,))
        
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No water logs found.")

        return [WaterLogResponse(
            user_id= row['user_id'],
            log_id= row['log_id'],
            quantity_ml= row['quantity_ml'],
            date= row['date'],
            time = row['time'],
            created_at=datetime.fromisoformat(row["created_at"])
        ) for row in rows
        ]
    finally:
        conn.close()

def delete_water_log(log_id:int, user_id:int) -> str:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1 FROM water_logs WHERE log_id = ? AND user_id = ?",(log_id, user_id))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Water log not found.")
    
        cursor.execute("DELETE FROM water_logs WHERE log_id = ? AND user_id = ?",(log_id, user_id))
        conn.commit()

        return "Water log has been deleted successfully."

    finally:
        conn.close()