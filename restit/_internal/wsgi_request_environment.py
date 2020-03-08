from enum import Enum
from functools import lru_cache
from typing import Dict


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
            self, request_method: RequestType, path: str, query_parameters: Dict[str, str], wsgi_environment: dict
    ):
        self.request_method = request_method
        self.path = path
        self.query_parameters = query_parameters
        self.wsgi_environment = wsgi_environment

    @staticmethod
    def create_from_wsgi_environment_dict(environ: dict) -> "WsgiRequestEnvironment":
        wsgi_request_environment = WsgiRequestEnvironment(
            request_method=RequestType(environ["REQUEST_METHOD"]),
            path=environ["PATH_INFO"],
            query_parameters=WsgiRequestEnvironment._create_query_parameters_from_query_string(
                environ.get("QUERY_STRING")
            ),
            wsgi_environment=environ
        )
        return wsgi_request_environment

    @staticmethod
    @lru_cache()
    def _create_query_parameters_from_query_string(query_string: str) -> dict:
        query_parameters = {}
        if query_string is None or "=" not in query_string:
            return query_parameters
        for query_string_pair in query_string.split("&"):
            try:
                key, value = query_string_pair.split("=")
                query_parameters[key] = value
            except ValueError:
                pass

        return query_parameters
