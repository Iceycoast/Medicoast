from datetime import datetime, timezone
from fastapi import HTTPException, status
from .models import MedicationLogCreate, MedicationLogResponse
from . import db
from typing import Optional


def create_medication_log(log:MedicationLogCreate) -> MedicationLogResponse:

    try:
        created_at = datetime.now(timezone.utc).isoformat()
        log_id = db.insert_medication_log(log, created_at)

        return MedicationLogResponse(
            log_id=log_id,
            user_id=log.user_id,
            medication_name= log.medication_name,
            dosage=log.dosage,
            date= log.date,
            time= log.time
        )
    except ValueError as ve: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
    
def get_medication_logs(user_id: int, date: Optional[str]= None) -> list[MedicationLogResponse]:
    
    try:
        logs =  db.fetch_medication_logs_by_user(user_id, date)

        if not logs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No medication logs found.")

        return logs
    
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
    

def remove_medication_log(log_id: int, user_id: int) -> dict:

    try:
        success = db.delete_medication_log(log_id, user_id)

        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found or not authorized to delete")
        
        return {"message" : "Medication Log Deleted Successfully"}
    
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))