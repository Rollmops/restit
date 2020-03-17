from functools import lru_cache
from typing import Any, Type
from urllib.parse import quote

import werkzeug

from restit.common import create_dict_from_assignment_syntax, get_default_encoding
from restit.internal.http_accept import HttpAccept
from restit.internal.request_deserializer_service import RequestDeserializerService


class Request:
    """https://www.python.org/dev/peps/pep-0333/"""

    def __init__(self, wsgi_environment: dict):
        self._wsgi_environment = wsgi_environment
        self._content_length = int(wsgi_environment.get("CONTENT_LENGTH", 0) or 0)
        self._query_string = wsgi_environment["QUERY_STRING"]
        self._path = wsgi_environment["PATH_INFO"]
        self._method_name = wsgi_environment["REQUEST_METHOD"]

        self._query_parameters: dict = create_dict_from_assignment_syntax(self._query_string)
        self._headers = self._get_headers(wsgi_environment)
        self._body = None

        self._request_deserializer_service = RequestDeserializerService()
        self._body_type_cache = {}

    @staticmethod
    def _get_headers(wsgi_environment: dict) -> dict:
        header = {
            "Accept": wsgi_environment.get("HTTP_ACCEPT", "*/*"),
            "Accept-Encoding": wsgi_environment.get("HTTP_ACCEPT_ENCODING", get_default_encoding()),
            "Content-Type": wsgi_environment.get("CONTENT_TYPE"),
            "Content-Encoding": wsgi_environment.get("CONTENT_ENCODING"),
            "Accept-Charset": wsgi_environment.get("HTTP_ACCEPT_CHARSET", get_default_encoding())
        }
        return {
            key: value for key, value in header.items() if value is not None
        }

    def _get_body_from_wsgi_environment(self, wsgi_environment: dict) -> bytes:
        return wsgi_environment["wsgi.input"].read(self._content_length)

    @lru_cache()
    def get_request_body_as_type(self, python_type: Type) -> Any:
        return self._body_type_cache.get(
            python_type,
            self._request_deserializer_service.deserialize_request_body(
                self.get_body(), self.get_content_type(), python_type,
                self.get_headers().get("Accept-Charset", get_default_encoding())
            )
        )

    def is_body_deserializable_to_type(self, python_type: Type) -> bool:
        return self._request_deserializer_service.is_body_deserializable_to_type(self.get_content_type(), python_type)

    def is_json(self) -> bool:
        return self.get_content_type().lower() == "application/json"

    def get_path(self) -> str:
        return self._path

    def get_request_method_name(self) -> str:
        return self._method_name

    def get_headers(self) -> dict:
        return self._headers

    def get_query_parameters(self) -> dict:
        return self._query_parameters

    def get_query_string(self) -> str:
        return self._query_string

    def get_encoding(self) -> str:
        return self._headers["Content-Encoding"]

    def get_content_type(self) -> str:
        return self._headers["Content-Type"]

    def get_body(self) -> bytes:
        if not self._body:
            self._body = self._get_body_from_wsgi_environment(self._wsgi_environment)
        return self._body

    def get_http_accept(self) -> str:
        return self.get_headers()["Accept"]

    @lru_cache(maxsize=1)
    def get_http_accept_object(self) -> HttpAccept:
        return HttpAccept.from_accept_string(self.get_http_accept())

    def set_body_from_string(self, body: str):
        self._body = body.encode(self.get_encoding())

    @lru_cache(maxsize=1)
    def get_werkzeug_request(self) -> werkzeug.wrappers.Request:
        return werkzeug.wrappers.Request(self._wsgi_environment)

    @lru_cache()
    def get_host_url(self) -> str:
        """https://www.python.org/dev/peps/pep-0333/#url-reconstruction"""
        url = self._wsgi_environment['wsgi.url_scheme'] + '://'

        if self._wsgi_environment.get('HTTP_HOST'):
            url += self._wsgi_environment['HTTP_HOST']
        else:
            url += self._wsgi_environment['SERVER_NAME']

            if self._wsgi_environment['wsgi.url_scheme'] == 'https':
                if self._wsgi_environment['SERVER_PORT'] != '443':
                    url += ':' + self._wsgi_environment['SERVER_PORT']
            else:
                if self._wsgi_environment['SERVER_PORT'] != '80':
                    url += ':' + self._wsgi_environment['SERVER_PORT']

        return url

    @lru_cache()
    def get_original_url(self) -> str:
        """https://www.python.org/dev/peps/pep-0333/#url-reconstruction"""
        url = self.get_host_url()

        url += quote(self._wsgi_environment.get('SCRIPT_NAME', ''))
        url += quote(self._wsgi_environment.get('PATH_INFO', ''))
        if self._wsgi_environment.get('QUERY_STRING'):
            url += '?' + self._wsgi_environment['QUERY_STRING']

        return url
