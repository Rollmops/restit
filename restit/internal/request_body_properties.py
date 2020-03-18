from typing import Dict, Union, Type

from marshmallow import Schema
from marshmallow.fields import Field

from restit.exception import UnprocessableEntity, UnsupportedMediaType
from restit.internal.mime_type import MIMEType


class RequestBodyProperties:
    def __init__(
            self,
            content_types: Dict[str, Union[Schema, Field]],
            description: str,
            required: bool, validation_error_class=UnprocessableEntity
    ):
        self.content_types = content_types
        self.description = description
        self.required = required
        self.validation_error_class = validation_error_class
        self._check_request_properties_schema_type()

    def get_schema_for_content_type(self, content_type: MIMEType) -> Union[Schema, Type]:
        try:
            return self.content_types[content_type.to_string()]
        except KeyError:
            raise UnsupportedMediaType()

    def _check_request_properties_schema_type(self):
        for schema_or_field in self.content_types.values():
            if not isinstance(schema_or_field, (Field, Schema)):
                raise RequestBodyProperties.UnsupportedSchemaTypeException(type(schema_or_field))

    class UnsupportedSchemaTypeException(Exception):
        pass
