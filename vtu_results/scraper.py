from vtu_captcha import VTUCaptchaSolver
from vtu_results.utils import get_etree, cleaned_string, table_to_dict
from vtu_results.exceptions import InvalidCaptchaError, VTUIsDownException, VTUResultsScraperBaseException, \
    InvalidUSNError

import requests

from urllib.parse import urlencode


class VTUResultScraper(object):
    BASE_URL = "https://results.vtu.ac.in"
    RESULT_ROUTE = "/FMEcbcs22/index.php"
    RESULT_PAGE_ROUTE = "/FMEcbcs22/resultpage.php"
    DEFAULT_RETRIES = 100

    def __init__(self, usn):
        self.session = requests.Session()
        self.session.verify = False
        self._token = None
        self._captcha_route = None
        self.usn = usn

    def _request(self, method, route, *args, **kwargs):
        return self.session.request(method, self.BASE_URL + route, *args, **kwargs)

    def get_homepage(self):
        response = self._request("GET", self.RESULT_ROUTE)
        tree = get_etree(response.content)
        try:
            self._token = tree.xpath('//input[@type="hidden" and @name="Token"]')[0].attrib["value"]
            self._captcha_route = tree.xpath('//img[contains(@alt, "CAPTCHA")]')[0].attrib["src"]
        except (IndexError, KeyError):
            raise VTUIsDownException

    def get_captcha(self):
        response = self._request("GET", self._captcha_route)
        solver = VTUCaptchaSolver(response.content)
        return solver.solve()

    def submit_form(self):
        captcha = self.get_captcha()
        payload = {"Token": self._token, "captchacode": captcha, "lns": self.usn}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self._request("POST", self.RESULT_PAGE_ROUTE, data=urlencode(payload), headers=headers)
        if "Invalid captcha code".lower() in response.text.lower():
            raise InvalidCaptchaError
        if "Seat Number is not available".lower() in response.text.lower():
            raise InvalidUSNError

        return get_etree(response.content)

    def extract_results(self):
        tree = self.submit_form()
        try:
            _, usn, _, student_name, *_ = (str().join(x.itertext()) for x in tree.xpath('//table[1]/tr/td'))
            result_tables = tree.xpath('//div[@class="divTable"]')[:-1]
            sems = [rt.getparent().xpath('.//div/b')[0].text.split(":")[-1].strip() for rt in result_tables]
            results = [{"semester": s, "result": table_to_dict(t)} for s, t in zip(sems, result_tables)]
        except (IndexError, KeyError, ValueError):
            raise VTUIsDownException
        else:
            usn = cleaned_string(usn)
            student_name = cleaned_string(student_name)
        return {
            "usn": usn,
            "student_name": student_name,
            "results": results,
        }

    def get_results(self):
        for _ in range(self.DEFAULT_RETRIES):
            try:
                self.get_homepage()
                return self.extract_results()
            except VTUResultsScraperBaseException:
                continue
        raise VTUResultsScraperBaseException

    @classmethod
    def get_results_from_usn(cls, usn):
        self = cls(usn)
        return self.get_results()
