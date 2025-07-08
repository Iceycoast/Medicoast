from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.db.database import get_connection
from app.utils.validators import validate_date_format, validate_time_format
import sqlite3



class WaterLogBase(BaseModel):
    quantity_ml: int = Field(..., gt=0, description="Amount of water in milliliters")

class WaterLogCreate(WaterLogBase):
    user_id: int
    date: str = Field(..., description= "Enter the Date (dd-mm-yyyy)")
    time: str = Field(..., description= "Enter the Time (HH-MM)(24 Hour)")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v):
        return validate_date_format(v)

    @field_validator("time")
    @classmethod
    def validate_time_format(cls, v):
        return validate_time_format(v)

class WaterLogResponse(WaterLogBase):
    log_id: int
    user_id: int
    date: str
    time: str
    class Config:
        orm_mode = True



def add_water_log(log: WaterLogCreate) -> WaterLogResponse:
    conn = get_connection()
    cursor = conn.cursor()

    date = log.date
    time = log.time
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
            time = time

        )
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
            time = row['time']

        ) for row in rows
        ]
    finally:
        conn.close()

def delete_water_log(log_id:int, user_id:int) -> str:
    conn = get_connection()
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