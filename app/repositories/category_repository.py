from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(Category, db)

    def get_by_id_and_user(self, category_id: int, user_id: int) -> Optional[Category]:
        """Fetch category by id ensuring it belongs to the authenticated user."""
        return self.db.query(Category).filter(
            Category.id == category_id,
            Category.user_id == user_id
        ).first()

    def get_by_name_and_user(self, name: str, user_id: int) -> Optional[Category]:
        """Check if a category with given name already exists for the user."""
        return self.db.query(Category).filter(
            Category.name.ilike(name.strip()),
            Category.user_id == user_id
        ).first()

    def get_all_by_user(self, user_id: int) -> List[Category]:
        """Fetch all custom categories for the given user."""
        return self.db.query(Category).filter(Category.user_id == user_id).order_by(Category.name).all()

    def create_category(self, name: str, user_id: int) -> Category:
        """Create a new custom category for a user."""
        category = Category(name=name.strip(), user_id=user_id)
        return self.create(category)
