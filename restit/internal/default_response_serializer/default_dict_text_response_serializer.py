from typing import List, Tuple, Union

from restit.internal.default_response_serializer.default_dict_json_response_serializer import \
    DefaultDictJsonResponseSerializer
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.response_serializer import ResponseSerializer, CanHandleResultType


class DefaultDictTextResponseSerializer(ResponseSerializer):

    def get_media_type_strings(self) -> List[str]:
        return ["text/plain"]

    def get_response_data_type(self) -> type:
        return dict

    def validate_and_serialize(
            self,
            response_input: dict,
            response_status_parameter: Union[None, ResponseStatusParameter],
            can_handle_result: CanHandleResultType
    ) -> Tuple[bytes, str]:
        response_in_bytes, _ = DefaultDictJsonResponseSerializer().validate_and_serialize(
            response_input, response_status_parameter, can_handle_result
        )

        return response_in_bytes, "text/plain"


class DefaultListTextResponseSerializer(DefaultDictTextResponseSerializer):
    def get_response_data_type(self) -> type:
        return list
