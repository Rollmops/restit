from typing import Any, List


class ResponseSerializer:
    def is_responsible_for_media_type(self, media_types: List[str]) -> bool:
        raise NotImplemented()

    def is_responsible_for_response_data_type(self, response_data_type: type) -> bool:
        raise NotImplemented()

    def serialize(self, response_input: Any) -> bytes:
        raise NotImplemented()

    def get_content_type(self) -> str:
        raise NotImplemented()
