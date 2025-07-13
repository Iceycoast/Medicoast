from pydantic import BaseModel, Field, field_validator
from app.utils.validators import validate_date_format, validate_time_format

class MedicationLogBase(BaseModel):
    medication_name : str = Field(..., description="Enter the name of the Medication.")
    dosage : str = Field(..., description="Enter the Dosage of the Medication.")
    time : str = Field(..., description="Enter the Time of the Medication (HH:MM)(24hr)")

    @field_validator('time')
    @staticmethod
    def validate_time_format(v:str) -> str:
        return validate_time_format(v)

class MedicationLogCreate(MedicationLogBase):
    user_id : int
    date: str = Field(..., description="Enter the Date (YYYY-MM-DD)")

    @field_validator('date')
    @staticmethod
    def validate_date_format(v:str) -> str:
        return validate_date_format(v)
    
class MedicationLogResponse(MedicationLogBase):
    log_id : int
    user_id : int 
    date : str 

    class Config:
        orm_mode = True