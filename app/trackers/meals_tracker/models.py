from typing import Optional, Literal
from pydantic import Field, field_validator, BaseModel
from app.utils.validators import validate_date_format, validate_time_format

class MealLogBase(BaseModel):
    meal_name: str = Field(..., min_length=3, description="Enter the name of the Meal.")
    calories: int = Field(..., gt=0, description="Enter the Calories consumed.")
    meal_type: Literal["Breakfast", "Lunch", "Dinner", "Snacks"] = Field(..., description="Choose one: Breakfast/Lunch/Dinner/Snacks")

class MealLogCreate(MealLogBase):
    user_id: int
    date: Optional[str] = Field(default=None, description="Optional. Provide the Date as (YYYY-MM-DD).")
    time: Optional[str] = Field(default=None, description="Optional. Provide the Time as (HH:MM AM/PM).")

    @field_validator("date")
    @staticmethod
    def validate_date_format(v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_date_format(v)
        return v

    @field_validator("time")
    @staticmethod
    def validate_time_format(v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validate_time_format(v)
        return v

class MealLogResponse(MealLogBase):
    log_id: int
    user_id: int
    date: str
    time: str

    model_config = {
        "from_attributes": True
    }
