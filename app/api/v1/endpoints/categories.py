from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED, summary="Create category")
def create_category(
    category_in: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new custom expense category for the authenticated user."""
    category_service = CategoryService(db)
    return category_service.create_category(user_id=current_user.id, category_in=category_in)


@router.get("/", response_model=List[CategoryResponse], summary="List categories")
def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve all custom expense categories belonging to the authenticated user."""
    category_service = CategoryService(db)
    return category_service.get_user_categories(user_id=current_user.id)


@router.get("/{category_id}", response_model=CategoryResponse, summary="Get category details")
def get_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve details for a specific category by ID."""
    category_service = CategoryService(db)
    return category_service.get_category_by_id(user_id=current_user.id, category_id=category_id)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete category")
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a category by ID (expenses associated with this category will be handled according to DB constraints)."""
    category_service = CategoryService(db)
    category_service.delete_category(user_id=current_user.id, category_id=category_id)
    return None
