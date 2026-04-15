"""Catalog request/response schemas."""

from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    code: str = Field(..., min_length=2, max_length=20)


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    code: Optional[str] = Field(None, min_length=2, max_length=20)
    is_active: Optional[bool] = None


class DepartmentResponse(DepartmentBase):
    id: UUID
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ResearchFieldBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    code: str = Field(..., min_length=2, max_length=20)


class ResearchFieldCreate(ResearchFieldBase):
    pass


class ResearchFieldUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    code: Optional[str] = Field(None, min_length=2, max_length=20)
    is_active: Optional[bool] = None


class ResearchFieldResponse(ResearchFieldBase):
    id: UUID
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
