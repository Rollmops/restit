from io import BytesIO
from json import dumps
from typing import Union, Tuple
from urllib.parse import urlparse
from wsgiref.util import setup_testing_defaults

from restit.common import get_default_encoding
from restit.request import Request
from restit.response import Response
from restit.restit_app import RestItApp


class RestItTestApp(RestItApp):

    def __init__(self, restit_app: RestItApp):
        super().__init__(
            resources=restit_app._resources,
            namespaces=restit_app._namespaces,
            debug=restit_app.debug,
            raise_exceptions=restit_app.raise_exceptions
        )
        self._init()

    def get(self, path: str, json: dict = None, data: Union[dict, str, bytes] = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "GET")

    def post(
            self, path: str, json: dict = None, data: Union[dict, str, bytes] = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "POST")

    def put(
            self, path: str, json: dict = None, data: Union[dict, str, bytes] = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "PUT")

    def delete(
            self, path: str, json: dict = None, data: Union[dict, str, bytes] = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "DELETE")

    def patch(
            self, path: str, json: dict = None, data: Union[dict, str, bytes] = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "PATCH")

    def options(
            self, path: str, json: dict = None, data: Union[dict, str, bytes] = None, headers: dict = None) -> Response:
        return self._get_response_for_method(path, json, data, headers, "OPTIONS")

    def _get_response_for_method(
            self, path: str, json: dict, data: Union[dict, str, bytes], headers: dict, method: str):
        wsgi_environment = self._create_wsgi_environment(json, data, headers, path, method)
        response = self._get_response(wsgi_environment)
        return response

    def _get_response(self, wsgi_environment: dict):
        resource, path_params = self._find_resource_for_url(wsgi_environment["PATH_INFO"])
        request = Request(wsgi_environment, path_params)
        if self.raise_exceptions:
            return self._get_response_or_raise_not_found(path_params, request, resource)
        else:
            return self._create_response_and_handle_exceptions(path_params, request, resource)

    def _create_wsgi_environment(
            self, json: Union[dict, None], data: Union[dict, None], header: Union[dict, None], path: str, method: str
    ):
        header = header or {}
        wsgi_environment = {}
        parsed_path = urlparse(path)
        setup_testing_defaults(wsgi_environment)
        body_as_bytes = b""
        wsgi_environment["HTTP_ACCEPT"] = header.get("Accept", "*/*")
        wsgi_environment["CONTENT_ENCODING"] = header.get("Content-Encoding", "gzip, deflate")
        wsgi_environment["HTTP_ACCEPT_ENCODING"] = header.get("Accept-Encoding", "gzip, deflate")
        content_type = "application/octet-stream"
        accept_charset = header.get("Accept-Charset", get_default_encoding())
        if json is not None:
            body_as_bytes = dumps(json).encode(encoding=accept_charset)
            content_type = "application/json"
        elif data is not None:
            body_as_bytes, content_type = \
                self._get_body_as_bytes_from_data_argument(data, accept_charset)
        wsgi_environment["REQUEST_METHOD"] = method
        wsgi_environment["PATH_INFO"] = parsed_path.path
        wsgi_environment["CONTENT_LENGTH"] = len(body_as_bytes)
        wsgi_environment["wsgi.input"] = BytesIO(body_as_bytes)
        wsgi_environment["QUERY_STRING"] = parsed_path.query
        wsgi_environment["CONTENT_TYPE"] = header.get("Content-Type", content_type)
        self._set_header_values(wsgi_environment, header)
        return wsgi_environment

    @staticmethod
    def _set_header_values(wsgi_environment: dict, headers: dict):
        for key, value in headers.items():
            wsgi_key = "HTTP_" + key.upper().replace("-", "_")
            wsgi_environment.setdefault(wsgi_key, value)

    @staticmethod
    def _get_body_as_bytes_from_data_argument(
            data: Union[dict, str, bytes], accept_charset: str) -> Tuple[bytes, str]:
        if isinstance(data, dict):
            body_as_bytes = "&".join([f"{key}={value}" for key, value in data.items()])
            return body_as_bytes.encode(encoding=accept_charset), "application/x-www-form-urlencoded"
        elif isinstance(data, str):
            return data.encode(encoding=accept_charset), "text/plain"
        elif isinstance(data, bytes):
            return data, "text/plain"
        else:
            raise RestItTestApp.UnsupportedDataTypeException(type(data))

    class UnsupportedDataTypeException(Exception):
        pass
