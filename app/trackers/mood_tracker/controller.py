from datetime import datetime, timezone
from fastapi import HTTPException, status
from typing import Optional
from .models import MoodLogCreate, MoodLogResponse
from . import db
from .ai_utils import get_ai_sentiment_and_suggestion

def create_mood_log(log:MoodLogCreate) -> MoodLogResponse:

    try:
        created_at = datetime.now(timezone.utc).isoformat()

        if log.date is None:
            log.date = datetime.now().strftime("%Y-%m-%d")

        if log.time is None:
            log.time = datetime.now().strftime("%H:%M")

        ai_sentiment, ai_suggestion = get_ai_sentiment_and_suggestion(log.mood, log.note)
        log_id  = db.insert_mood_log(log, ai_sentiment, ai_suggestion, created_at)

        return MoodLogResponse(
            log_id=log_id,
            user_id=log.user_id,
            mood=log.mood,
            note=log.note,
            ai_sentiment=ai_sentiment,
            ai_suggestion=ai_suggestion,
            date=log.date,
            time= log.time
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))

    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
    

def get_mood_logs(user_id: int, date: Optional[str] = None) -> list[MoodLogResponse]:
    try:
        logs =  db.fetch_mood_logs_by_user(user_id=user_id, date=date)

        if not logs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Mood logs found.")
        return logs
    
    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
    
    
def remove_mood_log(log_id: int, user_id: int) -> dict:
    try:
        success = db.delete_mood_log(log_id, user_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found or not authorized to delete.")

        return {"message": "Mood log deleted successfully."}

    except RuntimeError as re:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(re))
