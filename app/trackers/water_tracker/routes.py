from fastapi import APIRouter
from typing import Optional
from app.trackers.water_tracker.logic import (add_water_log, delete_water_log, get_water_logs_by_user, WaterLogCreate, WaterLogResponse)

router = APIRouter(prefix="/water", tags=["Water Tracker"])

@router.post("/log", response_model=WaterLogResponse)
def log_water(log:WaterLogCreate):
    return add_water_log(log)

@router.get("/log", response_model= list[WaterLogResponse])
def get_logs(user_id:int, date:Optional[str] = None):
    return get_water_logs_by_user(user_id, date)

@router.delete("/log/{log_id}")
def delete_log(log_id:int, user_id: int):
    return delete_water_log(log_id, user_id)