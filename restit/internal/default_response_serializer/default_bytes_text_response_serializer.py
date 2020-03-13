from typing import List

from restit.response_serializer import ResponseSerializer


class DefaultBytesTextResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["text/*"]

    def get_response_data_type(self) -> type:
        return bytes

    def serialize(self, response_input: bytes) -> bytes:
        return response_input
