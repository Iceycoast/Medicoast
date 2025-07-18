from fastapi import APIRouter, Depends
from typing import Optional

from .models import SleepLogCreate,SleepLogResponse
from . import controller
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/sleep", tags= ["Sleep Tracker"])


@router.post("/log", response_model= SleepLogResponse)
def create_log(log: SleepLogCreate):
    return controller.create_sleep_log(log)

@router.get("/logs", response_model= list[SleepLogResponse])
def get_logs(current_user: dict = Depends(get_current_user), date: Optional[str]=None):
    user_id = current_user["user_id"]
    return controller.get_sleep_logs(user_id, date)

@router.delete("/log/{log_id}", response_model=dict)
def delete_log(log_id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    message = controller.delete_sleep_log(log_id, user_id)
    return {"message": message}