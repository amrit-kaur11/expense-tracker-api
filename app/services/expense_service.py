import csv
import io
from typing import List, Optional
from sqlalchemy.orm import Session

from app.core.exceptions import EntityNotFoundException, ValidationException
from app.models.expense import Expense
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.storage_repository import StorageRepository
from app.schemas.expense import ExpenseCreate, ExpenseFilterParams, ExpenseResponse, ExpenseUpdate


class ExpenseService:
    def __init__(self, db: Session):
        self.db = db
        self.expense_repo = ExpenseRepository(db)
        self.category_repo = CategoryRepository(db)
        self.storage_repo = StorageRepository()

    def _to_response(self, expense: Expense) -> ExpenseResponse:
        """Convert Expense ORM model to ExpenseResponse schema with dynamic presigned URL."""
        signed_url = None
        if expense.bill_image_key:
            signed_url = self.storage_repo.generate_presigned_url(expense.bill_image_key)

        response = ExpenseResponse.model_validate(expense)
        response.bill_signed_url = signed_url
        return response

    def create_expense(self, user_id: int, expense_in: ExpenseCreate) -> ExpenseResponse:
        """Create a new expense for the authenticated user."""
        category = self.category_repo.get_by_id_and_user(expense_in.category_id, user_id)
        if not category:
            raise EntityNotFoundException(f"Category with ID {expense_in.category_id} not found or does not belong to you")

        expense = self.expense_repo.create_expense(
            user_id=user_id,
            category_id=expense_in.category_id,
            amount=expense_in.amount,
            description=expense_in.description,
            expense_date=expense_in.date
        )
        return self._to_response(expense)

    def get_expense(self, user_id: int, expense_id: int) -> ExpenseResponse:
        """Retrieve a specific expense by ID for the authenticated user."""
        expense = self.expense_repo.get_by_id_and_user(expense_id, user_id)
        if not expense:
            raise EntityNotFoundException(f"Expense with ID {expense_id} not found")
        return self._to_response(expense)

    def get_user_expenses(self, user_id: int, filters: ExpenseFilterParams) -> List[ExpenseResponse]:
        """Get filtered user expenses with pagination and dynamic signed URLs."""
        if filters.category_id:
            category = self.category_repo.get_by_id_and_user(filters.category_id, user_id)
            if not category:
                raise EntityNotFoundException(f"Category with ID {filters.category_id} not found")

        expenses = self.expense_repo.get_filtered_expenses(
            user_id=user_id,
            start_date=filters.start_date,
            end_date=filters.end_date,
            category_id=filters.category_id,
            limit=filters.limit,
            offset=filters.offset
        )
        return [self._to_response(exp) for exp in expenses]

    def update_expense(self, user_id: int, expense_id: int, expense_in: ExpenseUpdate) -> ExpenseResponse:
        """Update an existing expense."""
        expense = self.expense_repo.get_by_id_and_user(expense_id, user_id)
        if not expense:
            raise EntityNotFoundException(f"Expense with ID {expense_id} not found")

        if expense_in.category_id is not None:
            category = self.category_repo.get_by_id_and_user(expense_in.category_id, user_id)
            if not category:
                raise EntityNotFoundException(f"Category with ID {expense_in.category_id} not found")

        update_data = expense_in.model_dump(exclude_unset=True)
        updated_expense = self.expense_repo.update_expense_data(expense, **update_data)
        return self._to_response(updated_expense)

    def delete_expense(self, user_id: int, expense_id: int) -> None:
        """Delete an expense and remove its bill attachment from MinIO if present."""
        expense = self.expense_repo.get_by_id_and_user(expense_id, user_id)
        if not expense:
            raise EntityNotFoundException(f"Expense with ID {expense_id} not found")

        if expense.bill_image_key:
            self.storage_repo.delete_bill_image(expense.bill_image_key)

        self.expense_repo.delete(expense)

    def upload_bill_image(
        self,
        user_id: int,
        expense_id: int,
        file_bytes: bytes,
        filename: str,
        content_type: str
    ) -> ExpenseResponse:
        """Upload a bill image attachment to MinIO and persist the object key in DB."""
        expense = self.expense_repo.get_by_id_and_user(expense_id, user_id)
        if not expense:
            raise EntityNotFoundException(f"Expense with ID {expense_id} not found")

        if not content_type or not content_type.startswith("image/"):
            raise ValidationException("Only image files (JPEG, PNG, etc.) are allowed for bill uploads")

        # Delete previous image from MinIO if present
        if expense.bill_image_key:
            self.storage_repo.delete_bill_image(expense.bill_image_key)

        object_key = self.storage_repo.upload_bill_image(
            file_bytes=file_bytes,
            file_name=filename,
            content_type=content_type,
            user_id=user_id,
            expense_id=expense_id
        )

        updated_expense = self.expense_repo.update_bill_key(expense, object_key)
        return self._to_response(updated_expense)

    def export_expenses_csv(self, user_id: int, year: int, month: int) -> str:
        """Export user expenses for a given month as a CSV formatted string (Bonus Feature 2)."""
        expenses = self.expense_repo.get_monthly_expenses(user_id, year, month)

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Expense ID", "Date", "Category", "Amount", "Description", "Bill Attached"])

        for exp in expenses:
            category_name = exp.category.name if exp.category else "Uncategorized"
            has_bill = "Yes" if exp.bill_image_key else "No"
            writer.writerow([
                exp.id,
                exp.date.isoformat(),
                category_name,
                f"{exp.amount:.2f}",
                exp.description or "",
                has_bill
            ])

        return output.getvalue()
