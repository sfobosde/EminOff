from datetime import datetime
from pathlib import Path
import os
import traceback

from config import BASE_DIR

LOG_FILE = BASE_DIR / "agent.log"


def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
        f.flush()
        os.fsync(f.fileno())


def log_exception(ex: Exception):
    log(f"ERROR: {ex}")
    log(traceback.format_exc())