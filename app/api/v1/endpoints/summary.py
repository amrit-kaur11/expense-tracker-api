from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.summary import MonthlySummaryResponse
from app.services.summary_service import SummaryService

router = APIRouter()


@router.get("/monthly", response_model=MonthlySummaryResponse, summary="Get monthly expense summary")
def get_monthly_summary(
    year: Optional[int] = Query(None, description="Target year (defaults to current year)"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Target month (defaults to current month)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve total expenses spent in the current (or specified) month,
    broken down by category with budget limit warning indicators (Core Requirement 5 + Bonus Feature 1).
    """
    summary_service = SummaryService(db)
    return summary_service.get_monthly_summary(user_id=current_user.id, year=year, month=month)
