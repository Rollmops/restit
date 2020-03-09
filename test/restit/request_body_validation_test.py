import requests
from marshmallow import Schema, fields

from restit.expect_request_body_decorator import expect_request_body
from restit.request import Request
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response
from test.base_test_server_test_case import BaseTestServerTestCase


class RequestBodySchema(Schema):
    param1 = fields.Int(required=True)
    param2 = fields.Str(required=True)


@request_mapping("/miau")
class QueryParametersResource(Resource):
    @expect_request_body(schema=RequestBodySchema())
    def post(self, request: Request) -> Response:
        return Response(request.body_as_json)


class RequestBodyValidationTestCase(BaseTestServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseTestServerTestCase.resources = [
            QueryParametersResource()
        ]
        BaseTestServerTestCase.setUpClass()

    def test_request_body_validation(self):
        response = requests.post(f"http://127.0.0.1:{self.port}/miau", data={"param1": "1", "param2": "huhu"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({'param1': 1, 'param2': 'huhu'}, response.json())

    def test_request_body_validation_fails(self):
        response = requests.post(f"http://127.0.0.1:{self.port}/miau", data={"param1": "hans", "param2": 222})
        self.assertEqual(422, response.status_code)
        self.assertEqual(
            "Request body validation failed ({'param1': ['Not a valid integer.']})", response.text
        )
