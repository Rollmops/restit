from functools import lru_cache
from io import BufferedReader
from typing import Any
from urllib.parse import quote

from restit.common import create_dict_from_assignment_syntax
from restit.internal.forwarded_header import ForwardedHeader
from restit.internal.http_accept import HttpAccept
from restit.internal.mime_type import MIMEType
from restit.internal.request_deserializer_service import RequestDeserializerService
from restit.internal.typed_body import TypedBody


class Request:
    """https://www.python.org/dev/peps/pep-0333/"""

    def __init__(self, wsgi_environment: dict, path_params: dict):
        self._wsgi_environment = wsgi_environment
        self._path_params = path_params
        self._query_string = wsgi_environment["QUERY_STRING"]
        self._path = wsgi_environment["PATH_INFO"]
        self._method_name = wsgi_environment["REQUEST_METHOD"]

        self._query_parameters: dict = create_dict_from_assignment_syntax(self._query_string)
        self._headers = self._create_headers()

        self._forwarded = ForwardedHeader.from_headers(self._headers)

        self._typed_body = TypedBody(self.body, self.content_type)
        self._deserialized_body = None

        self._request_deserializer_service = RequestDeserializerService()

    def _create_headers(self):
        headers = {
            "Content-Type": self._wsgi_environment.get("CONTENT_TYPE"),
            "Content-Length": int(self._wsgi_environment.get("CONTENT_LENGTH", 0) or 0),
            "Content-Encoding": self._wsgi_environment.get("CONTENT_ENCODING"),
        }

        for key, value in self._wsgi_environment.items():
            if key.startswith("HTTP_"):
                header_key = key[5:].replace("_", "-").title()
                headers[header_key] = value

        return headers

    @lru_cache()
    def _get_body_from_wsgi_environment(self, buffered_input: BufferedReader) -> bytes:
        body = buffered_input.read(self.headers["Content-Length"])
        return body

    def is_json(self) -> bool:
        return self.content_type.to_string() == "application/json"

    @property
    def path(self) -> str:
        return self._path

    @property
    def request_method_name(self) -> str:
        return self._method_name

    @property
    def headers(self) -> dict:
        return self._headers

    @property
    def query_parameters(self) -> dict:
        return self._query_parameters

    @property
    def path_parameters(self) -> dict:
        return self._path_params

    @property
    def query_string(self) -> str:
        return self._query_string

    @property
    @lru_cache()
    def host(self) -> str:
        host = self.forwarded.host or self._headers.get("Host")
        if host is None:
            host = (self.forwarded.server or self._wsgi_environment["SERVER_NAME"])
            port = self._wsgi_environment['SERVER_PORT']
            if port != 443 and port != 80:
                host += f":{port}"

        return self.protocol + "://" + host

    @property
    def protocol(self) -> str:
        return self.forwarded.proto or self._wsgi_environment['wsgi.url_scheme']

    @property
    def content_encoding(self) -> str:
        return self._headers.get("Content-Encoding")

    @property
    def content_type(self) -> MIMEType:
        return MIMEType.from_string(self._headers.get("Content-Type") or "text/plain")

    @property
    def body(self) -> bytes:
        return self._get_body_from_wsgi_environment(self._wsgi_environment["wsgi.input"])

    @property
    def typed_body(self) -> TypedBody:
        return self._typed_body

    @property
    def forwarded(self) -> ForwardedHeader:
        return self._forwarded

    @property
    def deserialized_body(self):
        if self._deserialized_body is None:
            self.deserialized_body = self.typed_body[dict]
        return self._deserialized_body

    @deserialized_body.setter
    def deserialized_body(self, body: Any):
        if self._deserialized_body is None:
            self._deserialized_body = body
        else:
            raise Request.DeserializedBodyAlreadySetException()

    @property
    def http_accept_object(self) -> HttpAccept:
        return HttpAccept.from_accept_string(self.headers.get("Accept", "*/*"))

    @property
    def original_url(self) -> str:
        """https://www.python.org/dev/peps/pep-0333/#url-reconstruction"""
        url = self.host

        url += quote(self._wsgi_environment.get('SCRIPT_NAME', ''))
        url += quote(self._wsgi_environment.get('PATH_INFO', ''))
        if self._wsgi_environment.get('QUERY_STRING'):
            url += '?' + self._wsgi_environment['QUERY_STRING']

        return url

    def __str__(self) -> str:
        return f"Request(url={self.original_url}"

    class DeserializedBodyAlreadySetException(Exception):
        pass
