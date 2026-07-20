import requests

from config import SERVER_URL
from config import UPLOAD_TOKEN


def upload(image):

    headers = {
        "Authorization": f"Bearer {UPLOAD_TOKEN}"
    }

    files = {
        "file": (
            "screen.jpg",
            image,
            "image/jpeg",
        )
    }

    r = requests.post(
        SERVER_URL,
        headers=headers,
        files=files,
        timeout=30,
    )

    r.raise_for_status()

    return r.json()