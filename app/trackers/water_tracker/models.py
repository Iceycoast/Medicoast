from pydantic import BaseModel, field_validator, Field
from app.utils.validators import validate_date_format, validate_time_format
from typing import Optional

class WaterLogBase(BaseModel):
    quantity_ml: int = Field(..., gt=0, description="Amount of water in milliliters")

class WaterLogCreate(WaterLogBase):
    user_id: int
    date: Optional[str] = Field(default=None, description= "Optional. Provide the Date as (YYYY-MM-DD)")
    time: Optional[str] = Field(default=None, description= "Optional. Provide the Time as (HH-MM AM/PM)")

    @field_validator("date")
    @staticmethod
    def validate_date_format(v:Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_date_format(v)
        return v

    @field_validator("time")
    @staticmethod
    def validate_time_format(v:Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_time_format(v)
        return v 

class WaterLogResponse(WaterLogBase):
    log_id: int
    user_id: int
    date: str
    time: str

    model_config = {
        "from_attributes": True
    }
