from fastapi import APIRouter, Depends
from typing import Optional
from .models import BMILogsCreate, BMILogsResponse
from .controller import create_bmi_log, get_bmi_logs, remove_bmi_log
from .ai_advice import get_ai_advice_for_bmi_log
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/bmi", tags=["BMI Tracker"])

@router.post("/log", response_model=BMILogsResponse)
def create_log(log: BMILogsCreate):
    return create_bmi_log(log)

@router.get("/logs", response_model=list[BMILogsResponse])
def get_logs(current_user: dict = Depends(get_current_user), date: Optional[str] = None):
    user_id = current_user["user_id"]
    return get_bmi_logs(user_id, date)

@router.delete("/log/{log_id}")
def delete_log(log_id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return remove_bmi_log(log_id, user_id)

@router.get("/advice/{log_id}")
def get_advice(log_id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    advice = get_ai_advice_for_bmi_log(log_id, user_id)
    return {"advice": advice}