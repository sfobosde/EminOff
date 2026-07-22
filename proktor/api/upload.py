import time
import requests

from api.client import HEADERS
from config import SERVER_URL


def upload_image(buffer):

    files = {
        "file": (
            f"screenshot_{int(time.time())}.jpg",
            buffer,
            "image/jpeg",
        )
    }


    response = requests.post(
        SERVER_URL,
        headers=HEADERS,
        files=files,
        timeout=30,
    )


    response.raise_for_status()


    return response.json()