from datetime import date as DateType, datetime as DateTimeType
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ExpenseBase(BaseModel):
    amount: Decimal = Field(..., gt=0, example=45.50, description="Amount spent")
    description: Optional[str] = Field(None, max_length=255, example="Weekly grocery shopping")
    date: DateType = Field(..., example="2026-07-22")
    category_id: int = Field(..., example=1)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0, example=50.00)
    description: Optional[str] = Field(None, max_length=255, example="Updated grocery list")
    date: Optional[DateType] = Field(None, example="2026-07-22")
    category_id: Optional[int] = Field(None, example=1)


class ExpenseResponse(ExpenseBase):
    id: int
    user_id: int
    bill_image_key: Optional[str] = None
    bill_signed_url: Optional[str] = None
    created_at: DateTimeType
    updated_at: DateTimeType

    model_config = ConfigDict(from_attributes=True)


class ExpenseFilterParams(BaseModel):
    start_date: Optional[DateType] = None
    end_date: Optional[DateType] = None
    category_id: Optional[int] = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
