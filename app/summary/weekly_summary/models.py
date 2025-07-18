from typing import Optional
from pydantic import BaseModel, field_validator
from app.utils.validators import validate_date_format

class MoodLog(BaseModel):
    mood: str
    note: Optional[str] = None

class MealsLog(BaseModel):
    meals: str
    calories: int

class MedicationLog(BaseModel):
    name: str
    dosage: str

class DailyTrackerSummary(BaseModel):
    date: str
    # total water intake
    total_water_ml : Optional[int] = None

    # meals and total calories 
    meals: Optional[list[MealsLog]] = None
    total_calories: Optional[int] = None

    # bmi 
    bmi: Optional[float] = None

    # Sleep duration and time
    sleep_time: Optional[str] = None
    wake_time: Optional[str] = None
    duration: Optional[float] = None

    # mood for the day 
    moods: Optional[list[MoodLog]] = None

    # medications 
    medications: Optional[list[MedicationLog]] = None


    @field_validator('date')
    @staticmethod
    def validate_date_format(v:str) -> str:
        return validate_date_format(v)


class WeeklySummaryRequest(BaseModel):
    user_id: int 
    start_date: str

    @field_validator('start_date')
    @staticmethod
    def validate_date_format(v:str) -> str:
        return validate_date_format(v)

class WeeklySummaryResponse(BaseModel):
    start_date: str
    end_date: str
    week_logs: list[DailyTrackerSummary]