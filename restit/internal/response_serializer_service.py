from typing import List, Union, Tuple

from restit._response import Response
from restit.exception import NotAcceptable
from restit.internal.default_response_serializer.default_bytes_text_response_serializer import \
    DefaultBytesTextResponseSerializer
from restit.internal.default_response_serializer.default_dict_json_response_serializer import \
    DefaultDictJsonResponseSerializer, DefaultListJsonResponseSerializer
from restit.internal.default_response_serializer.default_dict_text_response_serializer import \
    DefaultDictTextResponseSerializer, DefaultListTextResponseSerializer
from restit.internal.default_response_serializer.default_str_text_response_serializer import \
    DefaultStrTextResponseSerializer
from restit.internal.default_response_serializer.dict_fallback_response_serializer import DictFallbackResponseSerializer
from restit.internal.default_response_serializer.str_fallback_response_serializer import \
    StringFallbackResponseSerializer
from restit.internal.http_accept import HttpAccept
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.response_serializer import ResponseSerializer, CanHandleResultType

_DEFAULT_RESPONSE_SERIALIZER = [
    DefaultDictJsonResponseSerializer(),
    DefaultStrTextResponseSerializer(),
    DefaultBytesTextResponseSerializer(),
    DefaultDictTextResponseSerializer(),
    DictFallbackResponseSerializer(),
    StringFallbackResponseSerializer(),
    DefaultListJsonResponseSerializer(),
    DefaultListTextResponseSerializer()
]


class ResponseSerializerService:
    _RESPONSE_SERIALIZER: List[ResponseSerializer] = _DEFAULT_RESPONSE_SERIALIZER.copy()

    @staticmethod
    def register_response_serializer(response_serializer: ResponseSerializer):
        ResponseSerializerService._RESPONSE_SERIALIZER.insert(0, response_serializer)

    @staticmethod
    def clear_all_response_serializer():
        ResponseSerializerService._RESPONSE_SERIALIZER = []

    @staticmethod
    def restore_default_response_serializer():
        ResponseSerializerService._RESPONSE_SERIALIZER = _DEFAULT_RESPONSE_SERIALIZER.copy()

    @staticmethod
    def get_matching_response_serializer_for_media_type(
            http_accept: HttpAccept) -> List[Tuple[ResponseSerializer, CanHandleResultType]]:
        response_serializer_matches = []
        for response_serializer in ResponseSerializerService._RESPONSE_SERIALIZER:
            can_handle_result = response_serializer.can_handle_incoming_media_type(http_accept)
            if can_handle_result is not None:
                response_serializer_matches.append((response_serializer, can_handle_result))

        return sorted(response_serializer_matches, key=lambda c: c[1].mime_type.quality, reverse=True)

    @staticmethod
    def validate_and_serialize_response_body(
            response: Response, http_accept: HttpAccept,
            response_status_parameter: Union[None, ResponseStatusParameter] = None
    ):
        matching_response_serializer_list = ResponseSerializerService.get_matching_response_serializer_for_media_type(
            http_accept
        )
        if not matching_response_serializer_list:
            raise NotAcceptable()

        for response_serializer, can_handle_result in matching_response_serializer_list:
            if isinstance(response.response_body_input, response_serializer.get_response_data_type()):
                response.content, content_type = response_serializer.validate_and_serialize(
                    response.response_body_input, response_status_parameter, can_handle_result
                )
                # Todo encoding from incoming accept charset
                try:
                    response.text = response.content.decode()
                except UnicodeDecodeError:
                    response.text = None
                response._prepare_headers(content_type)
                return

        raise Response.ResponseBodyTypeNotSupportedException(
            f"Unable to find response data serializer for {http_accept} and response data type "
            f"{type(response.response_body_input)}"
        )
