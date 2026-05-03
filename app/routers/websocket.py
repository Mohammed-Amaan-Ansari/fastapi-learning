from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# Store active connections
connections = []


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            # Broadcast message
            for conn in connections:
                await conn.send_text(f"Message: {data}")

    except WebSocketDisconnect:
        connections.remove(websocket)