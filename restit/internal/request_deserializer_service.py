from functools import lru_cache
from typing import List, Type, Union, Any

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


class RequestDeserializerService:
    _REQUEST_DESERIALIZER: List[RequestDeserializer] = _DEFAULT_REQUEST_DESERIALIZER.copy()

    @staticmethod
    def register_request_deserializer(request_deserializer: RequestDeserializer):
        RequestDeserializerService._REQUEST_DESERIALIZER.insert(0, request_deserializer)

    @staticmethod
    def clear_all_request_deserializers():
        RequestDeserializerService._REQUEST_DESERIALIZER.clear()

    @staticmethod
    def restore_default_request_deserializers():
        RequestDeserializerService._REQUEST_DESERIALIZER = _DEFAULT_REQUEST_DESERIALIZER.copy()

    @staticmethod
    def is_body_deserializable_to_type(content_type: str, python_type: Type) -> bool:
        return RequestDeserializerService._find_deserializer(content_type, python_type) is not None

    @staticmethod
    def deserialize_request_body(body: bytes, content_type: str, python_type: Type, encoding: str) -> Any:
        request_deserializer = RequestDeserializerService._find_deserializer(content_type, python_type)
        if request_deserializer is None:
            raise RequestDeserializerService.NoRequestDeserializerFoundException(
                f"Unable to find a request deserializer from content type {content_type} "
                f"to type {python_type}"
            )
        deserialized_value = request_deserializer.deserialize(body, encoding=encoding)
        return deserialized_value

    @staticmethod
    @lru_cache()
    def _find_deserializer(content_type: str, python_type: Type) -> Union[RequestDeserializer, None]:
        for request_deserializer in RequestDeserializerService._REQUEST_DESERIALIZER:
            if request_deserializer.can_handle(content_type, python_type):
                return request_deserializer

    class NoRequestDeserializerFoundException(Exception):
        pass
