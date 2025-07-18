from pydantic import BaseModel, Field, field_validator
from app.utils.validators import validate_date_format, validate_time_format

class SleepLogBase(BaseModel):
    date : str = Field(..., description="Please enter the date: (YYYY-MM-DD)")
    sleep_time: str = Field(..., description="Please enter the time you slept: (HH:MM AM/PM)")
    wake_time: str = Field(..., description="Please enter the time you woke up: (HH:MM AM/PM)")

    @field_validator("date")
    @staticmethod
    def validate_date_format(v: str) -> str:
        return validate_date_format(v)
    
    @field_validator("sleep_time", "wake_time")
    @staticmethod
    def validate_time_fields(v: str) -> str:
        return validate_time_format(v)

class SleepLogCreate(SleepLogBase):
    user_id : int

class SleepLogResponse(SleepLogBase):
    log_id : int
    user_id : int
    duration : float
        
    model_config = {
        "from_attributes": True
    }