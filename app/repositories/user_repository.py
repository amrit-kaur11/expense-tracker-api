from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Find user record by email address."""
        return self.db.query(User).filter(User.email == email.lower().strip()).first()

    def create_user(self, name: str, email: str, password_hash: str) -> User:
        """Create and persist a new user instance."""
        user = User(
            name=name.strip(),
            email=email.lower().strip(),
            password_hash=password_hash
        )
        return self.create(user)
