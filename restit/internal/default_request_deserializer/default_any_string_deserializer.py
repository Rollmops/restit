from typing import Type, Union, List

from restit.common import get_default_encoding
from restit.request_deserializer import RequestDeserializer


class DefaultAnyStringDeserializer(RequestDeserializer):
    def get_deserialized_python_type(self) -> Type:
        return str

    def get_content_type_list(self) -> Union[List[str], None]:
        return None

    def deserialize(self, request_input: bytes, encoding: str = None) -> str:
        return request_input.decode(encoding or get_default_encoding())
