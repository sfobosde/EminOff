from fileinput import filename
from pathlib import Path
from uuid import uuid4
import shutil
import imghdr
from fastapi.responses import FileResponse

from fastapi import (
    Depends,
    FastAPI,
    File,
    HTTPException,
    Request,
    UploadFile,
)

from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json
from datetime import datetime

from .auth import (
    security,
    verify_basic,
    verify_upload_token,
)
from .config import settings

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

EVENTS_FILE = Path("/data/events.json")

if not EVENTS_FILE.exists():
    EVENTS_FILE.write_text("[]", encoding="utf-8")

CONFIG_DIR = Path("config")

EVENT_TYPES_FILE = CONFIG_DIR / "event-types.json"

with open(EVENT_TYPES_FILE, encoding="utf-8") as f:
    EVENT_TYPES = json.load(f)

templates = Jinja2Templates(directory="app/templates")

docs_url = "/docs" if settings.ENABLE_DOCS else None

app = FastAPI(
    docs_url=docs_url,
    redoc_url=None,
)

from fastapi import WebSocket

ALLOWED = {
    "jpeg",
    "png",
    "gif",
    "webp",
}

class ConnectionManager:

    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, message: str):
        dead = []

        for ws in self.connections:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)

        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    _=Depends(verify_upload_token),
):

    contents = await file.read()

    if (
        len(contents)
        > settings.MAX_FILE_SIZE_MB * 1024 * 1024
    ):
        raise HTTPException(
            400,
            "File too large",
        )

    image_type = imghdr.what(None, contents)

    if image_type not in ALLOWED:
        raise HTTPException(
            400,
            "Unsupported image",
        )

    filename = f"{uuid4().hex}.{image_type}"

    path = UPLOAD_DIR / filename

    with open(path, "wb") as f:
        f.write(contents)

    await manager.broadcast(
        json.dumps({
            "kind": "image",
            "filename": filename
        })
    )

    return {
        "success": True,
        "filename": filename,
    }


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    credentials=Depends(security),
):
    verify_basic(credentials)

    files = sorted(
        UPLOAD_DIR.iterdir(),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "files": files,
        },
    )


@app.get("/image/{filename}", response_class=HTMLResponse)
def image_page(
    filename: str,
    request: Request,
    credentials=Depends(security),
):
    verify_basic(credentials)

    path = UPLOAD_DIR / filename

    if not path.exists():
        raise HTTPException(404)

    return templates.TemplateResponse(
        "image.html",
        {
            "request": request,
            "filename": filename,
        },
    )

@app.get("/raw/{filename}")
def raw_image(
    filename: str,
    credentials=Depends(security),
):
    verify_basic(credentials)

    path = UPLOAD_DIR / filename

    if not path.exists():
        raise HTTPException(404)

    return FileResponse(path)


@app.post("/delete/{filename}")
def delete_image(
    filename: str,
    credentials=Depends(security),
):
    verify_basic(credentials)

    path = UPLOAD_DIR / filename

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    path.unlink()

    return RedirectResponse(
        url="/",
        status_code=303,
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except Exception:
        manager.disconnect(websocket)
        

def load_events():

    with open(EVENTS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_events(events):

    with open(EVENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            events,
            f,
            ensure_ascii=False,
            indent=4
        )

from pydantic import BaseModel

class EventRequest(BaseModel):

    type: str

    message: str

@app.post("/event")
async def add_event(
    event: EventRequest,
    credentials=Depends(security)
):

    verify_basic(credentials)

    events = load_events()

    cfg = EVENT_TYPES.get(
        event.type,
        EVENT_TYPES["info"]
    )

    item = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "type": event.type,
        "message": event.message,
        "title": cfg["title"],
        "color": cfg["color"],
        "background": cfg["background"],
        "icon": cfg["icon"]
    }

    events.append(item)

    save_events(events)

    await manager.broadcast(
        json.dumps({
            "kind": "event",
            "event": item
        })
    )

    return {
        "success": True
    }