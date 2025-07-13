from fastapi import APIRouter
from .models import MedicationLogCreate, MedicationLogResponse
from . import controller
from typing import Optional

router = APIRouter(prefix="/medication", tags=["Medication Tracker"])

@router.post("/log", response_model= MedicationLogResponse)
def create_log(log:MedicationLogCreate):
    return controller.create_medication_log(log)

@router.get("/logs", response_model= list[MedicationLogResponse])
def get_logs(user_id: int, date: Optional[str]= None):
    return controller.get_medication_logs(user_id, date)

@router.delete("/log/{log_id}", response_model= dict)
def delete_log(log_id: int, user_id: int):
    return controller.remove_medication_log(log_id, user_id)