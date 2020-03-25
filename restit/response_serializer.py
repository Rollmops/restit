from typing import Any, List, Tuple, Union, NamedTuple

from marshmallow import Schema
from marshmallow.fields import Field

from restit.internal.http_accept import HttpAccept
from restit.internal.mime_type import MIMEType
from restit.internal.response_status_parameter import ResponseStatusParameter


class CanHandleResultType(NamedTuple):
    content_type: str
    mime_type: MIMEType


class ResponseSerializer:
    def can_handle_incoming_media_type(self, http_accept: HttpAccept) -> Union[None, CanHandleResultType]:
        best_match = http_accept.get_best_match(self.get_media_type_strings())
        if best_match is not None:
            return CanHandleResultType(best_match[0], best_match[1])

    def get_media_type_strings(self) -> List[str]:
        raise NotImplementedError()

    def get_response_data_type(self) -> type:
        raise NotImplementedError()

    def validate_and_serialize(
            self,
            response_input: Any,
            response_status_parameter: Union[None, ResponseStatusParameter],
            can_handle_result: CanHandleResultType
    ) -> Tuple[bytes, str]:
        """Returns a tuple of the serialized bytes and the content type"""
        raise NotImplementedError()

    @staticmethod
    def find_schema(
            content_type: str, response_status_parameter: Union[None, ResponseStatusParameter]
    ) -> Union[None, Schema, Field]:
        if response_status_parameter is not None:
            try:
                return response_status_parameter.content_types[content_type]
            except KeyError:
                raise ResponseSerializer.ContentTypeNotExpectedForResponseStatusException(content_type)

    class ContentTypeNotExpectedForResponseStatusException(Exception):
        pass

    class ResponseBodyValidationFailedException(Exception):
        pass
