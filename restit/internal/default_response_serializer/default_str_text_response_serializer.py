from typing import List, Tuple, Union

from restit.common import guess_text_content_subtype_string
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.internal.schema_or_field_deserializer import SchemaOrFieldDeserializer
from restit.response_serializer import ResponseSerializer, CanHandleResultType


class DefaultStrTextResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["text/*"]

    def get_response_data_type(self) -> type:
        return str

    def validate_and_serialize(
            self, response_input: str,
            response_status_parameter: Union[None, ResponseStatusParameter],
            can_handle_result: CanHandleResultType
    ) -> Tuple[bytes, str]:
        content_type = guess_text_content_subtype_string(response_input)
        schema_or_field = self.find_schema(content_type, response_status_parameter)
        if schema_or_field:
            response_input = str(SchemaOrFieldDeserializer.deserialize(response_input, schema_or_field))

        return response_input.encode(encoding=can_handle_result.mime_type.charset), content_type

    class SchemaNotSupportedForStringResponseBody(Exception):
        pass
