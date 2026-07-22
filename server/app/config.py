import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

    UPLOAD_DIR = os.getenv(
        "UPLOAD_DIR",
        "/data/uploads"
    )

    EVENTS_FILE = os.getenv(
        "EVENTS_FILE",
        "/data/events.json"
    )

    UPLOAD_TOKEN = os.getenv(
        "UPLOAD_TOKEN",
        ""
    )

    WEB_USERNAME = os.getenv(
        "WEB_USERNAME",
        "admin"
    )

    WEB_PASSWORD = os.getenv(
        "WEB_PASSWORD",
        "admin"
    )

    MAX_FILE_SIZE_MB = int(
        os.getenv(
            "MAX_FILE_SIZE_MB",
            "20"
        )
    )

    ENABLE_DOCS = (
        os.getenv(
            "ENABLE_DOCS",
            "false"
        ).lower() == "true"
    )


settings = Settings()