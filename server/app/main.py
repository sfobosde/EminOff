from fastapi import FastAPI

from .config import settings
from .routers import (
    events,
    images,
    websocket,
)

app = FastAPI(
    docs_url="/docs" if settings.ENABLE_DOCS else None,
    redoc_url=None,
)

app.include_router(images.router)
app.include_router(events.router)
app.include_router(websocket.router)


@app.get("/health")
def health():
    return {"status": "ok"}