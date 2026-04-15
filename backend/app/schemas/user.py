"""User request/response schemas."""

from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=200)
    phone: Optional[str] = None
    department_id: Optional[UUID] = None
    academic_rank: Optional[str] = None
    academic_title: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: str = Field(default="FACULTY", pattern="^(FACULTY|STAFF|LEADERSHIP|REVIEWER|ADMIN)$")


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=200)
    phone: Optional[str] = None
    department_id: Optional[UUID] = None
    academic_rank: Optional[str] = None
    academic_title: Optional[str] = None
    role: Optional[str] = Field(None, pattern="^(FACULTY|STAFF|LEADERSHIP|REVIEWER|ADMIN)$")
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: UUID
    role: str
    is_active: bool
    created_at: datetime
    department_name: Optional[str] = None

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    size: int
