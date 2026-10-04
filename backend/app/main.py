"""
SaleGoodman Backend — FastAPI Application

Entry point for the backend API. Registers all routers, configures CORS,
and exposes the /docs Swagger UI.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import auth, dashboard, contacts, leads, calls, follow_ups, deals, escalations, settings as settings_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    # Startup: nothing needed — Supabase client is lazy
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="SaleGoodman API",
    description="Backend API for the SaleGoodman autonomous AI sales platform",
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
app.include_router(leads.router, prefix="/leads", tags=["Leads"])
app.include_router(calls.router, prefix="/calls", tags=["Calls"])
app.include_router(follow_ups.router, prefix="/follow-ups", tags=["Follow-Ups"])
app.include_router(deals.router, prefix="/deals", tags=["Deals"])
app.include_router(escalations.router, prefix="/escalations", tags=["Escalations"])
app.include_router(settings_api.router, prefix="/settings", tags=["Settings"])


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for Railway."""
    return {"status": "healthy", "service": "salegoodman-api"}
