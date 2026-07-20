import os

from dotenv import load_dotenv

load_dotenv()


SERVER_URL = os.environ["SERVER_URL"]

UPLOAD_TOKEN = os.environ["UPLOAD_TOKEN"]

HOTKEY = os.getenv(
    "HOTKEY",
    "ctrl+shift+a",
)

JPEG_QUALITY = int(
    os.getenv(
        "JPEG_QUALITY",
        "90",
    )
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)