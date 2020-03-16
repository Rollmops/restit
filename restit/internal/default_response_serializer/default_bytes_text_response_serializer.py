from typing import List, Tuple, Union

from restit.common import guess_text_content_subtype_bytes
from restit.internal.default_response_serializer.default_str_text_response_serializer import \
    DefaultStrTextResponseSerializer
from restit.internal.response_status_parameter import ResponseStatusParameter
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
        if self.find_schema(content_type, response_status_parameter):
            raise DefaultStrTextResponseSerializer.SchemaNotSupportedForStringResponseBody()

        return response_input, content_type
