from datetime import datetime, timezone
from fastapi import HTTPException, status
from .models import SleepLogCreate, SleepLogResponse
from .utils import calculate_sleep_duration
from . import db
from typing import Optional

def create_sleep_log(log: SleepLogCreate) -> SleepLogResponse:

    try:
        duration = calculate_sleep_duration(log.sleep_time, log.wake_time)
        created_at = datetime.now(timezone.utc).isoformat()
        log_id = db.insert_sleep_log(log, duration, created_at)

        return SleepLogResponse(
            log_id= log_id,
            user_id= log.user_id,
            date= log.date,
            sleep_time= log.sleep_time,
            wake_time= log.wake_time,
            duration= duration
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(e))
    
    except RuntimeError as r:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r))
    
def get_sleep_logs(user_id: int, date:Optional[str] = None) -> list[SleepLogResponse]:

    try:
        logs =  db.fetch_sleep_logs_by_user(user_id, date)

        if not logs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sleep logs found.")

        return logs
    
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))



def delete_sleep_log(log_id: int, user_id: int) -> dict:

    deleted = db.delete_sleep_log(log_id, user_id)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sleep Log not found.")
    
    return {"message": "Sleep Log Deleted Successfully."}