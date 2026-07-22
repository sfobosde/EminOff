import json
import sys
from pathlib import Path


def get_app_dir():
    """
    Возвращает папку, где лежит exe.
    Работает и в Python, и после PyInstaller.
    """

    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parent


BASE_DIR = get_app_dir()


CONFIG_FILE = BASE_DIR / "config.json"
EVENTS_FILE = BASE_DIR / "events.json"


def load_config():

    if not CONFIG_FILE.exists():
        raise RuntimeError(
            f"Config not found: {CONFIG_FILE}"
        )

    with open(
        CONFIG_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


CONFIG = load_config()


SERVER_URL = CONFIG["server_url"]

UPLOAD_TOKEN = CONFIG["upload_token"]

HOTKEY = CONFIG.get(
    "hotkey",
    "ctrl+shift+a"
)

EXIT_HOTKEY = CONFIG.get(
    "exit_hotkey",
    "ctrl+shift+x"
)

JPEG_QUALITY = int(
    CONFIG.get(
        "jpeg_quality",
        90
    )
)