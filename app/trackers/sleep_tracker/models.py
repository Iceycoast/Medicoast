from pydantic import BaseModel, Field, field_validator
from app.utils.validators import validate_date_format

class SleepLogBase(BaseModel):
    user_id : int
    date : str = Field(..., description="Please enter the date: (YYYY-MM-DD)")
    sleep_time : str = Field(..., description="Please enter the time you slept: (HH:MM)(24Hr)")
    wake_time : str = Field(..., description="Please enter the time you woke up: (HH:MM)(24Hr)")

class SleepLogCreate(SleepLogBase):
    
    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v):
        return validate_date_format(v)

class SleepLogResponse(SleepLogBase):
    log_id : int
    duration : float
        
    class Config:
        orm_mode = True