from datetime import date, datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, File, Query, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseFilterParams, ExpenseResponse, ExpenseUpdate
from app.services.expense_service import ExpenseService

router = APIRouter()


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED, summary="Create expense")
def create_expense(
    expense_in: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new expense entry linked to a category."""
    expense_service = ExpenseService(db)
    return expense_service.create_expense(user_id=current_user.id, expense_in=expense_in)


@router.get("/", response_model=List[ExpenseResponse], summary="List/filter expenses")
def get_expenses(
    start_date: Optional[date] = Query(None, description="Filter expenses from this date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter expenses up to this date (YYYY-MM-DD)"),
    category_id: Optional[int] = Query(None, description="Filter expenses by category ID"),
    limit: int = Query(50, ge=1, le=100, description="Pagination limit"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve filtered user expenses with pagination support and dynamic signed bill URLs."""
    filters = ExpenseFilterParams(
        start_date=start_date,
        end_date=end_date,
        category_id=category_id,
        limit=limit,
        offset=offset
    )
    expense_service = ExpenseService(db)
    return expense_service.get_user_expenses(user_id=current_user.id, filters=filters)


@router.get("/export/csv", summary="Export expenses to CSV")
def export_expenses_csv(
    year: Optional[int] = Query(None, description="Target year (e.g. 2026)"),
    month: Optional[int] = Query(None, ge=1, le=12, description="Target month (1-12)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download user expenses for a given month as a CSV file (Bonus Feature 2)."""
    now = datetime.now(timezone.utc)
    target_year = year or now.year
    target_month = month or now.month

    expense_service = ExpenseService(db)
    csv_data = expense_service.export_expenses_csv(user_id=current_user.id, year=target_year, month=target_month)

    filename = f"expenses_{target_year}_{target_month:02d}.csv"
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/{expense_id}", response_model=ExpenseResponse, summary="Get expense details with signed bill URL")
def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve detailed expense record including dynamic presigned GET URL for bill attachment."""
    expense_service = ExpenseService(db)
    return expense_service.get_expense(user_id=current_user.id, expense_id=expense_id)


@router.put("/{expense_id}", response_model=ExpenseResponse, summary="Update expense")
def update_expense(
    expense_id: int,
    expense_in: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update details of an existing expense."""
    expense_service = ExpenseService(db)
    return expense_service.update_expense(user_id=current_user.id, expense_id=expense_id, expense_in=expense_in)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete expense")
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an expense record and its MinIO bill image attachment."""
    expense_service = ExpenseService(db)
    expense_service.delete_expense(user_id=current_user.id, expense_id=expense_id)
    return None


@router.post("/{expense_id}/bill", response_model=ExpenseResponse, summary="Upload bill image for expense")
async def upload_bill_image(
    expense_id: int,
    file: UploadFile = File(..., description="Multipart bill/receipt image file"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a bill receipt image to MinIO for an expense and return updated expense with signed URL."""
    file_bytes = await file.read()
    expense_service = ExpenseService(db)
    return expense_service.upload_bill_image(
        user_id=current_user.id,
        expense_id=expense_id,
        file_bytes=file_bytes,
        filename=file.filename or "receipt.jpg",
        content_type=file.content_type or "image/jpeg"
    )
