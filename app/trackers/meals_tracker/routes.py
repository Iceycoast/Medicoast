from fastapi import APIRouter
from typing import Optional
from .models import MealLogCreate, MealLogResponse
from . import controller


router = APIRouter(prefix="/meals", tags=["Meal Tracker"])


@router.post("/log", response_model=MealLogResponse)
def create_meal_log(log: MealLogCreate):
    return controller.create_meal_log(log)


@router.get("/logs", response_model=list[MealLogResponse])
def get_meal_logs(user_id: int, date: Optional[str] = None):
    return controller.get_meal_logs(user_id, date)


@router.delete("/log/{log_id}")
def delete_meal_log(log_id: int, user_id: int):
    controller.delete_meal_log(log_id, user_id)
    return {"message": "Meal log deleted successfully."}
