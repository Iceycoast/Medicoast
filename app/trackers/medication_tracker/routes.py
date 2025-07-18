from fastapi import APIRouter, Depends
from .models import MedicationLogCreate, MedicationLogResponse
from . import controller
from app.auth.dependencies import get_current_user
from typing import Optional

router = APIRouter(prefix="/medication", tags=["Medication Tracker"])

@router.post("/log", response_model=MedicationLogResponse)
def create_log(log: MedicationLogCreate):
    return controller.create_medication_log(log)

@router.get("/logs", response_model=list[MedicationLogResponse])
def get_logs(current_user: dict = Depends(get_current_user), date: Optional[str]= None):
    user_id = current_user["user_id"]
    return controller.get_medication_logs(user_id, date)

@router.delete("/log/{log_id}", response_model=dict)
def delete_log(log_id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return controller.remove_medication_log(log_id, user_id)