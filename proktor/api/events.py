import requests

from api.client import HEADERS
from config import SERVER_URL


def send_event(event):

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


    response.raise_for_status()