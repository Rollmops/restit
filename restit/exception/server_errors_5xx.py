from restit.exception.http_error import HttpError


class InternalServerError(HttpError):
    STATUS_CODE = 500
    TITLE = "Internal Server Error"
    DEFAULT_DESCRIPTION = "The server has encountered a situation it doesn't know how to handle."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/500"


# noinspection PyShadowingBuiltins
class NotImplemented(HttpError):
    STATUS_CODE = 501
    TITLE = "Not Implemented"
    DEFAULT_DESCRIPTION = \
        "The request method is not supported by the server and cannot be handled. " \
        "The only methods that servers are required to support (and therefore that must not return this code) " \
        "are GET and HEAD."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/501"


class BadGateway(HttpError):
    STATUS_CODE = 502
    TITLE = "Bad Gateway"
    DEFAULT_DESCRIPTION = \
        "This error response means that the server, while working as a gateway to get a response needed to handle " \
        "the request, got an invalid response."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/502"


class ServiceUnavailable(HttpError):
    STATUS_CODE = 503
    TITLE = "Service Unavailable"
    DEFAULT_DESCRIPTION = \
        "The server is not ready to handle the request. Common causes are a server that is down for maintenance " \
        "or that is overloaded. Note that together with this response, a user-friendly page explaining the problem " \
        "should be sent. This responses should be used for temporary conditions and the Retry-After: HTTP header " \
        "should, if possible, contain the estimated time before the recovery of the service. The webmaster must " \
        "also take care about the caching-related headers that are sent along with this response, as these " \
        "temporary condition responses should usually not be cached."

    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/503"


class GatewayTimeout(HttpError):
    STATUS_CODE = 504
    TITLE = "Gateway Timeout"
    DEFAULT_DESCRIPTION = \
        "This error response is given when the server is acting as a gateway and cannot get a response in time."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/504"


class HTTPVersionNotSupported(HttpError):
    STATUS_CODE = 505
    TITLE = "HTTP Version Not Supported"
    DEFAULT_DESCRIPTION = "The HTTP version used in the request is not supported by the server."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/505"


class VariantAlsoNegotiates(HttpError):
    STATUS_CODE = 506
    TITLE = "Variant Also Negotiates"
    DEFAULT_DESCRIPTION = \
        "The server has an internal configuration error: transparent content negotiation for the request results " \
        "in a circular reference."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/506"


class VariantAlsoNegotiates507(HttpError):
    STATUS_CODE = 507
    TITLE = "Variant Also Negotiates"
    DEFAULT_DESCRIPTION = \
        "The server has an internal configuration error: the chosen variant resource is configured to engage in " \
        "transparent content negotiation itself, and is therefore not a proper end point in the negotiation process."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/507"


class NetworkAuthenticationRequired(HttpError):
    STATUS_CODE = 511
    TITLE = "Network Authentication Required"
    DEFAULT_DESCRIPTION = "The 511 status code indicates that the client needs to authenticate to gain network access."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/511"
