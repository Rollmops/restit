from typing import List, Tuple

from restit.common import get_default_encoding, guess_text_content_subtype
from restit.response_serializer import ResponseSerializer


class StringFallbackResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["*/*"]

    def get_response_data_type(self) -> type:
        return str

    def serialize(self, response_input: str) -> Tuple[bytes, str]:
        response_input_bytes = response_input.encode(encoding=get_default_encoding())
        return response_input_bytes, guess_text_content_subtype(response_input_bytes)
