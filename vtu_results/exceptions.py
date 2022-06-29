class VTUResultsScraperBaseException(Exception):
    pass


class VTUIsDownException(VTUResultsScraperBaseException):
    pass


class InvalidCaptchaError(VTUResultsScraperBaseException):
    pass


class InvalidUSNError(VTUResultsScraperBaseException):
    pass
