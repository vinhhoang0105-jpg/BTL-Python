"""FastAPI application entry point.

Mounts all API routers, configures CORS, and exposes OpenAPI docs.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, users, catalog


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown lifecycle."""
    # Startup: run seed if needed (optional, controlled by env)
    import os
    if os.getenv("AUTO_SEED", "false").lower() == "true":
        from app.seed.seed_data import seed
        seed()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="SciRes — Hệ thống Quản lý NCKH",
    description="Scientific Research Management System for Universities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount API routers ────────────────────────────────────────────
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(catalog.router, prefix="/api")


@app.get("/api/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "SciRes API"}
