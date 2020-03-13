from typing import List, Type

from restit.common import create_dict_from_query_parameter_syntax
from restit.request_deserializer import RequestDeserializer


class DefaultFormDataDictDeserializer(RequestDeserializer):
    def get_content_type_list(self) -> List[str]:
        return ["application/x-www-form-urlencoded", "multipart/form-data", "application/x-url-encoded"]

    def deserialize(self, request_input: bytes, encoding: str = None) -> dict:
        return create_dict_from_query_parameter_syntax(request_input, encoding)

    def get_deserialized_python_type(self) -> Type:
        return dict
