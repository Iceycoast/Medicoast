from pydantic import BaseModel
from typing import Optional

class DailySummary(BaseModel):
    date: str
    water_ml: Optional[int] = None
    calories: Optional[int] = None
    sleep_hours: Optional[float] = None
    latest_bmi: Optional[float] = None
    mood: Optional[list[str]] = None
    medications: Optional[list[str]] = None
    ai_summary: Optional[str] = None
