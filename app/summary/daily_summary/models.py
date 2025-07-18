from pydantic import BaseModel, field_validator
from typing import Optional
from app.utils.validators import validate_date_format

class DailySummary(BaseModel):
    date: str
    water_ml: Optional[int] = None
    calories: Optional[int] = None
    sleep_hours: Optional[float] = None
    latest_bmi: Optional[float] = None
    mood: Optional[list[str]] = None
    medications: Optional[list[str]] = None
    ai_summary: Optional[str] = None

    @field_validator('date')
    @staticmethod
    def validate_date_format(v:str) -> str:
        return validate_date_format(v)