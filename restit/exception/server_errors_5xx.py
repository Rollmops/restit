from restit.exception.http_error import HttpError


class InternalServerError(HttpError):
    STATUS_CODE = 500
    TITLE = "Internal Server Error"
    DEFAULT_DESCRIPTION = "The server has encountered a situation it doesn't know how to handle."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/500"


class NotImplemented(HttpError):
    STATUS_CODE = 501
    TITLE = "Not Implemented"
    DEFAULT_DESCRIPTION = \
        "The request method is not supported by the server and cannot be handled. " \
        "The only methods that servers are required to support (and therefore that must not return this code) " \
        "are GET and HEAD."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/501"
