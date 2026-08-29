from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.auth import router as auth_router
from app.api.alerts import router as alerts_router
from app.api.hosts import router as hosts_router
from app.api.actions import router as actions_router
from app.database import get_db
from app.api.analytics import router as analytics_router


app = FastAPI(
    title="Capstone Backend",
    version="1.0.0",
)


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
# Routers
# ============================================================

app.include_router(auth_router)
app.include_router(alerts_router)
app.include_router(actions_router)
app.include_router(hosts_router)
app.include_router(analytics_router)


# ============================================================
# Root
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Capstone Backend is running!"
    }


# ============================================================
# Database Test
# ============================================================

@app.get("/db-test")
def database_test(
    db: Session = Depends(get_db),
):
    result = db.execute(text("SELECT 1"))

    return {
        "database": result.scalar()
    }


# ============================================================
# WEBSOCKET
# ============================================================

@app.websocket("/ws/alerts")
async def alert_websocket(websocket: WebSocket):

    from app.api.websocket import manager

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception:
        manager.disconnect(websocket)