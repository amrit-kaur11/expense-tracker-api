from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.repositories.base import BaseRepository


class BudgetRepository(BaseRepository[Budget]):
    def __init__(self, db: Session):
        super().__init__(Budget, db)

    def get_by_user_and_category(self, user_id: int, category_id: int) -> Optional[Budget]:
        """Fetch budget limit for a specific category belonging to user."""
        return self.db.query(Budget).filter(
            Budget.user_id == user_id,
            Budget.category_id == category_id
        ).first()

    def get_all_by_user(self, user_id: int) -> List[Budget]:
        """Fetch all category budget limits set by user."""
        return self.db.query(Budget).filter(Budget.user_id == user_id).all()

    def set_budget(self, user_id: int, category_id: int, monthly_limit: Decimal) -> Budget:
        """Create new budget limit or update existing limit for a user's category."""
        existing = self.get_by_user_and_category(user_id, category_id)
        if existing:
            existing.monthly_limit = monthly_limit
            return self.update(existing)

        budget = Budget(
            user_id=user_id,
            category_id=category_id,
            monthly_limit=monthly_limit
        )
        return self.create(budget)
