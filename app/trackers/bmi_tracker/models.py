from pydantic import BaseModel, Field, field_validator
from app.utils.validators import validate_date_format
from typing import Optional

class BMILogsBase(BaseModel):
    weight_kg: float = Field(..., gt=10, description="Please enter your weight in KGs.")
    height_cm: float = Field(..., gt=50, description="Please enter your height in centimeters.")

class BMILogsCreate(BMILogsBase):
    user_id: int
    date: str = Field(..., description="Enter the date (YYYY-MM-DD)")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v):
        return validate_date_format(v)

class BMILogsResponse(BMILogsBase):
    log_id: int
    user_id: int
    weight_kg: float
    height_cm: float
    bmi: float
    category: str
    date: str

    model_config = {
        "from_attributes": True
    } 