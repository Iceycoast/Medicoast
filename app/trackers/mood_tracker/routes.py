from fastapi import APIRouter, Depends
from .models import MoodLogCreate, MoodLogResponse
from . import controller
from app.auth.dependencies import get_current_user
from typing import Optional

router = APIRouter(prefix="/mood", tags=["Mood Tracker"])

@router.post("/log", response_model=MoodLogResponse)
def create_log(log: MoodLogCreate):
    return controller.create_mood_log(log)

@router.get("/logs", response_model=list[MoodLogResponse])
def get_logs(current_user: dict = Depends(get_current_user), date: Optional[str]=None):
    user_id = current_user["user_id"]
    return controller.get_mood_logs(user_id, date)

@router.delete("/log/{log_id}", response_model=dict)
def delete_log(log_id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return controller.remove_mood_log(log_id, user_id)
