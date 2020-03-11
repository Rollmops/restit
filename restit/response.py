from http import HTTPStatus
from typing import Union, List

from werkzeug.datastructures import MIMEAccept
from werkzeug.exceptions import NotAcceptable

from restit import _DEFAULT_ENCODING
from restit.response_serializer import ResponseSerializer
from restit.response_serializer.default_dict_json_response_serializer import DefaultDictJsonResponseSerializer
from restit.response_serializer.default_dict_text_response_serializer import DefaultDictTextResponseSerializer
from restit.response_serializer.default_str_text_response_serializer import DefaultStrTextResponseSerializer

_DEFAULT_RESPONSE_SERIALIZER = [
    DefaultDictJsonResponseSerializer(),
    DefaultStrTextResponseSerializer(),
    DefaultDictTextResponseSerializer()
]


class Response:
    _RESPONSE_SERIALIZER: List[ResponseSerializer] = _DEFAULT_RESPONSE_SERIALIZER.copy()

    def __init__(
            self,
            response_body: Union[str, dict],
            status_code: Union[int, HTTPStatus] = 200,
            header: dict = None, encoding=None
    ):
        self.response_body = response_body
        self.status_code: HTTPStatus = HTTPStatus(status_code, None) if isinstance(status_code, int) else status_code
        self.header = header or {}
        self.encoding = encoding or _DEFAULT_ENCODING
        self.body_as_bytes = b""

    @staticmethod
    def register_response_serializer(response_serializer: ResponseSerializer):
        Response._RESPONSE_SERIALIZER.insert(0, response_serializer)

    @staticmethod
    def clear_all_response_serializer():
        Response._RESPONSE_SERIALIZER = []

    @staticmethod
    def restore_default_response_serializer():
        Response._RESPONSE_SERIALIZER = _DEFAULT_RESPONSE_SERIALIZER.copy()

    def serialize_response_body(self, media_type: MIMEAccept):
        matching_response_serializer_list = self._get_matching_response_serializer_for_media_type(media_type)
        if not matching_response_serializer_list:
            raise NotAcceptable()

        for response_serializer in matching_response_serializer_list:
            if isinstance(self.response_body, response_serializer.get_response_data_type()):
                self.body_as_bytes = response_serializer.serialize(self.response_body)
                self.header["Content-Type"] = response_serializer.get_content_type()
                return

        raise Response.ResponseBodyTypeNotSupportedException(
            f"Unable to find response data serializer for media type {media_type} and response data type "
            f"{type(self.response_body)}"
        )

    @staticmethod
    def _get_matching_response_serializer_for_media_type(media_type: MIMEAccept) -> List[ResponseSerializer]:
        matching_response_serializer = [
            response_serializer
            for response_serializer in Response._RESPONSE_SERIALIZER
            if response_serializer.can_handle_incoming_media_type(media_type)
        ]

        return sorted(matching_response_serializer, key=lambda s: s.priority)

    def get_status(self) -> str:
        return f"{self.status_code.value} {self.status_code.name}"

    class ResponseBodyTypeNotSupportedException(Exception):
        pass
