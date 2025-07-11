from fastapi import APIRouter
from typing import Optional
from .models import MoodLogCreate, MoodLogResponse
from . import controller


router = APIRouter(prefix="/mood", tags=["Mood Tracker"])

@router.post("/log", response_model= MoodLogResponse)
def create_log(log:MoodLogCreate):
    return controller.create_mood_log(log)

@router.get("/logs", response_model=list[MoodLogResponse])
def get_logs(user_id:int, date:Optional[str]=None):
    return controller.get_mood_logs(user_id, date)

@router.delete("/log/{log_id}", response_model= dict)
def delete_log(log_id:int, user_id:int):
    return controller.remove_mood_log(log_id, user_id)
