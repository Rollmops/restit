from typing import List, Tuple, Union

from restit.common import guess_text_content_subtype_string
from restit.internal.default_response_serializer.default_str_text_response_serializer import \
    DefaultStrTextResponseSerializer
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.response_serializer import ResponseSerializer, CanHandleResultType


class StringFallbackResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["*/*"]

    def get_response_data_type(self) -> type:
        return str

    def validate_and_serialize(
            self,
            response_input: str,
            response_status_parameter: Union[None, ResponseStatusParameter],
            can_handle_result: CanHandleResultType
    ) -> Tuple[bytes, str]:
        content_type = guess_text_content_subtype_string(response_input)
        response_input_bytes = response_input.encode(encoding=can_handle_result.mime_type.charset)
        if self.find_schema(content_type, response_status_parameter):
            raise DefaultStrTextResponseSerializer.SchemaNotSupportedForStringResponseBody()

        return response_input_bytes, content_type
