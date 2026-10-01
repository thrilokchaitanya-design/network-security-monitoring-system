from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter(
    tags=["WebSocket"],
)


# ============================================================
# WEBSOCKET CONNECTION MANAGER
# ============================================================

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)


# ============================================================
# GLOBAL CONNECTION MANAGER
# ============================================================

manager = ConnectionManager()


# ============================================================
# ALERT WEBSOCKET
# ============================================================

@router.websocket("/ws/alerts")
async def alert_websocket(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception:
        manager.disconnect(websocket)
