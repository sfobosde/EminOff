import os
import time
from io import BytesIO

import keyboard
import mss
import requests
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
UPLOAD_TOKEN = os.getenv("UPLOAD_TOKEN")
HOTKEY = os.getenv("HOTKEY", "ctrl+shift+a")
JPEG_QUALITY = int(os.getenv("JPEG_QUALITY", "90"))

if not SERVER_URL:
    raise RuntimeError("SERVER_URL is not configured")

if not UPLOAD_TOKEN:
    raise RuntimeError("UPLOAD_TOKEN is not configured")


def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # первый монитор
        shot = sct.grab(monitor)

        image = Image.frombytes(
            "RGB",
            shot.size,
            shot.rgb,
        )

        buffer = BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=JPEG_QUALITY,
        )

        buffer.seek(0)

        return buffer


def upload(buffer):
    headers = {
        "Authorization": f"Bearer {UPLOAD_TOKEN}"
    }

    files = {
        "file": (
            f"screenshot_{int(time.time())}.jpg",
            buffer,
            "image/jpeg",
        )
    }

    response = requests.post(
        SERVER_URL,
        headers=headers,
        files=files,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def capture_and_upload():
    print("Capturing...")

    image = capture_screen()

    print("Uploading...")

    result = upload(image)

    print(result)

    print("Waiting...")


def main():
    print("--------------------------------")
    print(" Screen Agent")
    print("--------------------------------")
    print(f"Server : {SERVER_URL}")
    print(f"Hotkey : {HOTKEY}")
    print("--------------------------------")
    print("Waiting...")

    keyboard.add_hotkey(
        HOTKEY,
        capture_and_upload,
    )

    keyboard.wait()


if __name__ == "__main__":
    main()