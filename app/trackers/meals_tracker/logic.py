from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional
from app.db.database import get_connection
from fastapi import HTTPException, status
from app.utils.validators import validate_date_format, validate_time_format
import sqlite3


class MealsLogsBase(BaseModel):
    meal_name: str = Field(..., min_length= 3, description= "Enter the name of the Meal.")
    calories: int = Field(..., gt= 0, description= "Enter the Calories consumed")
    meal_type: str = Field(..., min_length= 5, description= "(Breakfast/Lunch/Dinner/Snacks)")

class MealsLogsCreate(MealsLogsBase):
    user_id: int 
    date: str = Field(..., description= "Enter the Date (DD-MM-YYYY)")
    time: str = Field(..., description= "Enter the Time (HH-MM)(24 Hour)")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v):
        return validate_date_format(v)

    @field_validator("time")
    @classmethod
    def validate_time_format(cls, v):
        return validate_time_format(v)


class MealsLogsResponse(MealsLogsBase):
    log_id: int
    user_id: int
    meal_name: str
    calories: int
    meal_type: str
    date: str
    time: str
    class Config:
        orm_mode = True


def create_meals_logs(log: MealsLogsCreate) -> MealsLogsResponse:
    conn = get_connection()
    cursor = conn.cursor()

    date = log.date
    time = log.time
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        cursor.execute('''
                INSERT INTO meals_logs(user_id, meal_name, calories, meal_type, date, time, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (log.user_id, log.meal_name, log.calories, log.meal_type, date, time, created_at))

        conn.commit()
        log_id = cursor.lastrowid
        if log_id is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve log_id")

        return MealsLogsResponse(
            log_id= log_id,
            user_id= log.user_id,
            meal_name= log.meal_name,
            calories= log.calories,
            meal_type= log.meal_type,
            date = date,
            time= time
        )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid data or user_id does not exist")

    finally:
        conn.close()

def get_meals_logs_by_user(user_id: int, date: Optional[str]=None) -> list[MealsLogsResponse]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if date:
            cursor.execute("SELECT * FROM meals_logs WHERE user_id = ? AND date = ?", (user_id,date))

        else:
            cursor.execute("SELECT * FROM meals_logs WHERE user_id = ?",(user_id,))

        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meals log not found.")
        
        return [MealsLogsResponse(
            log_id= row['log_id'],
            user_id= row['user_id'],
            meal_name= row['meal_name'],
            calories= row['calories'],
            meal_type= row['meal_type'],
            date = row['date'],
            time= row['time']
        ) for row in rows
        ]
    finally:
        conn.close()

def delete_meal_log(log_id:int, user_id:int) -> str:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1 FROM meals_logs WHERE log_id = ? AND user_id = ?", (log_id, user_id))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found for the user.")
        cursor.execute("DELETE FROM meals_logs WHERE log_id = ? AND user_id = ?", (log_id, user_id))
        conn.commit()
        return "Meal Log has been deleted Successfully."
    finally:
        conn.close()