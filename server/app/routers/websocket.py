from fastapi import (
    APIRouter,
    WebSocket
)

from ..services.websocket import manager


router = APIRouter()



@router.websocket("/ws")
async def websocket(
    websocket: WebSocket
):

    await manager.connect(
        websocket
    )


    try:

        while True:
            await websocket.receive_text()


    except Exception:

        manager.disconnect(
            websocket
        )