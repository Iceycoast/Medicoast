from typing import Optional
from datetime import datetime, timezone
from fastapi import HTTPException, status
from .models import WaterLogCreate, WaterLogResponse
from . import db



def create_water_log(log:WaterLogCreate) -> WaterLogResponse:
    
    try:
        created_at = datetime.now(timezone.utc).isoformat()

        if log.date is None:
            log.date = datetime.now().strftime("%Y-%m-%d")

        if log.time is None:
            log.time = datetime.now().strftime("%H:%M")

        log_id = db.insert_into_water_log(log, created_at)

        return WaterLogResponse(
            log_id=log_id,
            user_id=log.user_id,
            date= log.date,
            time = log.time,
            quantity_ml= log.quantity_ml
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
        

def get_water_logs(user_id:int, date:Optional[str]= None) -> list[WaterLogResponse]:

    try:
        logs = db.fetch_logs_by_user(user_id, date)

        if not logs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No water logs found.")
        return logs
    
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))  

def remove_water_log(log_id:int, user_id:int) -> dict:
    try:
        success = db.delete_water_log(log_id, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found or not authorized to delete.")

        return {"message": "Water log deleted successfully."}

    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))