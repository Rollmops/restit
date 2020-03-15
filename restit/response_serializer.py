from typing import Any, List, Tuple

from restit.internal.http_accept import HttpAccept


class ResponseSerializer:
    def __init__(self):
        self.priority = 0

    def can_handle_incoming_media_type(self, http_accept: HttpAccept) -> bool:
        best_match = http_accept.get_best_match(self.get_media_type_strings())
        if best_match is not None:
            self.priority = best_match[1].quality
            return True
        return False

    def get_media_type_strings(self) -> List[str]:
        raise NotImplemented()

    def get_response_data_type(self) -> type:
        raise NotImplemented()

    def serialize(self, response_input: Any) -> Tuple[bytes, str]:
        """Returns a tuple of the serialized bytes and the content type"""
        raise NotImplemented()
