from vtu_captcha.captcha_solver import VTUCaptchaSolver

import unittest


CAPTCHA_FILEPATH = "tests/test_captcha.png"
CAPTCHA_VALUE = "zsWmKR"


def get_captcha_bytes():
    with open(CAPTCHA_FILEPATH, "rb") as cf:
        return cf.read()


class TestCaptchaSolver(unittest.TestCase):

    def setUp(self):
        captcha_bytes = get_captcha_bytes()
        self.solver = VTUCaptchaSolver(captcha_bytes)

    def test_captcha_solver(self):
        captcha = self.solver.solve()
        self.assertEqual(captcha, CAPTCHA_VALUE)
