from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

websocket_router = APIRouter(prefix="/websocket", tags=["websocket"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.remove(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@websocket_router.websocket("/tasks")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)
