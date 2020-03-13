from functools import lru_cache
from typing import List, Any, Type, Union

import werkzeug.wrappers
from werkzeug.datastructures import MIMEAccept

from restit.common import create_dict_from_query_parameter_syntax, get_default_encoding
from restit.internal.default_request_deserializer.default_any_bytes_deserializer import DefaultAnyBytesDeserializer
from restit.internal.default_request_deserializer.default_any_string_deserializer import DefaultAnyStringDeserializer
from restit.internal.default_request_deserializer.default_application_json_dict_deserializer import \
    DefaultApplicationJsonDictDeserializer
from restit.internal.default_request_deserializer.default_form_data_dict_deserializer import \
    DefaultFormDataDictDeserializer
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
        self._extended_request_info = werkzeug.wrappers.Request(wsgi_environment)
        self._query_parameters: dict = create_dict_from_query_parameter_syntax(
            self.get_extended_request_info().query_string, encoding=self.get_encoding()
        )
        self._body = self._get_body_from_wsgi_environment(wsgi_environment)

    @staticmethod
    def _get_body_from_wsgi_environment(wsgi_environment: dict) -> bytes:
        length = int(wsgi_environment.get("CONTENT_LENGTH", 0))
        return wsgi_environment["wsgi.input"].read(length)

    @staticmethod
    def register_request_deserializer(request_deserializer: RequestDeserializer):
        Request._REQUEST_DESERIALIZER.insert(0, request_deserializer)

    @staticmethod
    def clear_all_response_serializer():
        Request._REQUEST_DESERIALIZER.clear()

    @staticmethod
    def restore_default_response_serializer():
        Request._REQUEST_DESERIALIZER = _DEFAULT_REQUEST_DESERIALIZER.copy()

    # noinspection PyShadowingBuiltins
    def get_request_body_as_type(self, type: Type) -> Any:
        request_deserializer = self._find_deserializer(type)
        if request_deserializer is None:
            raise Request.NoRequestDeserializerFoundException(
                f"Unable to find a request deserializer from content type {self.get_content_type()} to type {type}"
            )
        return request_deserializer.deserialize(self._body, encoding=self.get_encoding())

    # noinspection PyShadowingBuiltins
    def is_body_deserializable_to_type(self, type: Type) -> bool:
        return self._find_deserializer(type) is not None

    # noinspection PyShadowingBuiltins
    @lru_cache()
    def _find_deserializer(self, type: Type) -> Union[RequestDeserializer, None]:
        for request_deserializer in Request._REQUEST_DESERIALIZER:
            if request_deserializer.can_handle_content_type(self.get_content_type()) and \
                    type == request_deserializer.get_deserialized_python_type():
                return request_deserializer

    def is_json(self) -> bool:
        return self._extended_request_info.content_type.lower() == "application/json"

    def get_extended_request_info(self) -> werkzeug.wrappers.Request:
        return self._extended_request_info

    def get_path(self) -> str:
        return self._extended_request_info.path

    def get_accepted_media_types(self) -> MIMEAccept:
        return self._extended_request_info.accept_mimetypes

    def get_request_method_name(self) -> str:
        return self._extended_request_info.method

    def get_headers(self) -> dict:
        return dict(self.get_extended_request_info().headers)

    def get_query_parameters(self) -> dict:
        return self._query_parameters

    def get_query_string(self) -> str:
        return self.get_extended_request_info().query_string.decode(self.get_encoding())

    def get_encoding(self) -> str:
        return self.get_headers().get("Content-Encoding", get_default_encoding())

    def get_content_type(self) -> str:
        return self.get_extended_request_info().content_type

    def get_body(self) -> bytes:
        return self._body

    def set_body_from_string(self, body: str):
        self._body = body.encode(self.get_encoding())

    class NoRequestDeserializerFoundException(Exception):
        pass
