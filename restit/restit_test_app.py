from io import BytesIO
from json import dumps
from typing import Union
from urllib.parse import urlparse
from wsgiref.util import setup_testing_defaults

from restit import get_default_encoding
from restit.request import Request
from restit.response import Response
from restit.restit_app import RestitApp


class RestitTestApp(RestitApp):

    def __init__(self, restit_app: RestitApp, raise_exceptions: bool = False):
        super().__init__(
            resources=restit_app._resources,
            namespaces=restit_app._namespaces,
            expose_exceptions_to_sever=restit_app._expose_exceptions_to_sever,

        )
        self._raise_exceptions = raise_exceptions
        self._init()

    def set_raise_on_exceptions(self, raise_on_exceptions: bool):
        self._raise_exceptions = raise_on_exceptions

    def get(self, path: str, json: dict = None, data: dict = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "GET")

    def post(self, path: str, json: dict = None, data: dict = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "POST")

    def put(self, path: str, json: dict = None, data: dict = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "PUT")

    def delete(self, path: str, json: dict = None, data: dict = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "DELETE")

    def patch(self, path: str, json: dict = None, data: dict = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "PATCH")

    def options(self, path: str, json: dict = None, data: dict = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "OPTIONS")

    def _get_response_for_method(self, path: str, json: dict, data: dict, headers: dict, method: str):
        wsgi_environment = self._create_wsgi_environment(json, data, headers, path, method)
        response = self._get_response(wsgi_environment)
        return response

    def _get_response(self, wsgi_environment):
        request = Request(wsgi_environment)
        resource, path_params = self._find_resource_for_url(request.get_path())
        if self._raise_exceptions:
            return self._get_response_or_raise_not_found(path_params, request, resource)
        else:
            return self._create_response_and_handle_exceptions(path_params, request, resource)

    def _create_wsgi_environment(
            self, json: Union[dict, None], data: Union[dict, None], header: Union[dict, None], path: str, method: str
    ):
        header = header or {}
        wsgi_environment = {}
        setup_testing_defaults(wsgi_environment)
        body_as_bytes = b""
        if json is not None:
            body_as_bytes = dumps(json).encode(encoding=get_default_encoding())
        elif data is not None:
            body_as_bytes = dumps(data).encode(encoding=get_default_encoding())
        wsgi_environment["REQUEST_METHOD"] = method
        wsgi_environment["PATH_INFO"] = path
        wsgi_environment["CONTENT_LENGTH"] = len(body_as_bytes)
        wsgi_environment["wsgi.input"] = BytesIO(body_as_bytes)
        wsgi_environment["QUERY_STRING"] = urlparse(path).query
        wsgi_environment["HTTP_ACCEPT"] = header.get("Accept", "*/*")
        wsgi_environment["HTTP_ACCEPT_ENCODING"] = header.get("Accept-Encoding", "gzip, deflate")
        wsgi_environment["CONTENT_TYPE"] = header.get("Content-Type", self._get_content_type(json, data))
        return wsgi_environment

    @staticmethod
    def _get_content_type(json: Union[dict, None], data: Union[dict, None]):
        if json is not None:
            return "application/json"
        elif data is not None:
            return "application/x-www-form-urlencoded"
        else:
            return "*/*"
