import json
from typing import List, Type

from restit.request_deserializer import RequestDeserializer


class DefaultApplicationJsonDictDeserializer(RequestDeserializer):
    def get_content_type_list(self) -> List[str]:
        return ["application/json", "application/problem+json"]

    def deserialize(self, request_input: bytes, encoding: str = None) -> dict:
        if len(request_input) == 0:
            return {}

        return json.loads(request_input.decode(encoding))

    def get_deserialized_python_type(self) -> Type:
        return dict
