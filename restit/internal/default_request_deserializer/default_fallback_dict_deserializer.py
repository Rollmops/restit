import json
import logging
from typing import List, Type

from restit.request_deserializer import RequestDeserializer

LOGGER = logging.getLogger(__name__)


class DefaultFallbackDictDeserializer(RequestDeserializer):
    def get_content_type_list(self) -> List[str]:
        return ["*/*"]

    def deserialize(self, request_input: bytes, encoding: str = None) -> dict:
        LOGGER.warning("Trying to parse JSON from content type != application/json")
        if len(request_input) == 0:
            return {}
        response_as_dict = json.loads(request_input.decode(encoding))
        return response_as_dict

    def get_deserialized_python_type(self) -> Type:
        return dict
