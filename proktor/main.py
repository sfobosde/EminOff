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

    image = capture_screen()

    upload_image(image)


def stop_agent():

    keyboard.unhook_all_hotkeys()

    os._exit(0)



def main():

    register_keyboard(
        capture_and_upload,
        stop_agent,
    )


    events = load_events()


    for event in events:

        keyboard.add_hotkey(
            event["hotkey"],
            lambda e=event: send_event(e)
        )


    wait()



if __name__ == "__main__":
    main()