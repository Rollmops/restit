import json
from http import HTTPStatus
from typing import Union

from werkzeug.datastructures import MIMEAccept
from werkzeug.exceptions import NotAcceptable

from restit import _DEFAULT_ENCODING


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
        self.encoding = encoding or _DEFAULT_ENCODING
        self.body_as_bytes = b""

    def set_body_as_bytes(self, accept: MIMEAccept):
        if isinstance(self.response_body, dict):
            response_body_string = self._get_response_as_json(accept)
        elif isinstance(self.response_body, str):
            response_body_string = self.response_body
        else:
            raise Response.ResponseBodyTypeNotSupportedException(type(self.response_body))

        self.body_as_bytes = response_body_string.encode(encoding=self.encoding)

    def _get_response_as_json(self, accept):
        if not accept.accept_json:
            raise NotAcceptable(
                f"Trying to send a JSON response, but JSON is not accepted by the client (accepted: {accept})"
            )
        response_body_string = json.dumps(self.response_body)
        return response_body_string

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
