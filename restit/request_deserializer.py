from typing import Any, List, Type, Union


class RequestDeserializer:
    def get_content_type_list(self) -> Union[List[str], None]:
        raise NotImplemented()

    def deserialize(self, request_input: bytes, encoding: str = None) -> Any:
        raise NotImplemented()

    def get_deserialized_python_type(self) -> Type:
        raise NotImplemented()

    def can_handle_content_type(self, content_type: str) -> bool:
        return self.get_content_type_list() is None or content_type in self.get_content_type_list()
