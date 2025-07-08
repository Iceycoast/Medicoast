from fastapi import APIRouter, status, HTTPException
from typing import Optional
from app.trackers.meals_tracker.logic import (get_logs_by_user, create_meals_logs, delete_meal_log, MealsLogsCreate, MealsLogsResponse)

router = APIRouter(prefix="/meals",tags=["Meal Tracker"])

@router.post("/log", response_model=MealsLogsResponse, status_code=status.HTTP_201_CREATED)
def log_meal(meal_log: MealsLogsCreate):
    return create_meals_logs(meal_log)

@router.get("/logs", response_model=list[MealsLogsResponse])
def fetch_meal_logs(user_id: int, date:Optional[str] = None):
    return get_logs_by_user(user_id, date)

@router.delete("/log/{log_id}", status_code=status.HTTP_200_OK)
def delete_log(log_id: int, user_id:int):
    return delete_meal_log(log_id, user_id)