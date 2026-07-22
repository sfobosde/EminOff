import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

FILE = (
    BASE_DIR /
    "config" /
    "event-types.json"
)


with open(
    FILE,
    encoding="utf-8"
) as f:
    EVENT_TYPES = json.load(f)