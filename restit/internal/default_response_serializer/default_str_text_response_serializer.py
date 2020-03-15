from typing import List, Tuple

from restit.common import get_default_encoding
from restit.response_serializer import ResponseSerializer


class DefaultStrTextResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["text/plain"]

    def get_response_data_type(self) -> type:
        return str

    def serialize(self, response_input: str) -> Tuple[bytes, str]:
        return response_input.encode(encoding=get_default_encoding()), "text/plain"
