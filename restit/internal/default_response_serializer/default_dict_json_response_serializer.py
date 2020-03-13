import json
from typing import List

from restit.common import get_default_encoding
from restit.response_serializer import ResponseSerializer


class DefaultDictJsonResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["application/json", "application/problem+json"]

    def get_response_data_type(self) -> type:
        return dict

    def serialize(self, response_input: dict) -> bytes:
        return json.dumps(response_input).encode(encoding=get_default_encoding())