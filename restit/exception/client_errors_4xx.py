from restit.exception.http_error import HttpError


class BadRequest(HttpError):
    STATUS_CODE = 400
    TITLE = "Bad Request"
    DEFAULT_DESCRIPTION = \
        "This response means that server could not understand the request due to invalid syntax."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/400"


class NotFound(HttpError):
    STATUS_CODE = 404
    TITLE = "Not Found"
    DEFAULT_DESCRIPTION = \
        "Server can not find requested resource. This response code probably is most famous one due to its " \
        "frequency to occur in web."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/404"


class MethodNotAllowed(HttpError):
    STATUS_CODE = 405
    TITLE = "Method Not Allowed"
    DEFAULT_DESCRIPTION = \
        "The request method is known by the server but has been disabled and cannot be used. " \
        "The two mandatory methods, GET and HEAD, must never be disabled and should not return this error code."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/405"


class NotAcceptable(HttpError):
    STATUS_CODE = 406
    TITLE = "Not Acceptable"
    DEFAULT_DESCRIPTION = \
        "This response is sent when the web server, after performing server-driven content negotiation, " \
        "doesn't find any content following the criteria given by the user agent."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/406"


class UnsupportedMediaType(HttpError):
    STATUS_CODE = 415
    TITLE = "Unsupported Media Type"
    DEFAULT_DESCRIPTION = \
        "The media format of the requested data is not supported by the server, so the server is rejecting the request."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/415"


class UnprocessableEntity(HttpError):
    STATUS_CODE = 422
    TITLE = "Unprocessable Entity"
    DEFAULT_DESCRIPTION = \
        "Indicates that the server understands the content type of the request entity, and the syntax of the request " \
        "entity is correct, but it was unable to process the contained instructions."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/422"
