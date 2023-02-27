from contextlib import suppress
from tempfile import NamedTemporaryFile

from PIL import UnidentifiedImageError
from PIL import Image


def is_a_valid_image(image_bytes):
    with NamedTemporaryFile() as temp_file:
        temp_file.write(image_bytes)

        with suppress(UnidentifiedImageError), Image.open(temp_file.name) as file:
            return True

    return False
