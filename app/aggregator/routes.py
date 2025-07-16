from fastapi import APIRouter, Query, HTTPException
from .controller import get_daily_logs
from .models import DailySummary

router = APIRouter(prefix="/summary", tags=["Aggregator"])

@router.get("/daily", response_model=DailySummary)
def daily_summary(user_id: int = Query(...), date: str = Query(...)):
    summary = get_daily_logs(user_id, date)

    # Check if all logs are empty (excluding date and ai_summary)
    logs_empty = all(
        key in ["date", "ai_summary"] or summary.get(key) is None
        for key in summary
    )
    if logs_empty:
        raise HTTPException(status_code=404, detail="No logs found for the given date.")

    return summary
