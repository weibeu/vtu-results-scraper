from vtu_captcha.captcha_solver import VTUCaptchaSolver

import unittest


CAPTCHAS_BASE_PATH = "tests/test_captchas/"


def get_captcha_bytes(filename):
    with open(CAPTCHAS_BASE_PATH + filename, "rb") as cf:
        return cf.read()


class TestCaptchaSolver(unittest.TestCase):

    def _test_captcha(self, filepath, correct_captcha):
        captcha_bytes = get_captcha_bytes(filepath)
        captcha = VTUCaptchaSolver.solve_from_captcha_bytes(captcha_bytes)
        self.assertEqual(captcha, correct_captcha)

    def test_zero_rotated(self):
        self._test_captcha("test_captcha_zero_rot.png", "zsWmKR")

    def test_positive_rotated(self):
        self._test_captcha("test_captcha_pos_rot.png", "CHCUpV")

    def test_negative_rotated(self):
        self._test_captcha("test_captcha_neg_rot.png", "7FLrkW")
