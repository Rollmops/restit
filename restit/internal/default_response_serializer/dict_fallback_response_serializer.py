from typing import List, Tuple, Union

from restit.internal.default_response_serializer.default_dict_json_response_serializer import \
    DefaultDictJsonResponseSerializer
from restit.internal.mime_type import MIMEType
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.response_serializer import ResponseSerializer


class DictFallbackResponseSerializer(ResponseSerializer):
    def get_media_type_strings(self) -> List[str]:
        return ["*/*"]

    def get_response_data_type(self) -> type:
        return dict

    def validate_and_serialize(
            self,
            response_input: dict,
            response_status_parameter: Union[None, ResponseStatusParameter],
            can_handle_result: MIMEType
    ) -> Tuple[bytes, str]:
        response_in_bytes, _ = DefaultDictJsonResponseSerializer().validate_and_serialize(
            response_input, response_status_parameter, can_handle_result
        )

        return response_in_bytes, "application/json"
