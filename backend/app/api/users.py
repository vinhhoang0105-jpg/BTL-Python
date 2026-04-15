"""User management endpoints (Admin only)."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.core.security import hash_password
from app.core.dependencies import require_roles
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    role: str | None = None,
    search: str | None = None,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """List all users with pagination and optional filters."""
    query = db.query(User).options(joinedload(User.department))

    if role:
        query = query.filter(User.role == role)
    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%"))
        )

    total = query.count()
    users = query.offset((page - 1) * size).limit(size).all()

    return UserListResponse(
        items=[
            UserResponse(
                id=u.id, email=u.email, full_name=u.full_name, phone=u.phone,
                department_id=u.department_id, academic_rank=u.academic_rank,
                academic_title=u.academic_title, role=u.role, is_active=u.is_active,
                created_at=u.created_at,
                department_name=u.department.name if u.department else None,
            )
            for u in users
        ],
        total=total, page=page, size=size,
    )


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    body: UserCreate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Create a new user."""
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise BadRequestException("Email đã tồn tại trong hệ thống")

    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
        phone=body.phone,
        department_id=body.department_id,
        academic_rank=body.academic_rank,
        academic_title=body.academic_title,
        role=body.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id, email=user.email, full_name=user.full_name, phone=user.phone,
        department_id=user.department_id, academic_rank=user.academic_rank,
        academic_title=user.academic_title, role=user.role, is_active=user.is_active,
        created_at=user.created_at, department_name=None,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Get user by ID."""
    user = db.query(User).options(joinedload(User.department)).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("Người dùng")

    return UserResponse(
        id=user.id, email=user.email, full_name=user.full_name, phone=user.phone,
        department_id=user.department_id, academic_rank=user.academic_rank,
        academic_title=user.academic_title, role=user.role, is_active=user.is_active,
        created_at=user.created_at,
        department_name=user.department.name if user.department else None,
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    body: UserUpdate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Update an existing user."""
    user = db.query(User).options(joinedload(User.department)).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("Người dùng")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id, email=user.email, full_name=user.full_name, phone=user.phone,
        department_id=user.department_id, academic_rank=user.academic_rank,
        academic_title=user.academic_title, role=user.role, is_active=user.is_active,
        created_at=user.created_at,
        department_name=user.department.name if user.department else None,
    )
