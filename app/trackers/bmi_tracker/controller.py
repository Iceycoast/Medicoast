from typing import Optional
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.trackers.bmi_tracker.models import BMILogsCreate, BMILogsResponse
from app.trackers.bmi_tracker import db
from app.trackers.bmi_tracker.utils import calculate_bmi

def create_bmi_log(log: BMILogsCreate) -> BMILogsResponse:
    try:
        bmi, category = calculate_bmi(log.weight_kg, log.height_cm)
        created_at = datetime.now(timezone.utc).isoformat()
        log_id = db.insert_bmi_log(log, bmi, category, created_at)
        return BMILogsResponse(
            log_id=log_id,
            user_id=log.user_id,
            weight_kg=log.weight_kg,
            height_cm=log.height_cm,
            bmi=bmi,
            category=category,
            date=log.date
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))

def get_bmi_logs(user_id: int, date: Optional[str] = None) -> list[BMILogsResponse]:
    try:
        logs = db.fetch_bmi_logs_by_user(user_id, date)
        if not logs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No BMI logs found.")
        return logs
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))

def remove_bmi_log(log_id: int, user_id: int) -> dict:
    try:
        success = db.delete_bmi_log(log_id, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found or not authorized to delete.")
        return {"message": "BMI log deleted successfully."}
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re)) 