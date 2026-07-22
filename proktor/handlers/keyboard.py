import keyboard

from config import (
    HOTKEY,
    EXIT_HOTKEY,
)


def register_keyboard(
    screenshot_callback,
    stop_callback,
):

    keyboard.add_hotkey(
        HOTKEY,
        screenshot_callback
    )


    keyboard.add_hotkey(
        EXIT_HOTKEY,
        stop_callback
    )


def wait():

    keyboard.wait()