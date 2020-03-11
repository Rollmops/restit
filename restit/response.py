from http import HTTPStatus
from json import loads
from typing import Union, List

from werkzeug.datastructures import MIMEAccept
from werkzeug.exceptions import NotAcceptable

from restit.common import get_default_encoding
from restit.response_serializer import ResponseSerializer
from restit.response_serializer.default_dict_json_response_serializer import DefaultDictJsonResponseSerializer
from restit.response_serializer.default_dict_text_response_serializer import DefaultDictTextResponseSerializer
from restit.response_serializer.default_str_text_response_serializer import DefaultStrTextResponseSerializer

_DEFAULT_RESPONSE_SERIALIZER = [
    DefaultDictJsonResponseSerializer(),
    DefaultStrTextResponseSerializer(),
    DefaultDictTextResponseSerializer(),
]


class Response:
    _RESPONSE_SERIALIZER: List[ResponseSerializer] = _DEFAULT_RESPONSE_SERIALIZER.copy()

    def __init__(
            self,
            response_body: Union[str, dict],
            status_code: Union[int, HTTPStatus] = 200,
            headers: dict = None
    ):
        self._response_body_input = response_body
        self._status: HTTPStatus = HTTPStatus(status_code, None) if isinstance(status_code, int) else status_code
        self._headers = headers or {}
        self._headers.setdefault("Content-Encoding", get_default_encoding())
        self.content = b""
        self.text = ""

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
            if isinstance(self._response_body_input, response_serializer.get_response_data_type()):
                self.content = response_serializer.serialize(self._response_body_input)
                self.text = self.content.decode(encoding=self.get_headers()["Content-Encoding"])
                self._set_headers(response_serializer)
                return

        raise Response.ResponseBodyTypeNotSupportedException(
            f"Unable to find response data serializer for media type {media_type} and response data type "
            f"{type(self._response_body_input)}"
        )

    def _set_headers(self, response_serializer: ResponseSerializer):
        self._headers.setdefault("Content-Type", response_serializer.get_content_type())
        self._headers.setdefault("Content-Length", len(self.content))

    @staticmethod
    def _get_matching_response_serializer_for_media_type(media_type: MIMEAccept) -> List[ResponseSerializer]:
        matching_response_serializer = [
            response_serializer
            for response_serializer in Response._RESPONSE_SERIALIZER
            if response_serializer.can_handle_incoming_media_type(media_type)
        ]

        return sorted(matching_response_serializer, key=lambda s: s.priority)

    def get_status_string(self) -> str:
        return f"{self._status.value} {self._status.name}"

    def get_status_code(self) -> int:
        return self._status.value

    def json(self, **kwargs) -> dict:
        return loads(self.content.decode(encoding=self.get_headers()["Content-Encoding"]), **kwargs)

    def get_headers(self) -> dict:
        return self._headers

    class ResponseBodyTypeNotSupportedException(Exception):
        pass
