from http import HTTPStatus
from json import loads
from typing import Union, Any


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
        self._headers.setdefault("Content-Encoding", None)
        self.content = b""
        self.text = ""

    def _prepare_headers(self, content_type: str):
        self._headers.setdefault("Content-Type", content_type)
        self._headers.setdefault("Content-Length", len(self.content))

    @property
    def status_code(self) -> int:
        return self._status.value

    @property
    def status_string(self) -> str:
        return f"{self._status.value} {self._status.name}"

    def json(self, **kwargs) -> dict:
        return loads(self.content.decode(), **kwargs)

    @property
    def headers(self) -> dict:
        return self._headers

    def __str__(self) -> str:
        return f"Response({self.status_string})"

    class ResponseBodyTypeNotSupportedException(Exception):
        pass
