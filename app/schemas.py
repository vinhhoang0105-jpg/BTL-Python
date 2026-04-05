from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from app.models import ProjectStatus, UserRole, ProjectMemberRole

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    role: UserRole
    department: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProjectBase(BaseModel):
    title: str
    research_field: str
    budget: float = 0.0
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    research_field: Optional[str] = None
    budget: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None

class ProjectResponse(ProjectBase):
    id: UUID
    status: ProjectStatus
    leader_id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProjectMemberCreate(BaseModel):
    user_id: UUID
    role_in_project: ProjectMemberRole

class ProjectMemberResponse(BaseModel):
    user_id: UUID
    project_id: UUID
    role_in_project: ProjectMemberRole
    joined_at: datetime
    user: UserResponse
    model_config = ConfigDict(from_attributes=True)

class PublicationCreate(BaseModel):
    title: str
    journal_name: str
    publication_date: date
    file_url: Optional[str] = None

class PublicationResponse(PublicationCreate):
    id: UUID
    project_id: Optional[UUID]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
