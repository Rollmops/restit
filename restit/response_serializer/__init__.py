from typing import Any, List

from werkzeug.datastructures import MIMEAccept


class ResponseSerializer:
    def __init__(self):
        self.priority = 0
        self.best_match_media_type = None

    def can_handle_incoming_media_type(self, media_type: MIMEAccept) -> bool:
        self.best_match_media_type = media_type.best_match(self.get_media_type_strings())
        if self.best_match_media_type is not None:
            self.priority = media_type[media_type.find(self.best_match_media_type)][0]
            return True
        return False

    def get_media_type_strings(self) -> List[str]:
        raise NotImplemented()

    def get_response_data_type(self) -> type:
        raise NotImplemented()

    def serialize(self, response_input: Any) -> bytes:
        raise NotImplemented()

    def get_content_type(self) -> str:
        return self.best_match_media_type
