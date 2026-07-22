import json
from pathlib import Path
from datetime import datetime

from ..config import settings
from ..utils.event_config import EVENT_TYPES


EVENTS_FILE = Path(
    settings.EVENTS_FILE
)


if not EVENTS_FILE.exists():
    EVENTS_FILE.write_text(
        "[]",
        encoding="utf-8"
    )



def load_events():

    return json.loads(
        EVENTS_FILE.read_text(
            encoding="utf-8"
        )
    )



def save_events(events):

    EVENTS_FILE.write_text(
        json.dumps(
            events,
            ensure_ascii=False,
            indent=4
        ),
        encoding="utf-8"
    )



def create_event(
    event_type,
    message
):

    cfg = EVENT_TYPES.get(
        event_type,
        EVENT_TYPES["info"]
    )


    return {
        "time":
            datetime.now().strftime(
                "%H:%M:%S"
            ),

        "type":
            event_type,

        "message":
            message,

        **cfg
    }