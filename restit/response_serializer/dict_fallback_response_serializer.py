import json
from typing import List

from restit.common import get_default_encoding
from restit.response_serializer import ResponseSerializer


class DictFallbackResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["*/*"]

    def get_response_data_type(self) -> type:
        return dict

    def get_content_type(self) -> str:
        return "application/json"

    def serialize(self, response_input: dict) -> bytes:
        json_string = json.dumps(response_input)
        return json_string.encode(encoding=get_default_encoding())
