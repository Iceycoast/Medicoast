from fastapi import APIRouter
from .models import WeeklySummaryResponse
from .controller import get_weekly_summary

router = APIRouter(prefix="/summary", tags=["Summary"])

@router.get("/weekly", response_model=WeeklySummaryResponse)
def weekly_summary_route(user_id: int, start_date: str ):
    return get_weekly_summary(user_id, start_date)