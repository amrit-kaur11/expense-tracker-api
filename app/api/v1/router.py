from fastapi import APIRouter

from app.api.v1.endpoints import auth, budgets, categories, expenses, summary

api_router = APIRouter()

# Include sub-routers with respective path prefixes and OpenAPI tags
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["Budgets"])
api_router.include_router(summary.router, prefix="/summary", tags=["Summary"])
