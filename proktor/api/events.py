from logger import log, log_exception

import requests

from api.client import HEADERS
from config import SERVER_URL


def send_event(event):
    try:
        log(f"Sending event '{event['type']}': '{event['message']}'")
        url = SERVER_URL.replace(
            "/upload",
            "/event"
        )


        response = requests.post(
            url,
            headers=HEADERS,
            json={
                "type": event["type"],
                "message": event["message"]
            },
            timeout=30,
        )

        log(f"Event accepted ({response.status_code})")
        log(response.text)

        response.raise_for_status()
    except Exception as ex:
        log_exception(ex)