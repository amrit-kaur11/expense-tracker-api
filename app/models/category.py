from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.expense import Expense
    from app.models.budget import Budget


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Table constraints - duplicate category names per user prevented
    __table_args__ = (
        UniqueConstraint("name", "user_id", name="uq_category_name_user"),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="categories")
    expenses: Mapped[List["Expense"]] = relationship("Expense", back_populates="category", cascade="all, delete-orphan")
    budgets: Mapped[List["Budget"]] = relationship("Budget", back_populates="category", cascade="all, delete-orphan")
