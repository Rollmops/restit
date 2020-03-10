from marshmallow import Schema, ValidationError
from werkzeug import Request
from werkzeug.exceptions import UnprocessableEntity


def expect_query_parameters(schema: Schema, validation_error_class=UnprocessableEntity):
    def decorator(func):
        def wrapper(self, request: Request, **path_parameters):
            try:
                request.query_parameters = schema.load(request.query_parameters)
            except ValidationError as error:
                raise validation_error_class(f"Query parameter validation failed ({str(error)})")
            else:
                return func(self, request, **path_parameters)

        return wrapper

    return decorator
