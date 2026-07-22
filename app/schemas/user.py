from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, example="securepassword123")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., example="securepassword123")


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
