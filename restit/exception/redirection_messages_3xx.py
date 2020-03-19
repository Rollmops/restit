from restit.exception import HttpError


class MultipleChoice(HttpError):
    STATUS_CODE = 300
    TITLE = "Multiple Choice"
    DEFAULT_DESCRIPTION = \
        "The request has more than one possible responses. User-agent or user should choose one of them. " \
        "There is no standardized way to choose one of the responses."

    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/300"


class MovedPermanently(HttpError):
    STATUS_CODE = 301
    TITLE = "Moved Permanently"
    DEFAULT_DESCRIPTION = \
        "This response code means that URI of requested resource has been changed. Probably, new URI would be given " \
        "in the response."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/301"


class Found(HttpError):
    STATUS_CODE = 302
    TITLE = "Found"
    DEFAULT_DESCRIPTION = \
        "This response code means that URI of requested resource has been changed temporarily. " \
        "New changes in the URI might be made in the future. Therefore, this same URI should be used by the client " \
        "in future requests."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/302"


class SeeOther(HttpError):
    STATUS_CODE = 303
    TITLE = "See Other"
    DEFAULT_DESCRIPTION = \
        "Server sent this response to directing client to get requested resource to another URI with an GET request."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/303"


class NotModified(HttpError):
    STATUS_CODE = 304
    TITLE = "Not Modified"
    DEFAULT_DESCRIPTION = \
        "This is used for caching purposes. It is telling to client that response has not been modified. So, " \
        "client can continue to use same cached version of response."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/304"


class UseProxy(HttpError):
    STATUS_CODE = 305
    TITLE = "Use Proxy"
    DEFAULT_DESCRIPTION = \
        "This means requested response must be accessed by a proxy. This response code is not largely " \
        "supported because security reasons."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/305"


class TemporaryRedirect(HttpError):
    STATUS_CODE = 307
    TITLE = "Temporary Redirect"
    DEFAULT_DESCRIPTION = \
        "Server sent this response to directing client to get requested resource to another URI with same method " \
        "that used prior request. This has the same semantic than the 302 Found HTTP response code, with the " \
        "exception that the user agent must not change the HTTP method used: if a POST was used in the first " \
        "request, a POST must be used in the second request."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/307"


class PermanentRedirect(HttpError):
    STATUS_CODE = 308
    TITLE = "Permanent Redirect"
    DEFAULT_DESCRIPTION = \
        "This means that the resource is now permanently located at another URI, specified by the Location: " \
        "HTTP Response header. This has the same semantics as the 301 Moved Permanently HTTP response code, with " \
        "the exception that the user agent must not change the HTTP method used: if a POST was used in the first " \
        "request, a POST must be used in the second request."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/308"
