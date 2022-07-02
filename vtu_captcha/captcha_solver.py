from PIL import Image, ImageOps

import pytesseract
import io
import string
import math
import numpy as np


WHITELISTED_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits
TESSERACT_CONFIG = f"--psm 8 -l eng -c tessedit_char_whitelist={WHITELISTED_CHARS}"


# noinspection PyTypeChecker
class VTUCaptchaSolver(object):
    CAPTCHA_BASE_IMAGE_PATH = "vtu_captcha/vtu_captcha_base.png"
    base_arr = np.asarray(Image.open(CAPTCHA_BASE_IMAGE_PATH))
    NOISE_FILL = (255, 255, 255)

    def __init__(self, captcha_bytes):
        self.captcha_bytes = captcha_bytes
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
            self.captcha_arr[i][j] = list(self.NOISE_FILL)

    @staticmethod
    def crop_to_content(image):
        return image.crop(ImageOps.invert(image).getbbox())

    def justify_horizontally(self):
        shape = self.captcha_arr.shape
        # TOP LEFT PIXEL: i -> min, j -> min
        # TOP RIGHT PIXEL: i -> min, j -> max
        # Start from extreme opposite initial states.
        top_left = (shape[0], shape[1])
        top_right = (shape[0], 0)
        for i in range(shape[0]):
            for j in range(shape[1]):
                # Ignore noise fills.
                if tuple(self.captcha_arr[i][j]) == self.NOISE_FILL:
                    continue
                top_left_i, top_left_j = top_left
                top_right_i, top_right_j = top_right
                if i < top_left_i or i < top_left_j:
                    if j < top_left_j:
                        # Keep shifting top_left for extreme top left pixel.
                        top_left = (i, j)
                    elif j > top_right_j:
                        # Keep shifting top_right to extreme top right pixel.
                        top_right = (i, j)
        image = Image.fromarray(self.captcha_arr)
        slope = (top_right[0] - top_left[0]) / (top_right[1] - top_left[1])
        theta = math.degrees(math.atan(slope))
        image = image.rotate(theta, fillcolor=self.NOISE_FILL)
        return image

    def solve(self):
        self.remove_noise()
        image = self.justify_horizontally()
        image = self.crop_to_content(image)
        return pytesseract.image_to_string(image, config=TESSERACT_CONFIG).strip()

    @classmethod
    def solve_from_captcha_bytes(cls, captcha_bytes):
        self = cls(captcha_bytes)
        return self.solve()
