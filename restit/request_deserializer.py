from typing import Any, List, Type, Union

from restit.internal.mime_type import MIMEType


class RequestDeserializer:
    def get_content_type_list(self) -> Union[List[str], None]:
        raise NotImplementedError()

    def deserialize(self, request_input: bytes, encoding: str = None) -> Any:
        raise NotImplementedError()

    def get_deserialized_python_type(self) -> Type:
        raise NotImplementedError()

    def can_handle(self, content_type: MIMEType, python_type: Type) -> bool:
        if self.get_content_type_list() is None:
            return python_type == self.get_deserialized_python_type()

        for content_type_string in self.get_content_type_list():
            if content_type.matches_mime_type_string(content_type_string) and \
                    python_type == self.get_deserialized_python_type():
                return True
        return False
