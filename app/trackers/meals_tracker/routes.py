from fastapi import APIRouter, Depends
from .models import MealLogCreate, MealLogResponse
from . import controller
from app.auth.dependencies import get_current_user
from typing import Optional

router = APIRouter(prefix="/meals", tags=["Meal Tracker"])

@router.post("/log", response_model=MealLogResponse)
def create_log(log: MealLogCreate):
    return controller.create_meal_log(log)

@router.get("/logs", response_model=list[MealLogResponse])
def get_meal_logs(current_user: dict = Depends(get_current_user), date: Optional[str] = None):
    user_id = current_user["user_id"]
    return controller.get_meal_logs(user_id, date)

@router.delete("/log/{log_id}")
def delete_meal_log(log_id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return controller.delete_meal_log(log_id, user_id)
