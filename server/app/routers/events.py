import json

from fastapi import (
    APIRouter,
    Depends
)

from ..auth import verify_upload_token
from ..models.events import EventRequest

from ..services.events import (
    load_events,
    save_events,
    create_event
)

from ..services.websocket import manager


router = APIRouter()



@router.post("/event")
async def add_event(
    event: EventRequest,
    _=Depends(verify_upload_token)
):

    events = load_events()


    item = create_event(
        event.type,
        event.message
    )


    events.append(item)

    save_events(events)


    await manager.broadcast(
        json.dumps({
            "kind":"event",
            "event":item
        })
    )


    return {
        "success":True
    }