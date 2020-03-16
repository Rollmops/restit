from http import HTTPStatus
from json import loads
from typing import Union, List

from werkzeug.exceptions import NotAcceptable

from restit.common import get_default_encoding
from restit.internal.default_response_serializer.default_bytes_text_response_serializer import \
    DefaultBytesTextResponseSerializer
from restit.internal.default_response_serializer.default_dict_json_response_serializer import \
    DefaultDictJsonResponseSerializer
from restit.internal.default_response_serializer.default_dict_text_response_serializer import \
    DefaultDictTextResponseSerializer
from restit.internal.default_response_serializer.default_str_text_response_serializer import \
    DefaultStrTextResponseSerializer
from restit.internal.http_accept import HttpAccept
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.response_serializer import ResponseSerializer

_DEFAULT_RESPONSE_SERIALIZER = [
    DefaultDictJsonResponseSerializer(),
    DefaultStrTextResponseSerializer(),
    DefaultBytesTextResponseSerializer(),
    DefaultDictTextResponseSerializer(),
]


class Response:
    _RESPONSE_SERIALIZER: List[ResponseSerializer] = _DEFAULT_RESPONSE_SERIALIZER.copy()

    def __init__(
            self,
            response_body: Union[str, dict, bytes],
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

    def validate_and_serialize_response_body(
            self, http_accept: HttpAccept, response_status_parameter: Union[None, ResponseStatusParameter] = None
    ):
        matching_response_serializer_list = self._get_matching_response_serializer_for_media_type(http_accept)
        if not matching_response_serializer_list:
            raise NotAcceptable()

        for response_serializer in matching_response_serializer_list:
            if isinstance(self._response_body_input, response_serializer.get_response_data_type()):
                self.content, content_type = response_serializer.validate_and_serialize(
                    self._response_body_input, response_status_parameter
                )
                self.text = self.content.decode(encoding=self.get_headers()["Content-Encoding"])
                self._set_headers(content_type)
                return

        raise Response.ResponseBodyTypeNotSupportedException(
            f"Unable to find response data serializer for {http_accept} and response data type "
            f"{type(self._response_body_input)}"
        )

    def _set_headers(self, content_type: str):
        self._headers.setdefault("Content-Type", content_type)
        self._headers.setdefault("Content-Length", len(self.content))

    @staticmethod
    def _get_matching_response_serializer_for_media_type(http_accept: HttpAccept) -> List[ResponseSerializer]:
        matching_response_serializer = [
            response_serializer
            for response_serializer in Response._RESPONSE_SERIALIZER
            if response_serializer.can_handle_incoming_media_type(http_accept)
        ]

        return sorted(matching_response_serializer, key=lambda s: s.priority, reverse=True)

    def get_status_string(self) -> str:
        return f"{self._status.value} {self._status.name}"

    def get_status_code(self) -> int:
        return self._status.value

    def json(self, **kwargs) -> dict:
        return loads(self.content.decode(encoding=self.get_headers()["Content-Encoding"]), **kwargs)

    def get_headers(self) -> dict:
        return self._headers

    def get_content_type(self, fallback: str = None) -> str:
        return self._headers.get("Content-Type", fallback or "application/octet-stream")

    class ResponseBodyTypeNotSupportedException(Exception):
        pass
