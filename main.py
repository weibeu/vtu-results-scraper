from concurrent.futures import ThreadPoolExecutor

import math
import hashlib
import requests


class VTUCaptchaHarvester(object):
    BASE_URL = "https://results.vtu.ac.in"
    RESULT_ROUTE = "/FMEcbcs22/index.php"
    CAPTCHA_ROUTE = "/captcha/vtu_captcha.php?_CAPTCHA&t=0.10401200+1656173754"
    BASE_PATH = "captchas"
    MAX_WORKERS = 50

    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False

    def _save_captcha(self, captcha_bytes):
        filename = hashlib.sha1(captcha_bytes).hexdigest()
        with open(f"{self.BASE_PATH}/{filename}.png", "wb") as cf:
            cf.write(captcha_bytes)

    def request(self, method, route, *args, **kwargs):
        return self.session.request(method, self.BASE_URL + route, *args, **kwargs)

    def fetch_captcha(self):
        _response = self.request("GET", self.RESULT_ROUTE)
        response = self.request("GET", self.CAPTCHA_ROUTE)
        self._save_captcha(response.content)

    def bulk_fetch_captcha(self, n=math.inf):
        with ThreadPoolExecutor(self.MAX_WORKERS) as executor:
            while n > 0:
                executor.submit(self.fetch_captcha)
                n -= 1


if __name__ == "__main__":
    captcha_harvester = VTUCaptchaHarvester()
    print(captcha_harvester.bulk_fetch_captcha())
