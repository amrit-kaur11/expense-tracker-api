from datetime import date
from decimal import Decimal
from typing import List, Optional, Tuple
from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.expense import Expense
from app.repositories.base import BaseRepository


class ExpenseRepository(BaseRepository[Expense]):
    def __init__(self, db: Session):
        super().__init__(Expense, db)

    def get_by_id_and_user(self, expense_id: int, user_id: int) -> Optional[Expense]:
        """Fetch an expense by ID ensuring it belongs to the authenticated user."""
        return self.db.query(Expense).filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        ).first()

    def get_filtered_expenses(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        category_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Expense]:
        """Fetch user expenses with optional date range and category filtering."""
        query = self.db.query(Expense).filter(Expense.user_id == user_id)

        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        if category_id:
            query = query.filter(Expense.category_id == category_id)

        return query.order_by(Expense.date.desc(), Expense.id.desc()).offset(offset).limit(limit).all()

    def create_expense(
        self,
        user_id: int,
        category_id: int,
        amount: Decimal,
        description: Optional[str],
        expense_date: date
    ) -> Expense:
        """Create and persist a new expense."""
        expense = Expense(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            description=description,
            date=expense_date
        )
        return self.create(expense)

    def update_expense_data(self, expense: Expense, **kwargs) -> Expense:
        """Update fields on an existing expense instance."""
        for key, value in kwargs.items():
            if value is not None and hasattr(expense, key):
                setattr(expense, key, value)
        return self.update(expense)

    def update_bill_key(self, expense: Expense, bill_image_key: str) -> Expense:
        """Update the MinIO bill image object key reference."""
        expense.bill_image_key = bill_image_key
        return self.update(expense)

    def get_monthly_category_totals(self, user_id: int, year: int, month: int) -> List[Tuple[int, str, Decimal]]:
        """
        Aggregate total expenditure per category for a specific month/year.
        Returns list of (category_id, category_name, sum_amount).
        """
        results = self.db.query(
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            func.coalesce(func.sum(Expense.amount), 0).label("total_amount")
        ).join(
            Expense, Expense.category_id == Category.id
        ).filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).group_by(
            Category.id, Category.name
        ).all()

        return [(r.category_id, r.category_name, Decimal(str(r.total_amount))) for r in results]

    def get_monthly_expenses(self, user_id: int, year: int, month: int) -> List[Expense]:
        """Fetch all expenses for a given user in a specified month/year for CSV export."""
        return self.db.query(Expense).filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).order_by(Expense.date.asc()).all()
