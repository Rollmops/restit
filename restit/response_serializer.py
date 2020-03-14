from typing import Any, List, Union

from restit.internal.http_accept import HttpAccept
from restit.internal.mime_type import MIMEType


class ResponseSerializer:
    def __init__(self):
        self.priority = 0
        self.best_match_mime_type: Union[MIMEType, None] = None

    def can_handle_incoming_media_type(self, http_accept: HttpAccept) -> bool:
        best_match = http_accept.get_best_match(self.get_media_type_strings())
        if best_match is not None:
            self.best_match_mime_type = best_match[1]
            self.priority = self.best_match_mime_type.quality
            return True
        return False

    def get_media_type_strings(self) -> List[str]:
        raise NotImplemented()

    def get_response_data_type(self) -> type:
        raise NotImplemented()

    def serialize(self, response_input: Any) -> bytes:
        raise NotImplemented()

    def get_content_type(self) -> str:
        return self.best_match_mime_type.to_string(with_details=False)
