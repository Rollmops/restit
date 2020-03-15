from typing import List, Tuple

from restit.common import guess_text_content_subtype
from restit.response_serializer import ResponseSerializer


class DefaultBytesTextResponseSerializer(ResponseSerializer):

    def get_media_type_strings(self) -> List[str]:
        return ["text/*"]

    def get_response_data_type(self) -> type:
        return bytes

    def serialize(self, response_input: bytes) -> Tuple[bytes, str]:
        return response_input, guess_text_content_subtype(response_input)
