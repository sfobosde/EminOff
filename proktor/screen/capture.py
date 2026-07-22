from io import BytesIO
from logger import log
import mss
from PIL import Image

from config import JPEG_QUALITY


def capture_screen():
    log("Capturing screen")
    with mss.mss() as sct:

        monitor = sct.monitors[1]

        shot = sct.grab(monitor)


        image = Image.frombytes(
            "RGB",
            shot.size,
            shot.rgb,
        )


        buffer = BytesIO()


        image.save(
            buffer,
            format="JPEG",
            quality=JPEG_QUALITY,
        )


        buffer.seek(0)

        log(f"Screenshot created ({shot.width}x{shot.height})")
        return buffer