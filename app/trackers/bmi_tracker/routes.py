from fastapi import APIRouter
from typing import Optional
from .models import BMILogsCreate, BMILogsResponse
from .controller import create_bmi_log, get_bmi_logs, remove_bmi_log
from .ai_advice import get_ai_advice_for_bmi_log

router = APIRouter(prefix="/bmi", tags=["BMI Tracker"])

@router.post("/log", response_model=BMILogsResponse)
def create_log(log: BMILogsCreate):
    return create_bmi_log(log)

@router.get("/logs", response_model=list[BMILogsResponse])
def get_logs(user_id: int, date: Optional[str] = None):
    return get_bmi_logs(user_id, date)

@router.delete("/log/{log_id}", response_model=dict)
def delete_log(log_id: int, user_id: int):
    return remove_bmi_log(log_id, user_id)

@router.get("/advice")
def get_advice(log_id: int, user_id: int):
    advice = get_ai_advice_for_bmi_log(log_id, user_id)
    return {"advice": advice}