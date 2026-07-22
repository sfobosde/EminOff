from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    RedirectResponse,
)
from fastapi.security import HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from ..auth import (
    security,
    verify_basic,
    verify_upload_token,
)
from ..services.storage import (
    delete_image,
    get_image,
    list_images,
    save_image,
)
from ..services.websocket import manager

import json

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    credentials: HTTPBasicCredentials = Depends(security),
):
    verify_basic(credentials)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "files": list_images(),
        },
    )


@router.get("/image/{filename}", response_class=HTMLResponse)
def image_page(
    filename: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(security),
):
    verify_basic(credentials)

    get_image(filename)

    return templates.TemplateResponse(
        "image.html",
        {
            "request": request,
            "filename": filename,
        },
    )


@router.get("/raw/{filename}")
def raw_image(
    filename: str,
    credentials: HTTPBasicCredentials = Depends(security),
):
    verify_basic(credentials)

    return FileResponse(
        get_image(filename)
    )


@router.post("/delete/{filename}")
def remove_image(
    filename: str,
    credentials: HTTPBasicCredentials = Depends(security),
):
    verify_basic(credentials)

    delete_image(filename)

    return RedirectResponse(
        "/",
        status_code=303,
    )


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    _=Depends(verify_upload_token),
):
    contents = await file.read()

    filename = save_image(contents)

    await manager.broadcast(
        json.dumps(
            {
                "kind": "image",
                "filename": filename,
            }
        )
    )

    return {
        "success": True,
        "filename": filename,
    }