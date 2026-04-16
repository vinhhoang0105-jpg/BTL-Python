"""User management endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.core.security import hash_password
from app.core.dependencies import get_current_user, require_roles
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/users", tags=["User Management"])


def _to_resp(user: User) -> UserResponse:
    return UserResponse(
        id=user.id, email=user.email, full_name=user.full_name,
        phone=user.phone, department_id=user.department_id,
        academic_rank=user.academic_rank, academic_title=user.academic_title,
        role=user.role, is_active=user.is_active, created_at=user.created_at,
        department_name=user.department.name if user.department else None,
    )


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    role: str | None = None,
    search: str | None = None,
    current_user: User = Depends(get_current_user),   # all authenticated
    db: Session = Depends(get_db),
):
    """List users. All authenticated users can list (for member/reviewer selection)."""
    query = db.query(User).options(joinedload(User.role_rel), joinedload(User.department))
    if role:
        query = query.join(User.role_rel).filter(Role.code == role)
    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%"))
        )
    total = query.count()
    users = query.order_by(User.full_name).offset((page - 1) * size).limit(size).all()
    return UserListResponse(items=[_to_resp(u) for u in users], total=total, page=page, size=size)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    body: UserCreate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Create a new user (Admin only)."""
    if db.query(User).filter(User.email == body.email).first():
        raise BadRequestException("Email đã tồn tại trong hệ thống")
    role_obj = db.query(Role).filter(Role.code == body.role).first()
    if not role_obj:
        raise BadRequestException(f"Vai trò '{body.role}' không hợp lệ")
    user = User(
        email=body.email, hashed_password=hash_password(body.password),
        full_name=body.full_name, phone=body.phone,
        department_id=body.department_id, academic_rank=body.academic_rank,
        academic_title=body.academic_title, role_id=role_obj.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user = db.query(User).options(joinedload(User.role_rel), joinedload(User.department)).filter(User.id == user.id).first()
    return _to_resp(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    user = db.query(User).options(joinedload(User.role_rel), joinedload(User.department)).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("Người dùng")
    return _to_resp(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    body: UserUpdate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    user = db.query(User).options(joinedload(User.role_rel), joinedload(User.department)).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("Người dùng")
    update_data = body.model_dump(exclude_unset=True)
    if "role" in update_data:
        role_obj = db.query(Role).filter(Role.code == update_data.pop("role")).first()
        if not role_obj:
            raise BadRequestException("Vai trò không hợp lệ")
        user.role_id = role_obj.id
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    user = db.query(User).options(joinedload(User.role_rel), joinedload(User.department)).filter(User.id == user.id).first()
    return _to_resp(user)
