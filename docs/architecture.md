# SciRes — Architecture Document

> Version 1.0 | MVP Architecture

## 1. System Overview

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │────▶│   Backend    │────▶│  PostgreSQL  │
│  React/Vite  │ API │   FastAPI    │ SQL │     16       │
│  Port 3000   │◀────│  Port 8000   │◀────│  Port 5432   │
└──────────────┘     └──────────────┘     └──────────────┘
     Browser           Docker              Docker
```

## 2. Architecture Pattern

**Layered Architecture** with clear separation:

```
Frontend (React SPA)
  └── API Client (Axios + JWT interceptor)
        └── REST API calls over HTTP

Backend (FastAPI)
  ├── API Layer       → Route handlers, request/response
  ├── Service Layer   → Business logic, state machine (future)
  ├── Schema Layer    → Pydantic validation
  ├── Model Layer     → SQLAlchemy ORM
  └── Core Layer      → Auth, security, exceptions

Database (PostgreSQL)
  └── Managed by Alembic migrations
```

## 3. Authentication Flow

```
1. User submits email + password → POST /api/auth/login
2. Backend verifies credentials → returns JWT token
3. Frontend stores token in localStorage
4. All subsequent requests include: Authorization: Bearer <token>
5. Backend validates token on every request via dependency injection
6. Token expires after 24 hours → user must re-login
```

## 4. Authorization Model

- **Role-based access control (RBAC)** with 5 roles
- Single role per user (MVP simplification)
- Authorization checked at two levels:
  1. **Route level**: `require_roles()` FastAPI dependency
  2. **Data level**: service layer filters data by user ownership

## 5. State Machine Architecture

- Proposal lifecycle managed by a centralized transition table
- All state changes go through a single `transition_proposal()` function
- Every transition is logged in `proposal_status_history` table
- Frontend cannot set status directly — only trigger actions

## 6. Frontend Architecture

```
src/
├── api/           → One file per API domain (auth, users, catalog...)
├── contexts/      → React Context for global state (Auth only for MVP)
├── components/    → Reusable UI components
│   └── Layout/    → Page chrome (Sidebar, Header, MainLayout)
├── pages/         → One folder per role, one file per screen
└── utils/         → Constants, helpers
```

**Key decisions:**
- TanStack Query for server state management (caching, refetching)
- React Hook Form + Zod for form validation
- Role-based sidebar menu defined in config (not hardcoded per page)
- CSS design system with variables (no CSS framework)

## 7. Database Design Principles

- UUIDs as primary keys (avoid sequential ID enumeration)
- Soft delete via `is_active` flag (not hard delete)
- Timestamps on all entities (`created_at`, `updated_at`)
- Status columns as VARCHAR (not integer codes) for readability
- Foreign key constraints for referential integrity
- Indexes on frequently queried columns (email, status)

## 8. API Design Conventions

| Convention | Example |
|-----------|---------|
| Prefix | All routes under `/api/` |
| Naming | Plural nouns for collections: `/api/proposals` |
| Pagination | `?page=1&size=20` on list endpoints |
| Filtering | Query params: `?status=SUBMITTED&role=FACULTY` |
| Error format | `{"detail": "Vietnamese error message"}` |
| Status codes | 200 (OK), 201 (Created), 400, 401, 403, 404 |
| Auth header | `Authorization: Bearer <jwt>` |
| Docs | Auto-generated OpenAPI at `/docs` |

## 9. Deployment Topology (Development)

All services run in Docker Compose:

| Service | Image | Port | Volumes |
|---------|-------|------|---------|
| db | postgres:16-alpine | 5432 | pgdata (persistent) |
| backend | python:3.12-slim (custom) | 8000 | ./backend (hot-reload) |
| frontend | node:20-alpine (custom) | 3000 | ./frontend (hot-reload) |
