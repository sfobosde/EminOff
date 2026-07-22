from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import settings
from .routers import (
    events,
    images,
    websocket,
)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url=None,
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

app.include_router(images.router)
app.include_router(events.router)
app.include_router(websocket.router)


@app.get("/health")
def health():
    return {"status": "ok"}