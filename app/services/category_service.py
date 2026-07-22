from typing import List
from sqlalchemy.orm import Session

from app.core.exceptions import EntityAlreadyExistsException, EntityNotFoundException
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repo = CategoryRepository(db)

    def create_category(self, user_id: int, category_in: CategoryCreate) -> Category:
        """Create a new custom category for the user."""
        existing = self.category_repo.get_by_name_and_user(category_in.name, user_id)
        if existing:
            raise EntityAlreadyExistsException(f"Category '{category_in.name}' already exists")

        return self.category_repo.create_category(name=category_in.name, user_id=user_id)

    def get_user_categories(self, user_id: int) -> List[Category]:
        """Get all custom categories for the authenticated user."""
        return self.category_repo.get_all_by_user(user_id)

    def get_category_by_id(self, user_id: int, category_id: int) -> Category:
        """Get a single category by ID, verifying user ownership."""
        category = self.category_repo.get_by_id_and_user(category_id, user_id)
        if not category:
            raise EntityNotFoundException(f"Category with ID {category_id} not found")
        return category

    def delete_category(self, user_id: int, category_id: int) -> None:
        """Delete a category belonging to the authenticated user."""
        category = self.get_category_by_id(user_id, category_id)
        self.category_repo.delete(category)
