"""Catalog endpoints: Departments and Research Fields."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.catalog import Department, ResearchField
from app.schemas.catalog import (
    DepartmentCreate, DepartmentUpdate, DepartmentResponse,
    ResearchFieldCreate, ResearchFieldUpdate, ResearchFieldResponse,
)
from app.core.dependencies import get_current_user, require_roles
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/catalog", tags=["Catalog"])


# ── Departments ──────────────────────────────────────────────────

@router.get("/departments", response_model=list[DepartmentResponse])
async def list_departments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all active departments."""
    return db.query(Department).filter(Department.is_active == True).order_by(Department.name).all()


@router.post("/departments", response_model=DepartmentResponse, status_code=201)
async def create_department(
    body: DepartmentCreate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Create a new department (Admin only)."""
    existing = db.query(Department).filter(
        (Department.name == body.name) | (Department.code == body.code)
    ).first()
    if existing:
        raise BadRequestException("Khoa/Phòng đã tồn tại")

    dept = Department(name=body.name, code=body.code)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


@router.put("/departments/{dept_id}", response_model=DepartmentResponse)
async def update_department(
    dept_id: UUID,
    body: DepartmentUpdate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Update a department (Admin only)."""
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise NotFoundException("Khoa/Phòng")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dept, field, value)

    db.commit()
    db.refresh(dept)
    return dept


# ── Research Fields ──────────────────────────────────────────────

@router.get("/research-fields", response_model=list[ResearchFieldResponse])
async def list_research_fields(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all active research fields."""
    return db.query(ResearchField).filter(ResearchField.is_active == True).order_by(ResearchField.name).all()


@router.post("/research-fields", response_model=ResearchFieldResponse, status_code=201)
async def create_research_field(
    body: ResearchFieldCreate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Create a new research field (Admin only)."""
    existing = db.query(ResearchField).filter(
        (ResearchField.name == body.name) | (ResearchField.code == body.code)
    ).first()
    if existing:
        raise BadRequestException("Lĩnh vực nghiên cứu đã tồn tại")

    field = ResearchField(name=body.name, code=body.code)
    db.add(field)
    db.commit()
    db.refresh(field)
    return field


@router.put("/research-fields/{field_id}", response_model=ResearchFieldResponse)
async def update_research_field(
    field_id: UUID,
    body: ResearchFieldUpdate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Update a research field (Admin only)."""
    field = db.query(ResearchField).filter(ResearchField.id == field_id).first()
    if not field:
        raise NotFoundException("Lĩnh vực nghiên cứu")

    update_data = body.model_dump(exclude_unset=True)
    for f, value in update_data.items():
        setattr(field, f, value)

    db.commit()
    db.refresh(field)
    return field
