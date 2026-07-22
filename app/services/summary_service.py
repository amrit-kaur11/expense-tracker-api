from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.budget_repository import BudgetRepository
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.summary import CategorySummary, MonthlySummaryResponse


class SummaryService:
    def __init__(self, db: Session):
        self.db = db
        self.expense_repo = ExpenseRepository(db)
        self.budget_repo = BudgetRepository(db)

    def get_monthly_summary(
        self,
        user_id: int,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> MonthlySummaryResponse:
        """
        Calculate total amount spent in current (or specified) month broken down by category.
        Includes monthly budget limits and evaluates 'exceeds_budget' warning flags.
        """
        now = datetime.now(timezone.utc)
        target_year = year or now.year
        target_month = month or now.month

        # Fetch spending totals per category for the specified month
        category_totals = self.expense_repo.get_monthly_category_totals(user_id, target_year, target_month)

        # Fetch configured category budgets for the user
        user_budgets = self.budget_repo.get_all_by_user(user_id)
        budget_map = {b.category_id: b.monthly_limit for b in user_budgets}

        breakdown = []
        overall_total = Decimal("0.00")

        for cat_id, cat_name, total_amount in category_totals:
            overall_total += total_amount
            monthly_budget = budget_map.get(cat_id)

            exceeds_budget = False
            if monthly_budget is not None and total_amount > monthly_budget:
                exceeds_budget = True

            breakdown.append(
                CategorySummary(
                    category_id=cat_id,
                    category_name=cat_name,
                    total_amount=total_amount,
                    monthly_budget=monthly_budget,
                    exceeds_budget=exceeds_budget
                )
            )

        return MonthlySummaryResponse(
            year=target_year,
            month=target_month,
            total_monthly_expenses=overall_total,
            categories_breakdown=breakdown
        )
