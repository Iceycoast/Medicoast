from datetime import datetime, timezone
from fastapi import HTTPException, status
from .models import SleepLogCreate, SleepLogResponse
from .utils import calculate_sleep_duration, map_row_to_sleep_response
from . import db
from typing import Optional

def create_sleep_log(log: SleepLogCreate) -> SleepLogResponse:

    try:
        duration = calculate_sleep_duration(log.sleep_time, log.wake_time)
        created_at = datetime.now(timezone.utc).isoformat()

        data = log.model_dump()
        data["duration"] = duration
        data["created_at"] = created_at

        log_id = db.insert_sleep_log(**data)

        return SleepLogResponse(
            log_id= log_id,
            **log.model_dump(),
            duration= duration
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= str(e))
    
    except RuntimeError as r:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(r))
    
def get_sleep_logs(user_id: int, date:Optional[str] = None) -> list[SleepLogResponse]:

    rows = db.fetch_sleep_logs_by_user(user_id, date)

    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sleep logs found.")

    return [map_row_to_sleep_response(row) for row in rows]


def delete_sleep_log(log_id: int, user_id: int) -> str:

    deleted = db.delete_sleep_log(log_id, user_id)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sleep Log not found.")
    
    return "Sleep Log Deleted Successfully."