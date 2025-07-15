from pydantic import BaseModel, model_validator, Field, field_validator
from typing import Optional
from app.utils.validators import validate_date_format, validate_time_format


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
    date : Optional[str] = Field(default= None, description="Optional. Provide date as (YYYY-MM-DD)")
    time : Optional[str] = Field(default= None, description="Optional. Provide the time as (HH:MM AM/PM)")

    @field_validator('date')
    @staticmethod
    def validate_date_format(v:Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_date_format(v)
        return v 
    
    
    @field_validator('time')
    @staticmethod
    def validate_time_format(v:Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_time_format(v)
        return v 


class MoodLogResponse(MoodLogsBase):
    log_id : int
    user_id : int
    ai_sentiment : str
    ai_suggestion : str
    date: str
    time : str

    model_config = {
        "from_attributes":True
    }