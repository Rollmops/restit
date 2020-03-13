from typing import Dict

from marshmallow import Schema, ValidationError
from werkzeug.exceptions import UnprocessableEntity, UnsupportedMediaType

from restit.request import Request


class RequestBodyParameter:
    def __init__(
            self,
            content_type_schemas: Dict[str, Schema],
            description: str,
            required: bool, validation_error_class=UnprocessableEntity
    ):
        self.content_types = content_type_schemas
        self.description = description
        self.required = required
        self.validation_error_class = validation_error_class

    def validate(self, request: Request) -> dict:
        schema = self._find_schema_for_content_type(request)
        try:
            return schema.load(request.get_body_as_dict())
        except ValidationError as error:
            raise self.validation_error_class(
                f"Request body validation failed ({str(error)})"
            )

    def _find_schema_for_content_type(self, request: Request) -> Schema:
        try:
            return self.content_types[request.get_extended_request_info().content_type]
        except KeyError:
            raise UnsupportedMediaType()
