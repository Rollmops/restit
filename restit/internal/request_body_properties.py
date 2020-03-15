from typing import Dict, Union, Type

from marshmallow import Schema, ValidationError
from werkzeug.exceptions import UnprocessableEntity, UnsupportedMediaType

from restit.request import Request


class RequestBodyProperties:
    def __init__(
            self,
            content_types: Dict[str, Union[Schema, Type]],
            description: str,
            required: bool, validation_error_class=UnprocessableEntity
    ):
        self.content_types = content_types
        self.description = description
        self.required = required
        self.validation_error_class = validation_error_class

    def get_schema_for_content_type(self, content_type: str) -> Union[Schema, Type]:
        try:
            return self.content_types[content_type]
        except KeyError:
            raise UnsupportedMediaType()

    def validate(self, request: Request) -> str:
        schema_or_type = self.get_schema_for_content_type(request.get_content_type())
        try:
            body_as_dict = request.get_request_body_as_type(dict)
            return schema_or_type.dumps(body_as_dict)
        except (ValidationError, ValueError) as error:
            raise self.validation_error_class(
                f"Request body validation failed ({str(error)})"
            )
