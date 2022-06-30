from PIL import Image

import pytesseract
import io
import string
import numpy as np


WHITELISTED_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits
TESSERACT_CONFIG = f"--psm 8 -l eng -c tessedit_char_whitelist={WHITELISTED_CHARS}"


class VTUCaptchaSolver(object):
    CAPTCHA_BASE_IMAGE_PATH = "vtu_captcha/vtu_captcha_base.png"
    # noinspection PyTypeChecker
    base_arr = np.asarray(Image.open(CAPTCHA_BASE_IMAGE_PATH))
    NOISE_FILL = [255, 255, 255]

    def __init__(self, captcha_bytes):
        self.captcha_bytes = captcha_bytes
        # noinspection PyTypeChecker
        self.captcha_arr = np.asarray(Image.open(io.BytesIO(self.captcha_bytes)))

    def captcha_pixels(self):
        shape = self.captcha_arr.shape
        yield from ((i, j) for i in range(shape[0]) for j in range(shape[1]))

    def remove_noise(self):
        for i, j in self.captcha_pixels():
            base_pixel = self.base_arr[i][j]
            captcha_pixel = tuple(self.captcha_arr[i][j])
            if captcha_pixel != tuple(base_pixel) and len(set(captcha_pixel)) == 1:
                continue
            self.captcha_arr[i][j] = self.NOISE_FILL

    def solve(self):
        self.remove_noise()
        return pytesseract.image_to_string(self.captcha_arr, config=TESSERACT_CONFIG).strip()
