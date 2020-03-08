from http import HTTPStatus
from typing import Union

import orjson

from restit import DEFAULT_ENCODING


class Response:
    def __init__(
            self,
            response_body: Union[str, dict],
            status_code: Union[int, HTTPStatus] = 200,
            header: dict = None, encoding=None
    ):
        self.response_body = response_body
        self.status_code = HTTPStatus(status_code, None)
        self.header = header or {}
        self.encoding = encoding or DEFAULT_ENCODING

    @staticmethod
    def from_http_status(http_status: HTTPStatus) -> "Response":
        return Response(
            response_body=http_status.description,
            status_code=http_status.value
        )

    def get_body_as_bytes(self) -> bytes:
        if isinstance(self.response_body, dict):
            response_body_as_string = orjson.dumps(self.response_body)
        elif isinstance(self.response_body, str):
            response_body_as_string = self.response_body
        else:
            raise Response.ResponseBodyTypeNotSupportedException(type(self.response_body))

        return response_body_as_string.encode(encoding=self.encoding)

    def adapt_header(self):
        if "Content-Type" not in self.header:
            self._adapt_content_type()

    def get_status(self) -> str:
        return f"{self.status_code.value} {self.status_code.name}"

    def _adapt_content_type(self):
        if isinstance(self.response_body, dict):
            self.header["Content-Type"] = f"application/json; charset={self.encoding}"
        elif isinstance(self.response_body, str):
            self.header["Content-Type"] = f"text/plain; charset={self.encoding}"
        else:
            Response.ResponseBodyTypeNotSupportedException(type(self.response_body))

    class ResponseBodyTypeNotSupportedException(Exception):
        pass
