from datetime import datetime, timezone
from fastapi import HTTPException, status
from . import db
from .models import MealLogCreate, MealLogResponse


def create_meal_log(log: MealLogCreate) -> MealLogResponse:
    try:
        if log.date is None:
            log.date = datetime.now().strftime("%Y-%m-%d")
        if log.time is None:
            log.time = datetime.now().strftime("%I:%M %p")
        created_at = datetime.now(timezone.utc).isoformat()
        log_id = db.insert_meal_log(log, created_at)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))

    return MealLogResponse(
        log_id=log_id,
        user_id=log.user_id,
        meal_name=log.meal_name,
        calories=log.calories,
        meal_type=log.meal_type,
        date=log.date,
        time=log.time
    )


def get_meal_logs(user_id: int, date: str | None = None) -> list[MealLogResponse]:
    try:
        logs = db.fetch_meal_logs_by_user(user_id, date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch logs: {e}")

    if not logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No meal logs found for this user.")
    
    return logs


def delete_meal_log(log_id: int, user_id: int) -> None:
    deleted = db.delete_meal_log(log_id, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found or doesn't belong to the user.")
