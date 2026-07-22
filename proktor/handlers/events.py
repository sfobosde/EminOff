import json

from config import EVENTS_FILE


def load_events():

    if not EVENTS_FILE.exists():
        return []


    with open(
        EVENTS_FILE,
        encoding="utf-8"
    ) as file:

        return json.load(file)