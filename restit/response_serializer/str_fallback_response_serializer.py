from typing import List

from restit.common import get_default_encoding
from restit.response_serializer import ResponseSerializer


class StringFallbackResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["*/*"]

    def get_response_data_type(self) -> type:
        return str

    def get_content_type(self) -> str:
        return "text/plain"

    def serialize(self, response_input: str) -> bytes:
        return response_input.encode(encoding=get_default_encoding())
