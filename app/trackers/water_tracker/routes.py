from fastapi import APIRouter
from typing import Optional
from . import controller
from .models import WaterLogCreate, WaterLogResponse

router = APIRouter(prefix="/water", tags=["Water Tracker"])

@router.post("/log", response_model=WaterLogResponse)
def log_water(log:WaterLogCreate):
    return controller.create_water_log(log)

@router.get("/log", response_model= list[WaterLogResponse])
def get_logs(user_id:int, date:Optional[str] = None):
    return controller.get_water_logs(user_id, date)

@router.delete("/log/{log_id}", response_model=dict)
def delete_log(log_id:int, user_id: int):
    return controller.remove_water_log(log_id, user_id)