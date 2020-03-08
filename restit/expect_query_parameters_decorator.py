from http import HTTPStatus

from marshmallow import Schema, ValidationError

from restit.request import Request
from restit.response import Response


def expect_query_parameters(schema: Schema, validation_error_status=HTTPStatus.UNPROCESSABLE_ENTITY):
    def decorator(func):
        def wrapper(self, request: Request, **path_parameters):
            try:
                request.query_parameters = schema.load(request.query_parameters)
            except ValidationError as error:
                return Response.from_http_status(
                    http_status=validation_error_status,
                    description="Query parameter validation failed",
                    additional_description=str(error)
                )
            else:
                return func(self, request, **path_parameters)

        return wrapper

    return decorator
