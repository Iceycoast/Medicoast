from pydantic import BaseModel, model_validator, Field, field_validator
from typing import Optional
from datetime import datetime, date
from app.utils.validators import validate_date_format


class MoodLogsBase(BaseModel):
    mood : Optional[str] = Field (description="Enter your mood. (e.g., happy/sad/angry/joyful)")
    note : Optional[str] = Field(description="Enter a Note of how are you feeling.")

    @model_validator(mode="after")
    def require_mood_or_note(self):
        if not self.mood and not self.note:
            raise ValueError("At least one of 'Mood' or 'Note' should be provided ")
        return self

class MoodLogCreate(MoodLogsBase):
    user_id: int
    date : str = Field(..., description="Please enter the Date (DD-MM-YYYY)")

    @field_validator('date')
    @staticmethod
    def validate_date_format(v:str) -> str:
        return validate_date_format(v)
    
class MoodLogResponse(MoodLogsBase):
    log_id : int
    user_id : int
    ai_sentiment : str
    ai_suggestion : str
    date: str

    class Config:
        orm_mode = True