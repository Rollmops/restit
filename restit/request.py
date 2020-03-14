from functools import lru_cache
from typing import List, Any, Type, Union

import werkzeug

from restit.common import create_dict_from_assignment_syntax, get_default_encoding
from restit.internal.default_request_deserializer.default_any_bytes_deserializer import DefaultAnyBytesDeserializer
from restit.internal.default_request_deserializer.default_any_string_deserializer import DefaultAnyStringDeserializer
from restit.internal.default_request_deserializer.default_application_json_dict_deserializer import \
    DefaultApplicationJsonDictDeserializer
from restit.internal.default_request_deserializer.default_form_data_dict_deserializer import \
    DefaultFormDataDictDeserializer
from restit.internal.http_accept import HttpAccept
from restit.request_deserializer import RequestDeserializer

_DEFAULT_REQUEST_DESERIALIZER = [
    DefaultApplicationJsonDictDeserializer(),
    DefaultFormDataDictDeserializer(),
    DefaultAnyBytesDeserializer(),
    DefaultAnyStringDeserializer()
]


class Request:
    _REQUEST_DESERIALIZER: List[RequestDeserializer] = _DEFAULT_REQUEST_DESERIALIZER.copy()

    def __init__(self, wsgi_environment: dict):
        self._wsgi_environment = wsgi_environment
        self._content_length = int(wsgi_environment.get("CONTENT_LENGTH", 0) or 0)
        self._headers = wsgi_environment
        self._query_string = wsgi_environment["QUERY_STRING"]
        self._path = wsgi_environment["PATH_INFO"]
        self._method_name = wsgi_environment["REQUEST_METHOD"]
        self._content_type = wsgi_environment["CONTENT_TYPE"]

        self._query_parameters: dict = create_dict_from_assignment_syntax(self._query_string)

        self._http_accept = HttpAccept.from_accept_string(wsgi_environment["HTTP_ACCEPT"])
        self._body = self._get_body_from_wsgi_environment(wsgi_environment)

    def _get_body_from_wsgi_environment(self, wsgi_environment: dict) -> bytes:
        return wsgi_environment["wsgi.input"].read(self._content_length)

    @staticmethod
    def register_request_deserializer(request_deserializer: RequestDeserializer):
        Request._REQUEST_DESERIALIZER.insert(0, request_deserializer)

    @staticmethod
    def clear_all_response_serializer():
        Request._REQUEST_DESERIALIZER.clear()

    @staticmethod
    def restore_default_response_serializer():
        Request._REQUEST_DESERIALIZER = _DEFAULT_REQUEST_DESERIALIZER.copy()

    def get_request_body_as_type(self, python_type: Type) -> Any:
        request_deserializer = self._find_deserializer(python_type)
        if request_deserializer is None:
            raise Request.NoRequestDeserializerFoundException(
                f"Unable to find a request deserializer from content type {self.get_content_type()} "
                f"to type {python_type}"
            )
        return request_deserializer.deserialize(self._body, encoding=self.get_encoding())

    def is_body_deserializable_to_type(self, python_type: Type) -> bool:
        return self._find_deserializer(python_type) is not None

    @lru_cache()
    def _find_deserializer(self, python_type: Type) -> Union[RequestDeserializer, None]:
        for request_deserializer in Request._REQUEST_DESERIALIZER:
            if request_deserializer.can_handle(self.get_content_type(), python_type):
                return request_deserializer

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
        return self.get_headers().get("CONTENT_ENCODING", get_default_encoding())

    def get_content_type(self) -> str:
        return self._content_type

    def get_body(self) -> bytes:
        return self._body

    def get_http_accept(self) -> HttpAccept:
        return self._http_accept

    def set_body_from_string(self, body: str):
        self._body = body.encode(self.get_encoding())

    @lru_cache(maxsize=1)
    def get_werkzeug_request(self) -> werkzeug.wrappers.Request:
        return werkzeug.wrappers.Request(self._wsgi_environment)

    class NoRequestDeserializerFoundException(Exception):
        pass
