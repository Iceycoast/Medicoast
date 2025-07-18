from fastapi import APIRouter, Depends
from .models import WaterLogCreate, WaterLogResponse
from . import controller
from app.auth.dependencies import get_current_user
from typing import Optional

router = APIRouter(prefix="/water", tags=["Water Tracker"])

@router.post("/log", response_model=WaterLogResponse)
def create_log(log: WaterLogCreate):
    return controller.create_water_log(log)

@router.get("/logs", response_model=list[WaterLogResponse])
def get_logs(current_user: dict = Depends(get_current_user), date: Optional[str] = None):
    user_id = current_user["user_id"]
    return controller.get_water_logs(user_id, date)

@router.delete("/log/{log_id}", response_model=dict)
def delete_log(log_id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return controller.remove_water_log(log_id, user_id)