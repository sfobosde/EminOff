from pathlib import Path
from uuid import uuid4
import imghdr

from fastapi import HTTPException

from ..config import settings


UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


ALLOWED = {
    "jpeg",
    "png",
    "gif",
    "webp",
}


def save_image(
    content: bytes
):

    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            400,
            "File too large"
        )


    image_type = imghdr.what(
        None,
        content
    )


    if image_type not in ALLOWED:
        raise HTTPException(
            400,
            "Unsupported image"
        )


    filename = (
        f"{uuid4().hex}.{image_type}"
    )


    path = UPLOAD_DIR / filename


    path.write_bytes(content)


    return filename



def get_image(
    filename: str
):

    path = UPLOAD_DIR / filename

    if not path.exists():
        raise HTTPException(
            404,
            "File not found"
        )

    return path



def list_images():

    return sorted(
        UPLOAD_DIR.iterdir(),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )



def delete_image(
    filename: str
):

    path = get_image(filename)

    path.unlink()