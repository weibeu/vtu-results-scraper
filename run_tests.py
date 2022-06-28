#!/usr/bin/env python3
import unittest

from tests.test_captcha_solver import TestCaptchaSolver


def suite():
    suite_ = unittest.defaultTestLoader.loadTestsFromTestCase(TestCaptchaSolver)
    return suite_


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
