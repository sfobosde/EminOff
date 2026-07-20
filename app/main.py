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

from .auth import (
    security,
    verify_basic,
    verify_upload_token,
)
from .config import settings

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory="app/templates")

docs_url = "/docs" if settings.ENABLE_DOCS else None

app = FastAPI(
    docs_url=docs_url,
    redoc_url=None,
)


ALLOWED = {
    "jpeg",
    "png",
    "gif",
    "webp",
}


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