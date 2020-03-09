import requests
from marshmallow import Schema, fields

from restit.expect_query_parameters_decorator import expect_query_parameters
from restit.request import Request
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response
from test.base_test_server_test_case import BaseTestServerTestCase


class QueryParameterSchema(Schema):
    param1 = fields.Int(required=True)
    param2 = fields.Str(required=True)


@request_mapping("/queryparams")
class QueryParametersResource(Resource):
    @expect_query_parameters(schema=QueryParameterSchema())
    def get(self, request: Request) -> Response:
        return Response(request.query_parameters)


class QueryParameterDecoratorTestCase(BaseTestServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseTestServerTestCase.resources = [
            QueryParametersResource()
        ]
        BaseTestServerTestCase.setUpClass()

    def test_query_parameter(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/queryparams?param1=1&param2=huhu")
        self.assertEqual(200, response.status_code)
        self.assertEqual({'param1': 1, 'param2': 'huhu'}, response.json())

    def test_validation_error_gives_422_status(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/queryparams?param1=1&")
        self.assertEqual(422, response.status_code)
        self.assertEqual(
            "Query parameter validation failed ({'param2': ['Missing data for required field.']})",
            response.text
        )
