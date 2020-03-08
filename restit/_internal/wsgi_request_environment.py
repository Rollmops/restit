from enum import Enum
from typing import Dict

from restit._internal.common import create_dict_from_query_parameter_syntax


class RequestType(Enum):
    GET = "GET"
    DELETE = "DELETE"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    CONNECT = "CONNECT"
    TRACE = "TRACE"


class WsgiRequestEnvironment:
    def __init__(
            self, request_method: RequestType,
            path: str,
            query_parameters: Dict[str, str],
            wsgi_environment: dict,
            body: dict
    ):
        self.request_method = request_method
        self.path = path
        self.query_parameters = query_parameters
        self.wsgi_environment = wsgi_environment
        self.body = body

    @staticmethod
    def create_from_wsgi_environment_dict(environ: dict) -> "WsgiRequestEnvironment":
        wsgi_request_environment = WsgiRequestEnvironment(
            request_method=RequestType(environ["REQUEST_METHOD"]),
            path=environ["PATH_INFO"],
            query_parameters=create_dict_from_query_parameter_syntax(environ.get("QUERY_STRING")),
            body=WsgiRequestEnvironment._get_request_body(environ),
            wsgi_environment=environ,
        )
        return wsgi_request_environment

    @staticmethod
    def _get_request_body(environ: dict) -> dict:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size)
        return request_body
