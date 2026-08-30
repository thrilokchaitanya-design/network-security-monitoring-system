from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.auth import router as auth_router
from app.api.alerts import router as alerts_router
from app.api.hosts import router as hosts_router
from app.api.actions import router as actions_router
from app.api.analytics import router as analytics_router
from app.api.websocket import router as websocket_router

from app.database import get_db


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Capstone Backend",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(alerts_router)
app.include_router(actions_router)
app.include_router(hosts_router)
app.include_router(analytics_router)
app.include_router(websocket_router)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Capstone Backend is running!"
    }


# ============================================================
# DATABASE TEST
# ============================================================

@app.get("/db-test")
def database_test(
    db: Session = Depends(get_db),
):
    result = db.execute(text("SELECT 1"))

    return {
        "database": result.scalar()
    }