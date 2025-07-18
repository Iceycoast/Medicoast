from fastapi import APIRouter, Query
from .controller import get_daily_logs
from .models import DailySummary

router = APIRouter(prefix="/summary", tags=["Summary"])

@router.get("/daily", response_model=DailySummary)
def daily_summary(user_id: int = Query(...), date: str = Query(...)):
    return get_daily_logs(user_id, date)
