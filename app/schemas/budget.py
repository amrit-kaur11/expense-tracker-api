from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class BudgetBase(BaseModel):
    category_id: int = Field(..., example=1)
    monthly_limit: Decimal = Field(..., gt=0, example=500.00, description="Monthly spending limit for this category")


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    monthly_limit: Decimal = Field(..., gt=0, example=600.00)


class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    category_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
