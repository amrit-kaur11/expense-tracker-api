from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class CategorySummary(BaseModel):
    category_id: int = Field(..., example=1)
    category_name: str = Field(..., example="Groceries")
    total_amount: Decimal = Field(..., example=150.75, description="Total spent in this category for the specified month")
    monthly_budget: Optional[Decimal] = Field(None, example=200.00, description="Monthly budget limit if configured")
    exceeds_budget: bool = Field(False, description="Warning flag indicating if category expenditure exceeded its budget limit")


class MonthlySummaryResponse(BaseModel):
    year: int = Field(..., example=2026)
    month: int = Field(..., example=7)
    total_monthly_expenses: Decimal = Field(..., example=1250.50, description="Total expenses across all categories for the month")
    categories_breakdown: List[CategorySummary]
