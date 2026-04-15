# SciRes MVP — Permissions & Functional Decomposition

> **Version:** 1.0  
> **Last Updated:** 2026-04-15  
> **Author:** Solution Architect  
> **Purpose:** Definitive reference for backend authorization and frontend route/UI gating.

---

## 1. Role Definitions

| Role Code | Vietnamese Name | English Name | Description |
|-----------|----------------|--------------|-------------|
| `FACULTY` | Giảng viên | Faculty | University lecturers/researchers who propose and execute research projects |
| `STAFF` | Cán bộ Phòng KHCN | S&T Department Staff | Officers managing the research lifecycle, validating dossiers, managing councils |
| `LEADERSHIP` | Lãnh đạo | Leadership | University leaders (Rector, Vice-Rector) who make final approval decisions |
| `REVIEWER` | Phản biện / Thành viên hội đồng | Reviewer | Experts assigned to evaluate proposals and acceptance dossiers |
| `ADMIN` | Quản trị hệ thống | System Admin | Technical administrator managing users, roles, and system catalogs |

### Role Assignment Rules (MVP)
- Each user has **exactly one primary role** (simplification for MVP).
- A user with `FACULTY` role can also be assigned as a `REVIEWER` for proposals they are NOT the PI or co-investigator of.
- `ADMIN` is a superuser — can access all data but does NOT participate in business workflows.
- Future: support multiple roles per user, role delegation, department-level admins.

---

## 2. Functional Decomposition

### 2.1 Module Map

```
MVP Functional Areas
├── F1: Authentication & Profile
│   ├── F1.1: Login (email + password → JWT)
│   ├── F1.2: View/Edit own profile
│   └── F1.3: Change password
│
├── F2: System Administration
│   ├── F2.1: User Management (CRUD + role assignment)
│   └── F2.2: Catalog Management (departments, research fields)
│
├── F3: Registration Period Management
│   ├── F3.1: Create registration period
│   ├── F3.2: Open / Close period
│   └── F3.3: View active periods
│
├── F4: Proposal Management
│   ├── F4.1: Create proposal (draft)
│   ├── F4.2: Edit proposal (while in DRAFT or REVISION_REQUESTED)
│   ├── F4.3: Submit proposal
│   ├── F4.4: View own proposals (Faculty)
│   ├── F4.5: View all proposals (Staff, Leadership, Admin)
│   └── F4.6: View proposal detail + status history
│
├── F5: Validation & Review
│   ├── F5.1: Validate proposal completeness (Staff)
│   ├── F5.2: Return proposal for revision (Staff)
│   ├── F5.3: Create review council
│   ├── F5.4: Assign reviewers to council
│   ├── F5.5: Submit review score + comments (Reviewer)
│   └── F5.6: View review results
│
├── F6: Approval
│   ├── F6.1: View pending approvals (Leadership)
│   ├── F6.2: Approve proposal
│   └── F6.3: Reject proposal (with reason)
│
├── F7: Progress Tracking
│   ├── F7.1: Submit progress report (Faculty)
│   ├── F7.2: View progress reports for a proposal
│   └── F7.3: Monitor all project progress (Staff, Leadership)
│
├── F8: Acceptance (Nghiệm thu)
│   ├── F8.1: Submit acceptance dossier (Faculty)
│   ├── F8.2: Validate acceptance dossier (Staff)
│   ├── F8.3: Create acceptance council
│   ├── F8.4: Submit acceptance review (Reviewer)
│   ├── F8.5: Confirm acceptance result (Leadership)
│   └── F8.6: View acceptance details
│
└── F9: Dashboard & Reports
    ├── F9.1: Faculty personal dashboard
    ├── F9.2: S&T university-wide dashboard
    ├── F9.3: Leadership KPI dashboard
    └── F9.4: Export summary report (CSV)
```

### 2.2 Use Case Summary per Module

| ID | Use Case | Primary Actor | Trigger |
|----|----------|---------------|---------|
| F1.1 | Login | Any user | User navigates to login page |
| F1.2 | View/Edit profile | Any user | User clicks profile |
| F1.3 | Change password | Any user | User clicks change password |
| F2.1 | Manage users | Admin | Admin opens user management |
| F2.2 | Manage catalogs | Admin | Admin opens catalog management |
| F3.1 | Create registration period | Staff | Staff opens period management |
| F3.2 | Open/Close period | Staff | Staff changes period status |
| F3.3 | View active periods | Faculty, Staff | User views available periods |
| F4.1 | Create proposal draft | Faculty | Faculty clicks "New Proposal" |
| F4.2 | Edit proposal | Faculty | Faculty edits draft/returned proposal |
| F4.3 | Submit proposal | Faculty | Faculty clicks "Submit" |
| F4.4 | View own proposals | Faculty | Faculty opens "My Proposals" |
| F4.5 | View all proposals | Staff, Leadership | Staff/Leadership opens proposal list |
| F4.6 | View proposal detail | Owner, Staff, Leadership | User clicks on a proposal |
| F5.1 | Validate proposal | Staff | Staff reviews submitted proposal |
| F5.2 | Return for revision | Staff | Staff finds issues in proposal |
| F5.3 | Create review council | Staff | Staff creates council after validation |
| F5.4 | Assign reviewers | Staff | Staff adds members to council |
| F5.5 | Submit review | Reviewer | Reviewer scores assigned proposal |
| F5.6 | View review results | Staff, Leadership | View aggregated scores |
| F6.1 | View pending approvals | Leadership | Leadership opens approval queue |
| F6.2 | Approve proposal | Leadership | Leadership clicks approve |
| F6.3 | Reject proposal | Leadership | Leadership clicks reject |
| F7.1 | Submit progress report | Faculty (PI) | Faculty submits periodic update |
| F7.2 | View progress reports | Owner, Staff, Leadership | User opens progress tab |
| F7.3 | Monitor all progress | Staff, Leadership | Staff opens tracking dashboard |
| F8.1 | Submit acceptance dossier | Faculty (PI) | Faculty submits final report |
| F8.2 | Validate acceptance dossier | Staff | Staff checks completeness |
| F8.3 | Create acceptance council | Staff | Staff creates acceptance council |
| F8.4 | Submit acceptance review | Reviewer | Reviewer scores acceptance |
| F8.5 | Confirm acceptance result | Leadership | Leadership confirms final result |
| F8.6 | View acceptance details | Owner, Staff, Leadership | User views acceptance info |
| F9.1 | Faculty dashboard | Faculty | Faculty opens dashboard |
| F9.2 | S&T dashboard | Staff | Staff opens dashboard |
| F9.3 | Leadership KPI | Leadership | Leadership opens dashboard |
| F9.4 | Export report | Staff, Leadership | User clicks export |

---

## 3. Role–Permission Matrix (Granular)

### Legend
| Symbol | Meaning |
|--------|---------|
| ✅ | Full access |
| 📖 | Read only |
| 🔒 | Own data only |
| ❌ | No access |
| ⚡ | Action (not CRUD) |

### 3.1 Authentication & Profile (F1)

| Permission | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|-----------|:-------:|:-----:|:----------:|:--------:|:-----:|
| Login | ✅ | ✅ | ✅ | ✅ | ✅ |
| View own profile | ✅ | ✅ | ✅ | ✅ | ✅ |
| Edit own profile | ✅ | ✅ | ✅ | ✅ | ✅ |
| Change own password | ✅ | ✅ | ✅ | ✅ | ✅ |

### 3.2 System Administration (F2)

| Permission | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|-----------|:-------:|:-----:|:----------:|:--------:|:-----:|
| List all users | ❌ | ❌ | ❌ | ❌ | ✅ |
| Create user | ❌ | ❌ | ❌ | ❌ | ✅ |
| Update user | ❌ | ❌ | ❌ | ❌ | ✅ |
| Deactivate user | ❌ | ❌ | ❌ | ❌ | ✅ |
| Assign role to user | ❌ | ❌ | ❌ | ❌ | ✅ |
| CRUD departments | ❌ | ❌ | ❌ | ❌ | ✅ |
| CRUD research fields | ❌ | ❌ | ❌ | ❌ | ✅ |
| View departments | 📖 | 📖 | 📖 | 📖 | ✅ |
| View research fields | 📖 | 📖 | 📖 | 📖 | ✅ |

### 3.3 Registration Periods (F3)

| Permission | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|-----------|:-------:|:-----:|:----------:|:--------:|:-----:|
| View active periods | 📖 | ✅ | 📖 | ❌ | ✅ |
| Create period | ❌ | ✅ | ❌ | ❌ | ✅ |
| Update period | ❌ | ✅ | ❌ | ❌ | ✅ |
| Open/Close period | ❌ | ⚡ | ❌ | ❌ | ⚡ |

### 3.4 Proposals (F4)

| Permission | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|-----------|:-------:|:-----:|:----------:|:--------:|:-----:|
| Create proposal | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit own proposal (DRAFT/REVISION_REQUESTED) | 🔒 | ❌ | ❌ | ❌ | ❌ |
| Delete own proposal (DRAFT only) | 🔒 | ❌ | ❌ | ❌ | ❌ |
| Submit own proposal | 🔒⚡ | ❌ | ❌ | ❌ | ❌ |
| View own proposals | 🔒 | ❌ | ❌ | ❌ | ❌ |
| View all proposals | ❌ | ✅ | ✅ | ❌ | ✅ |
| View assigned proposals | ❌ | ❌ | ❌ | 🔒 | ❌ |
| View proposal detail | 🔒 | ✅ | ✅ | 🔒 | ✅ |
| View status history | 🔒 | ✅ | ✅ | ❌ | ✅ |

### 3.5 Validation & Review (F5)

| Permission | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|-----------|:-------:|:-----:|:----------:|:--------:|:-----:|
| Validate proposal (pass/return) | ❌ | ⚡ | ❌ | ❌ | ❌ |
| Create review council | ❌ | ✅ | ❌ | ❌ | ❌ |
| Assign reviewer to council | ❌ | ✅ | ❌ | ❌ | ❌ |
| Remove reviewer from council | ❌ | ✅ | ❌ | ❌ | ❌ |
| View council details | ❌ | ✅ | 📖 | 🔒 | ✅ |
| Submit review score | ❌ | ❌ | ❌ | 🔒⚡ | ❌ |
| Edit own review (before deadline) | ❌ | ❌ | ❌ | 🔒 | ❌ |
| View all reviews for a proposal | ❌ | ✅ | 📖 | ❌ | ✅ |
| View own review only | ❌ | ❌ | ❌ | 🔒 | ❌ |

### 3.6 Approval (F6)

| Permission | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|-----------|:-------:|:-----:|:----------:|:--------:|:-----:|
| View pending approvals | ❌ | ❌ | ✅ | ❌ | ❌ |
| Approve proposal | ❌ | ❌ | ⚡ | ❌ | ❌ |
| Reject proposal | ❌ | ❌ | ⚡ | ❌ | ❌ |
| View approval history | ❌ | 📖 | ✅ | ❌ | ✅ |

### 3.7 Progress Tracking (F7)

| Permission | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|-----------|:-------:|:-----:|:----------:|:--------:|:-----:|
| Submit progress report | 🔒⚡ | ❌ | ❌ | ❌ | ❌ |
| View own progress reports | 🔒 | ❌ | ❌ | ❌ | ❌ |
| View all progress reports | ❌ | ✅ | 📖 | ❌ | ✅ |
| Monitor progress dashboard | ❌ | ✅ | 📖 | ❌ | ✅ |

### 3.8 Acceptance (F8)

| Permission | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|-----------|:-------:|:-----:|:----------:|:--------:|:-----:|
| Submit acceptance dossier | 🔒⚡ | ❌ | ❌ | ❌ | ❌ |
| View own acceptance dossier | 🔒 | ❌ | ❌ | ❌ | ❌ |
| Validate acceptance dossier | ❌ | ⚡ | ❌ | ❌ | ❌ |
| Create acceptance council | ❌ | ✅ | ❌ | ❌ | ❌ |
| Submit acceptance review | ❌ | ❌ | ❌ | 🔒⚡ | ❌ |
| Confirm acceptance result | ❌ | ❌ | ⚡ | ❌ | ❌ |
| View acceptance overview | ❌ | ✅ | 📖 | 🔒 | ✅ |

### 3.9 Dashboard & Reports (F9)

| Permission | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|-----------|:-------:|:-----:|:----------:|:--------:|:-----:|
| Faculty personal dashboard | ✅ | ❌ | ❌ | ❌ | ❌ |
| S&T university dashboard | ❌ | ✅ | ❌ | ❌ | ✅ |
| Leadership KPI dashboard | ❌ | ❌ | ✅ | ❌ | ✅ |
| Reviewer workload view | ❌ | ❌ | ❌ | ✅ | ❌ |
| Export CSV report | ❌ | ✅ | ✅ | ❌ | ✅ |

---

## 4. Authorization Implementation Guide

### 4.1 Backend Middleware Pattern

```python
# Decorator-based authorization (FastAPI dependency)
# Usage in route handlers:

@router.get("/proposals")
async def list_proposals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "FACULTY":
        return get_proposals_by_pi(db, current_user.id)
    elif current_user.role in ["STAFF", "LEADERSHIP", "ADMIN"]:
        return get_all_proposals(db)
    elif current_user.role == "REVIEWER":
        return get_assigned_proposals(db, current_user.id)
    raise HTTPException(403, "Access denied")
```

### 4.2 Permission Check Utility

```python
# core/permissions.py
PERMISSIONS = {
    "proposal:create": ["FACULTY"],
    "proposal:read_own": ["FACULTY"],
    "proposal:read_all": ["STAFF", "LEADERSHIP", "ADMIN"],
    "proposal:read_assigned": ["REVIEWER"],
    "proposal:submit": ["FACULTY"],          # + must be owner
    "proposal:validate": ["STAFF"],
    "proposal:approve": ["LEADERSHIP"],
    "council:create": ["STAFF"],
    "council:assign_reviewer": ["STAFF"],
    "review:submit": ["REVIEWER"],           # + must be assigned
    "progress:submit": ["FACULTY"],          # + must be PI
    "acceptance:submit": ["FACULTY"],        # + must be PI
    "acceptance:confirm": ["LEADERSHIP"],
    "user:manage": ["ADMIN"],
    "catalog:manage": ["ADMIN"],
    "period:manage": ["STAFF", "ADMIN"],
    "dashboard:faculty": ["FACULTY"],
    "dashboard:staff": ["STAFF", "ADMIN"],
    "dashboard:leadership": ["LEADERSHIP", "ADMIN"],
    "report:export": ["STAFF", "LEADERSHIP", "ADMIN"],
}

def check_permission(user_role: str, permission: str) -> bool:
    return user_role in PERMISSIONS.get(permission, [])
```

### 4.3 Frontend Route Gating

```javascript
// utils/roleRoutes.js
export const ROLE_ROUTES = {
  FACULTY: [
    '/dashboard',
    '/my-proposals',
    '/proposals/new',
    '/proposals/:id',
    '/proposals/:id/progress',
    '/proposals/:id/acceptance',
  ],
  STAFF: [
    '/dashboard',
    '/periods',
    '/proposals',
    '/proposals/:id',
    '/reviews',
    '/councils',
    '/progress',
    '/acceptance',
    '/reports',
  ],
  LEADERSHIP: [
    '/dashboard',
    '/approvals',
    '/proposals',
    '/proposals/:id',
    '/reports',
  ],
  REVIEWER: [
    '/dashboard',
    '/assigned',
    '/assigned/:id/review',
    '/councils/schedule',
  ],
  ADMIN: [
    '/dashboard',
    '/users',
    '/catalog',
    '/periods',
    // Admin can access all routes
  ],
};

export const getDefaultRoute = (role) => {
  return '/dashboard'; // All roles land on their role-specific dashboard
};
```

### 4.4 Sidebar Menu per Role

| Menu Item (Vietnamese) | Route | FACULTY | STAFF | LEADERSHIP | REVIEWER | ADMIN |
|----------------------|-------|:-------:|:-----:|:----------:|:--------:|:-----:|
| Tổng quan | `/dashboard` | ✅ | ✅ | ✅ | ✅ | ✅ |
| Đề tài của tôi | `/my-proposals` | ✅ | ❌ | ❌ | ❌ | ❌ |
| Tạo đề xuất | `/proposals/new` | ✅ | ❌ | ❌ | ❌ | ❌ |
| Báo cáo tiến độ | `/my-progress` | ✅ | ❌ | ❌ | ❌ | ❌ |
| Hồ sơ nghiệm thu | `/my-acceptance` | ✅ | ❌ | ❌ | ❌ | ❌ |
| Quản lý đợt đăng ký | `/periods` | ❌ | ✅ | ❌ | ❌ | ✅ |
| Danh sách hồ sơ | `/proposals` | ❌ | ✅ | ❌ | ❌ | ❌ |
| Quản lý xét duyệt | `/reviews` | ❌ | ✅ | ❌ | ❌ | ❌ |
| Quản lý hội đồng | `/councils` | ❌ | ✅ | ❌ | ❌ | ❌ |
| Theo dõi tiến độ | `/progress` | ❌ | ✅ | ❌ | ❌ | ❌ |
| Quản lý nghiệm thu | `/acceptance` | ❌ | ✅ | ❌ | ❌ | ❌ |
| Báo cáo tổng hợp | `/reports` | ❌ | ✅ | ✅ | ❌ | ✅ |
| Chờ phê duyệt | `/approvals` | ❌ | ❌ | ✅ | ❌ | ❌ |
| Hồ sơ được phân công | `/assigned` | ❌ | ❌ | ❌ | ✅ | ❌ |
| Lịch hội đồng | `/councils/schedule` | ❌ | ❌ | ❌ | ✅ | ❌ |
| Quản lý người dùng | `/users` | ❌ | ❌ | ❌ | ❌ | ✅ |
| Danh mục | `/catalog` | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 5. Data Access Scope Rules

These rules ensure users can only see data they're authorized for:

| Rule ID | Rule | Applies To |
|---------|------|------------|
| DA-1 | Faculty can only see proposals where they are PI or co-investigator | FACULTY |
| DA-2 | Reviewer can only see proposals assigned to them via council membership | REVIEWER |
| DA-3 | Staff can see ALL proposals across all departments | STAFF |
| DA-4 | Leadership can see ALL proposals (read-only except approval actions) | LEADERSHIP |
| DA-5 | Faculty can only submit progress/acceptance for proposals where they are PI | FACULTY |
| DA-6 | Reviewer can only submit reviews for councils they are a member of | REVIEWER |
| DA-7 | A user CANNOT be a reviewer for their own proposal | ALL |
| DA-8 | Admin can see all data but cannot perform business actions (approve, review, etc.) | ADMIN |
