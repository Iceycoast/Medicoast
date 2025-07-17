from fastapi import HTTPException, status
from .models import DailySummary
from .ai_summary import generate_daily_summary
from .db import fetch_logs, save_ai_summary, get_ai_summary
from .utils import extract_summary_from_logs
from typing import Any
from .constants import TRACKER_TABLES
import logging

logger = logging.getLogger(__name__)

def get_daily_logs(user_id: int, date: str) -> dict[str, Any]:
    
    try:

        summary: dict[str, Any] = {"date": date}
        has_logs = False

        # Step 1: Fetch and process all logs from the trackers

        for table in TRACKER_TABLES:
            logs = fetch_logs(table, user_id, date)
            if logs: has_logs = True
            summary.update(extract_summary_from_logs(table, logs))
        
        if not has_logs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tracker data found for this date.")

        # Step 2: Convert to Pydantic model

        daily_summary_model = DailySummary(**summary)


        # Step 3: Check for existing AI summary

        cached_summary = get_ai_summary(user_id, date)
        if cached_summary is None:
            ai_summary = generate_daily_summary(daily_summary_model)
            if ai_summary:
                save_ai_summary(user_id, date, ai_summary)
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate AI summary.")

        return summary
    except HTTPException:
        raise  # Reraise to let FastAPI handle it properly

    except Exception as e:
        logger.exception("Unexpected error while generating daily logs")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.") 