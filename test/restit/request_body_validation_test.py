import unittest

import requests
from marshmallow import Schema, fields

from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.restit_app import RestitApp
from test.helper import start_server_with_wsgi_app


class RequestBodySchema(Schema):
    param1 = fields.Int(required=True)
    param2 = fields.Str(required=True)


from http import HTTPStatus

from marshmallow import Schema, ValidationError

from restit.request import Request
from restit.response import Response


def expect_request_body(schema: Schema, validation_error_status=HTTPStatus.UNPROCESSABLE_ENTITY):
    def decorator(func):
        def wrapper(self, request: Request, **path_parameters):
            try:
                request.body_as_json = schema.load(request.body_as_json)
            except ValidationError as error:
                return Response.from_http_status(
                    http_status=validation_error_status,
                    description="Request body validation failed",
                    additional_description=str(error)
                )
            else:
                return func(self, request, **path_parameters)

        return wrapper

    return decorator


@request_mapping("/miau")
class QueryParametersResource(Resource):
    @expect_request_body(schema=RequestBodySchema())
    def post(self, request: Request) -> Response:
        return Response(request.body_as_json)


class RequestBodyValidationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.restit_app = RestitApp(resources=[
            QueryParametersResource()
        ])

    def test_request_body_validation(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.post(f"http://127.0.0.1:{port}/miau", data={"param1": "1", "param2": "huhu"})
            self.assertEqual(200, response.status_code)
            self.assertEqual({'param1': 1, 'param2': 'huhu'}, response.json())
