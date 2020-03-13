import json
from typing import List, Type

from restit.common import get_default_encoding
from restit.request_deserializer import RequestDeserializer


class DefaultApplicationJsonDictDeserializer(RequestDeserializer):
    def get_content_type_list(self) -> List[str]:
        return ["application/json", "application/problem+json"]

    def deserialize(self, request_input: bytes, encoding: str = None) -> dict:
        return json.loads(request_input.decode(encoding or get_default_encoding()))

    def get_deserialized_python_type(self) -> Type:
        return dict
