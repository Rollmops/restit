from restit.exception.http_error import HttpError


class BadRequest(HttpError):
    STATUS_CODE = 400
    TITLE = "Bad Request"
    DEFAULT_DESCRIPTION = \
        "This response means that server could not understand the request due to invalid syntax."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/400"


class Unauthorized(HttpError):
    STATUS_CODE = 401
    TITLE = "Unauthorized"
    DEFAULT_DESCRIPTION = \
        "Authentication is needed to get requested response. This is similar to 403, but in this case, " \
        "authentication is possible."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/401"


class PaymentRequired(HttpError):
    STATUS_CODE = 402
    TITLE = "Payment Required"
    DEFAULT_DESCRIPTION = \
        "This response code is reserved for future use. Initial aim for creating this code was using it for digital " \
        "payment systems however this is not used currently."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/402"


class Forbidden(HttpError):
    STATUS_CODE = 403
    TITLE = "Forbidden"
    DEFAULT_DESCRIPTION = \
        "Client does not have access rights to the content so server is rejecting to give proper response."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/403"


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


class ProxyAuthenticationRequired(HttpError):
    STATUS_CODE = 407
    TITLE = "Proxy Authentication Required"
    DEFAULT_DESCRIPTION = "This is similar to 401 but authentication is needed to be done by a proxy."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/407"


class RequestTimeout(HttpError):
    STATUS_CODE = 408
    TITLE = "Request Timeout"
    DEFAULT_DESCRIPTION = \
        "This response is sent on an idle connection by some servers, even without any previous request by the client. " \
        "It means that the server would like to shut down this unused connection. This response is used much more " \
        "since some browsers, like Chrome or IE9, use HTTP preconnection mechanisms to speed up surfing (see Bug " \
        "881804, which tracks the future implementation of such a mechanism in Firefox). Also note that some servers " \
        "merely shut down the connection without sending this message."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/408"


class Conflict(HttpError):
    STATUS_CODE = 409
    TITLE = "Conflict"
    DEFAULT_DESCRIPTION = "This response would be sent when a request conflict with current state of server."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/409"


class Gone(HttpError):
    STATUS_CODE = 410
    TITLE = "Gone"
    DEFAULT_DESCRIPTION = "This response would be sent when requested content has been deleted from server."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/410"


class LengthRequired(HttpError):
    STATUS_CODE = 411
    TITLE = "Length Required"
    DEFAULT_DESCRIPTION = \
        "Server rejected the request because the Content-Length header field is not defined and the server requires it."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/411"


class PreconditionFailed(HttpError):
    STATUS_CODE = 412
    TITLE = "Precondition Failed"
    DEFAULT_DESCRIPTION = "The client has indicated preconditions in its headers which the server does not meet."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/412"


class PayloadTooLarge(HttpError):
    STATUS_CODE = 413
    TITLE = "Payload Too Large"
    DEFAULT_DESCRIPTION = \
        "Request entity is larger than limits defined by server; the server might close the connection or return an " \
        "Retry-After header field."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/413"


class URITooLong(HttpError):
    STATUS_CODE = 414
    TITLE = "URI Too Long"
    DEFAULT_DESCRIPTION = "The URI requested by the client is longer than the server is willing to interpret."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/414"


class UnsupportedMediaType(HttpError):
    STATUS_CODE = 415
    TITLE = "Unsupported Media Type"
    DEFAULT_DESCRIPTION = \
        "The media format of the requested data is not supported by the server, so the server is rejecting the request."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/415"


class RequestedRangeNotSatisfiable(HttpError):
    STATUS_CODE = 416
    TITLE = "Requested Range Not Satisfiable"
    DEFAULT_DESCRIPTION = \
        "The range specified by the Range header field in the request can't be fulfilled; it's possible that the " \
        "range is outside the size of the target URI's data."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/416"


class ExpectationFailed(HttpError):
    STATUS_CODE = 417
    TITLE = "Expectation Failed"
    DEFAULT_DESCRIPTION = \
        "This response code means the expectation indicated by the Expect request header field can't be met by the " \
        "server."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/417"


class MisdirectedRequest(HttpError):
    STATUS_CODE = 421
    TITLE = "Misdirected Request"
    DEFAULT_DESCRIPTION = \
        "The request was directed at a server that is not able to produce a response. This can be sent by a server " \
        "that is not configured to produce responses for the combination of scheme and authority that are " \
        "included in the request URI."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/421"


class UnprocessableEntity(HttpError):
    STATUS_CODE = 422
    TITLE = "Unprocessable Entity"
    DEFAULT_DESCRIPTION = \
        "Indicates that the server understands the content type of the request entity, and the syntax of the request " \
        "entity is correct, but it was unable to process the contained instructions."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/422"


class UpgradeRequired(HttpError):
    STATUS_CODE = 426
    TITLE = "Upgrade Required"
    DEFAULT_DESCRIPTION = \
        "The server refuses to perform the request using the current protocol but might be willing to do so after " \
        "the client upgrades to a different protocol. The server MUST send an Upgrade header field in a 426 " \
        "response to indicate the required protocol(s) (Section 6.7 of [RFC7230])."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/426"


class PreconditionRequired(HttpError):
    STATUS_CODE = 428
    TITLE = "Precondition Required"
    DEFAULT_DESCRIPTION = \
        "The origin server requires the request to be conditional. Intended to prevent the 'lost update' problem, " \
        "where a client GETs a resource's state, modifies it, and PUTs it back to the server, when meanwhile a " \
        "third party has modified the state on the server, leading to a conflict."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/428"


class TooManyRequests(HttpError):
    STATUS_CODE = 429
    TITLE = "Too Many Requests"
    DEFAULT_DESCRIPTION = "The user has sent too many requests in a given amount of time (\"rate limiting\")."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/429"


class RequestHeaderFieldsTooLarge(HttpError):
    STATUS_CODE = "431"
    TITLE = "Request Header Fields Too Large"
    DEFAULT_DESCRIPTION = \
        "The server is unwilling to process the request because its header fields are too large. The request MAY be " \
        "resubmitted after reducing the size of the request header fields."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/431"


class UnavailableForLegalReasons(HttpError):
    STATUS_CODE = 451
    TITLE = "Unavailable For Legal Reasons"
    DEFAULT_DESCRIPTION = "The user requests an illegal resource, such as a web page censored by a government."
    DEFAULT_RFC7807_TYPE = "https://developer.mozilla.org/de/docs/Web/HTTP/Status/451"
