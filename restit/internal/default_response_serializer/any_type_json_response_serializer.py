import json
from typing import List, Union, Tuple, Any

from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.response_serializer import ResponseSerializer, CanHandleResultType


class AnyTypeJsonResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["application/json", "application/problem+json"]

    def get_response_data_type(self) -> type:
        return object

    def validate_and_serialize(
            self,
            response_input: object,
            response_status_parameter: Union[None, ResponseStatusParameter],
            can_handle_result: CanHandleResultType
    ) -> Tuple[bytes, str]:
        if self._is_primitive(response_input):
            raise AnyTypeJsonResponseSerializer.PrimitiveTypeNotSupportedForJsonResponse(response_input)

        content_type = "application/json"
        schema = ResponseSerializer.find_schema(content_type, response_status_parameter)
        if schema:
            json_string = schema.dumps(response_input)
        else:
            json_string = json.dumps(dir(response_input))
        return json_string.encode(encoding=can_handle_result.mime_type.charset), content_type

    @staticmethod
    def _is_primitive(value: Any) -> bool:
        return not hasattr(value, "__dict__")

    class PrimitiveTypeNotSupportedForJsonResponse(Exception):
        pass
