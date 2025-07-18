from fastapi import APIRouter, Depends, Query
from .controller import get_daily_logs
from .models import DailySummary
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/summary", tags=["Summary"])

@router.get("/daily", response_model= DailySummary)
def daily_summary(date: str = Query(...), current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return get_daily_logs(user_id, date)
