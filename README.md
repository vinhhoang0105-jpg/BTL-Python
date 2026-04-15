# SciRes — Hệ thống Quản lý Nghiên cứu Khoa học

> University Scientific Research Management System — MVP

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, React Router, TanStack Query, React Hook Form, Zod |
| Backend | FastAPI, SQLAlchemy, Alembic, Pydantic, python-jose (JWT) |
| Database | PostgreSQL 16 |
| Container | Docker, Docker Compose |

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- No other services running on ports `3000`, `5432`, `8000`

### 1. Clone & Configure

```bash
git clone <repo-url>
cd BTL-PY
cp .env.example .env
```

### 2. Start All Services

```bash
docker-compose up --build
```

This will:
- Start PostgreSQL 16 on port `5432`
- Start FastAPI backend on port `8000` (auto-creates tables + seeds data)
- Start React frontend on port `3000`

### 3. Access

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000/api/health |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |

### 4. Demo Accounts

All accounts use password: `password123`

| Role | Email |
|------|-------|
| Quản trị viên | admin@university.edu.vn |
| Phòng KHCN | staff@university.edu.vn |
| Lãnh đạo | leader@university.edu.vn |
| Giảng viên | faculty1@university.edu.vn |
| Phản biện | reviewer1@university.edu.vn |

## Development

### Backend Only

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Only

```bash
cd frontend
npm install
npm run dev
```

### Database Migrations

```bash
# Inside backend container or with DATABASE_URL set:
cd backend

# Generate new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

### Seed Data

```bash
# Inside backend container:
python -m app.seed.seed_data
```

## Project Structure

```
BTL-PY/
├── docker-compose.yml          # Container orchestration
├── .env / .env.example         # Environment configuration
├── init.sql                    # PostgreSQL bootstrap
├── docs/                       # Project documentation
│   ├── permissions.md          # Role-permission matrix
│   └── workflow.md             # State machines & workflows
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py             # App entry point
│   │   ├── config.py           # Settings
│   │   ├── database.py         # DB engine
│   │   ├── core/               # Auth, security, exceptions
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── api/                # Route handlers
│   │   └── seed/               # Demo data
│   ├── alembic/                # Database migrations
│   └── requirements.txt
└── frontend/                   # React application
    ├── src/
    │   ├── App.jsx             # Router
    │   ├── api/                # Axios API layer
    │   ├── contexts/           # Auth context
    │   ├── components/Layout/  # Sidebar, Header, MainLayout
    │   ├── pages/              # Page components
    │   └── utils/              # Constants, helpers
    └── package.json
```

## API Overview

| Module | Prefix | Status |
|--------|--------|--------|
| Auth | `/api/auth` | ✅ Done |
| Users | `/api/users` | ✅ Done |
| Catalog | `/api/catalog` | ✅ Done |
| Periods | `/api/periods` | 🔜 Next |
| Proposals | `/api/proposals` | 🔜 Next |
| Councils | `/api/councils` | 🔜 Planned |
| Approvals | `/api/approvals` | 🔜 Planned |
| Progress | `/api/progress` | 🔜 Planned |
| Acceptance | `/api/acceptance` | 🔜 Planned |
| Dashboard | `/api/dashboard` | 🔜 Planned |

## License

Private — University project.
