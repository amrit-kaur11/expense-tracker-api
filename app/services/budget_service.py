from typing import List, Optional
from sqlalchemy.orm import Session

from app.core.exceptions import EntityNotFoundException
from app.models.budget import Budget
from app.repositories.budget_repository import BudgetRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.budget import BudgetCreate, BudgetResponse


class BudgetService:
    def __init__(self, db: Session):
        self.db = db
        self.budget_repo = BudgetRepository(db)
        self.category_repo = CategoryRepository(db)

    def _to_response(self, budget: Budget) -> BudgetResponse:
        """Convert Budget model to BudgetResponse schema with category name."""
        category = self.category_repo.get_by_id_and_user(budget.category_id, budget.user_id)
        category_name = category.name if category else None
        
        response = BudgetResponse.model_validate(budget)
        response.category_name = category_name
        return response

    def set_category_budget(self, user_id: int, budget_in: BudgetCreate) -> BudgetResponse:
        """Set or update monthly budget limit for a category."""
        category = self.category_repo.get_by_id_and_user(budget_in.category_id, user_id)
        if not category:
            raise EntityNotFoundException(f"Category with ID {budget_in.category_id} not found")

        budget = self.budget_repo.set_budget(
            user_id=user_id,
            category_id=budget_in.category_id,
            monthly_limit=budget_in.monthly_limit
        )
        return self._to_response(budget)

    def get_user_budgets(self, user_id: int) -> List[BudgetResponse]:
        """Get all monthly budget limits defined by user."""
        budgets = self.budget_repo.get_all_by_user(user_id)
        return [self._to_response(b) for b in budgets]

    def get_category_budget(self, user_id: int, category_id: int) -> Optional[BudgetResponse]:
        """Get budget limit for a specific user category."""
        budget = self.budget_repo.get_by_user_and_category(user_id, category_id)
        if not budget:
            return None
        return self._to_response(budget)
