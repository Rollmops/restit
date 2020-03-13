from typing import Type, Union, List

from restit.request_deserializer import RequestDeserializer


class DefaultAnyBytesDeserializer(RequestDeserializer):
    def get_deserialized_python_type(self) -> Type:
        return bytes

    def get_content_type_list(self) -> Union[List[str], None]:
        return None

    def deserialize(self, request_input: bytes, encoding: str = None) -> bytes:
        return request_input
