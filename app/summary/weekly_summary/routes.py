from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from .pdf_generator.pdf_generator import generate_weekly_pdf
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/summary", tags=["Summary"])


@router.get("/weekly/pdf")
def weekly_pdf_route(user_full_name: str, start_date: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    pdf_bytes = generate_weekly_pdf(user_id, user_full_name, start_date)
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"inline; filename=weekly_summary_{user_id}_{start_date}.pdf"
        }
    )

@router.get("/weekly/pdf/download")
def weekly_pdf_download_route(user_full_name: str, start_date: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    pdf_bytes = generate_weekly_pdf(user_id, user_full_name, start_date)
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=weekly_summary_{user_id}_{start_date}.pdf"
        }
    )