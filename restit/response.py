from http import HTTPStatus
from json import loads
from typing import Union, Any

from restit.common import get_default_encoding


class Response:

    def __init__(
            self,
            response_body: Any,
            status_code: Union[int, HTTPStatus] = 200,
            headers: dict = None
    ):
        self.response_body_input = response_body
        self._status: HTTPStatus = HTTPStatus(status_code, None) if isinstance(status_code, int) else status_code
        self._headers = headers or {}
        self._headers.setdefault("Content-Encoding", get_default_encoding())
        self.content = b""
        self.text = ""

    def _prepare_headers(self, content_type: str):
        self._headers.setdefault("Content-Type", content_type)
        self._headers.setdefault("Content-Length", len(self.content))

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
