from typing import Any, List

from werkzeug.datastructures import MIMEAccept


class ResponseSerializer:
    def __init__(self):
        self.priority = 0

    def can_handle_incoming_media_type(self, media_type: MIMEAccept) -> bool:
        best_match = media_type.best_match(self.get_media_type_strings())
        if best_match is not None:
            self.priority = media_type[media_type.find(best_match)][0]
            return True
        return False

    def get_media_type_strings(self) -> List[str]:
        raise NotImplemented()

    def get_response_data_type(self) -> type:
        raise NotImplemented()

    def serialize(self, response_input: Any) -> bytes:
        raise NotImplemented()

    def get_content_type(self) -> str:
        raise NotImplemented()
