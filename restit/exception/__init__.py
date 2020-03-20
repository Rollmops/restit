from .client_errors_4xx import MethodNotAllowed, BadRequest, NotFound, UnsupportedMediaType, UnprocessableEntity, \
    NotAcceptable, TooManyRequests, Conflict, ExpectationFailed, Forbidden, Gone, LengthRequired, MisdirectedRequest, \
    PayloadTooLarge, PaymentRequired, PreconditionFailed, PreconditionRequired, ProxyAuthenticationRequired, \
    RequestedRangeNotSatisfiable, RequestHeaderFieldsTooLarge, RequestTimeout, Unauthorized, UnavailableForLegalReasons, \
    UpgradeRequired, URITooLong
from .http_error import HttpError
from .redirection_messages_3xx import Found, MovedPermanently, MultipleChoice, NotModified, PermanentRedirect, SeeOther, \
    TemporaryRedirect, UseProxy
from .server_errors_5xx import InternalServerError, NotImplemented, HTTPVersionNotSupported, ServiceUnavailable, \
    BadGateway, GatewayTimeout, NetworkAuthenticationRequired, VariantAlsoNegotiates, VariantAlsoNegotiates507


class MissingRequestMappingException(Exception):
    pass


class PathIsNotStartingWithSlashException(Exception):
    pass
