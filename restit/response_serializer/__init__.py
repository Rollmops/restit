from typing import Any

from werkzeug.datastructures import MIMEAccept


class ResponseSerializer:
    def is_responsible_for_media_type(self, media_type: MIMEAccept) -> bool:
        raise NotImplemented()

    def is_responsible_for_response_data_type(self, response_data_type: type) -> bool:
        raise NotImplemented()

    def serialize(self, response_input: Any) -> bytes:
        raise NotImplemented()

    def get_content_type(self) -> str:
        raise NotImplemented()
