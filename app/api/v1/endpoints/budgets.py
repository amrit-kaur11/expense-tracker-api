from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetResponse
from app.services.budget_service import BudgetService

router = APIRouter()


@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_200_OK, summary="Set category budget limit")
def set_budget(
    budget_in: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set or update monthly spending budget limit for a specific category (Bonus Feature 1)."""
    budget_service = BudgetService(db)
    return budget_service.set_category_budget(user_id=current_user.id, budget_in=budget_in)


@router.get("/", response_model=List[BudgetResponse], summary="List user budgets")
def get_budgets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve all category budget limits configured by the authenticated user."""
    budget_service = BudgetService(db)
    return budget_service.get_user_budgets(user_id=current_user.id)
