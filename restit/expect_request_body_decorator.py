from marshmallow import Schema, ValidationError
from werkzeug.exceptions import UnprocessableEntity

from restit.request import Request


def expect_request_body(schema: Schema, validation_error_class=UnprocessableEntity):
    def decorator(func):
        def wrapper(self, request: Request, **path_parameters):
            try:
                request.body_as_dict = schema.load(request.body_as_dict)
            except ValidationError as error:
                raise validation_error_class(f"Request body validation failed ({str(error)})")
            else:
                return func(self, request, **path_parameters)

        return wrapper

    return decorator
