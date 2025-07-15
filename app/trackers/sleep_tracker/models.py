from pydantic import BaseModel, Field, field_validator
from app.utils.validators import validate_date_format, validate_time_format

class SleepLogBase(BaseModel):
    user_id : int
    date : str = Field(..., description="Please enter the date: (YYYY-MM-DD)")
    sleep_time: str = Field(..., description="Please enter the time you slept: (HH:MM AM/PM)")
    wake_time: str = Field(..., description="Please enter the time you woke up: (HH:MM AM/PM)")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v):
        return validate_date_format(v)
    
    @field_validator("sleep_time", "wake_time")
    @classmethod
    def validate_time_fields(cls, v):
        return validate_time_format(v)

class SleepLogCreate(SleepLogBase):
    pass    

class SleepLogResponse(SleepLogBase):
    log_id : int
    duration : float
        
    model_config = {
        "from_attributes": True
    }