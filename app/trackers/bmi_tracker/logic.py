from datetime import datetime,timezone
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.db.database import get_connection
from app.utils.validators import validate_date_format
import sqlite3


class BMILogsBase(BaseModel):
    weight_kg : float = Field(..., gt=10, description="Please enter your weight in KGs.")
    height_cm : float = Field(..., gt=50, description="Please enter your height in centimeters.")

class BMILogsCreate(BMILogsBase):
    user_id : int
    date : str = Field(..., description="Enter the date (YYYY-MM-DD)")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v):
        return validate_date_format(v)


class BMILogsResponse(BMILogsBase):
    log_id: int
    user_id : int
    weight_kg : float
    height_cm : float
    bmi : float
    category : str
    date : str

    class Config:
        orm_mode = True


def calculate_bmi(weight_kg:float, height_cm:float) -> tuple[float, str]:
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError ("Height or Weight can not be 0. Please enter Valid Data.")
    
    height_m = height_cm/100
    bmi = round(weight_kg/(height_m**2),2)

    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return bmi, category

def create_bmi_logs(log: BMILogsCreate) -> BMILogsResponse:
    conn = get_connection()
    cursor = conn.cursor()

    bmi, category = calculate_bmi(log.weight_kg, log.height_cm)
    date = log.date
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        cursor.execute('''
                INSERT INTO bmi_logs(user_id, weight_kg, height_cm, bmi, category, date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (log.user_id, log.weight_kg, log.height_cm, bmi, category, date, created_at))

        conn.commit()
        log_id = cursor.lastrowid
        if log_id is None:
            raise HTTPException(status_code=500, detail= "Failed to retrieve Log ID.")
        
        return BMILogsResponse(
                log_id= log_id,
                user_id= log.user_id,
                weight_kg= log.weight_kg,
                height_cm= log.height_cm,
                bmi = bmi,
                category= category,
                date= date
        )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail= "Invalid data or User ID does not exist.")
    finally:
        conn.close()

def delete_bmi_log(log_id:int, user_id:int) -> str:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1 FROM bmi_logs WHERE log_id = ? AND user_id = ?",(log_id,user_id))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Log not found for the User.")
        cursor.execute("DELETE FROM bmi_logs WHERE log_id = ? AND user_id = ?",(log_id,user_id))

        conn.commit()
        return "BMI Log successfully deleted."
    finally:
        conn.close()

def get_bmi_logs_by_user(user_id: int, date:Optional[str]=None) -> list[BMILogsResponse]:
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        if date:
            cursor.execute("SELECT * FROM bmi_logs WHERE user_id = ? AND date = ?", (user_id,date))
        else:
            cursor.execute("SELECT * FROM bmi_logs WHERE user_id = ?", (user_id,))

        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BMI Logs not found.")
        
        return[BMILogsResponse(
                log_id= row['log_id'],
                user_id= row['user_id'],
                weight_kg= row['weight_kg'],
                height_cm= row['height_cm'],
                bmi= row['bmi'],
                category= row['category'],
                date= row['date']
        ) for row in rows
        ]
    finally:
        conn.close()