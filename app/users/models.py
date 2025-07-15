from pydantic import BaseModel, Field, field_validator
from app.utils.validators import validate_male_or_female
from typing import Optional

class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: Optional[str] = None
    age: int = Field(..., gt=12, lt=90)
    gender : str = Field(..., description="Please enter your gender: Male or Female (or M/F)")

    @field_validator('gender')
    @staticmethod
    def validate_gender(v:str) -> str:
        return validate_male_or_female(v)

class UserCreate(UserBase):
    email: str = Field(..., description="Please enter your Email.")
    username: str = Field(..., min_length=4, description="Please choose your Username.")
    password: str = Field(..., min_length=8, description="Please choose a Password.")

class UserResponse(UserBase):
    user_id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str
