from typing import List, Tuple, Union

from restit.common import guess_text_content_subtype_bytes, get_default_encoding
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.internal.type_converter.schema_or_field_deserializer import SchemaOrFieldDeserializer
from restit.response_serializer import ResponseSerializer


class DefaultBytesTextResponseSerializer(ResponseSerializer):

    def get_media_type_strings(self) -> List[str]:
        return ["text/*"]

    def get_response_data_type(self) -> type:
        return bytes

    def validate_and_serialize(
            self, response_input: bytes, response_status_parameter: Union[None, ResponseStatusParameter]
    ) -> Tuple[bytes, str]:
        content_type = guess_text_content_subtype_bytes(response_input)
        schema_or_field = self.find_schema(content_type, response_status_parameter)
        if schema_or_field:
            response_input = bytes(
                str(SchemaOrFieldDeserializer.deserialize(
                    response_input.decode(get_default_encoding()), schema_or_field
                )),
                encoding=get_default_encoding()
            )

        return response_input, content_type
