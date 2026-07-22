import time
import requests

from api.client import HEADERS
from config import SERVER_URL
from logger import log

def upload_image(buffer):
    log(f"Uploading screenshot to {SERVER_URL}")
    files = {
        "file": (
            f"screenshot_{int(time.time())}.jpg",
            buffer,
            "image/jpeg",
        )
    }

    started = time.perf_counter()
    response = requests.post(
        SERVER_URL,
        headers=HEADERS,
        files=files,
        timeout=30,
    )


    response.raise_for_status()
    log(f"Server returned HTTP {response.status_code}")
    elapsed = time.perf_counter() - started

    log(f"Upload finished in {elapsed:.2f}s")

    return response.json()