from fastapi import APIRouter
from typing import Optional

from .models import SleepLogCreate,SleepLogResponse
from . import controller

router = APIRouter(prefix="/sleep", tags= ["Sleep Tracker"])


@router.post("/log", response_model= SleepLogResponse)
def create_log(log: SleepLogCreate):
    return controller.create_sleep_log(log)

@router.get("/logs", response_model= list[SleepLogResponse])
def get_logs(user_id: int, date: Optional[str]=None):
    return controller.get_sleep_logs(user_id, date)

@router.delete("/log/{log_id}")
def delete_log(log_id: int, user_id: int):
    message = controller.delete_sleep_log(log_id, user_id)
    return {"message": message}