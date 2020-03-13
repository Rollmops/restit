from marshmallow import Schema, ValidationError
from werkzeug.exceptions import UnprocessableEntity


class RequestBodyParameter:
    def __init__(self, schema: Schema, validation_error_class=UnprocessableEntity):
        self.schema = schema
        self.validation_error_class = validation_error_class

    def validate(self, request_body: dict) -> dict:
        try:
            return self.schema.load(request_body)
        except ValidationError as error:
            raise self.validation_error_class(
                f"Request body validation failed ({str(error)})"
            )
