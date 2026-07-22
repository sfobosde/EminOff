from logger import log, log_exception
import os
import keyboard


from screen.capture import capture_screen

from api.upload import upload_image
from api.events import send_event

from handlers.events import load_events

from handlers.keyboard import (
    register_keyboard,
    wait,
)


def capture_and_upload():
    log("Screenshot hotkey pressed")

    try:
        image = capture_screen()
        upload_image(image)
        log("Capture workflow completed")
    except Exception as ex:
        log_exception(ex)


def stop_agent():
    log("Stopping agent")
    keyboard.unhook_all_hotkeys()
    log("All hotkeys removed")
    os._exit(0)



def main():
    register_keyboard(
        capture_and_upload,
        stop_agent,
    )

    events = load_events()
    log(f"Loaded {len(events)} hotkey events")

    for event in events:

        keyboard.add_hotkey(
            event["hotkey"],
            lambda e=event: send_event(e)
        )

        log(f"Registered event '{event['type']}' on {event['hotkey']}")

    log("Agent is ready")
    wait()

if __name__ == "__main__":
    log("========== Agent started ==========")
    main()