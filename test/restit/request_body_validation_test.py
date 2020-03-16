import requests
from marshmallow import Schema, fields

from restit import RestitTestApp, RestitApp
from restit.request import Request
from restit.request_body_decorator import request_body
from restit.request_mapping_decorator import request_mapping
from restit.resource import Resource
from restit.response import Response
from test.base_test_server_test_case import BaseTestServerTestCase


class RequestBodySchema(Schema):
    param1 = fields.Int(required=True)
    param2 = fields.Str(required=True)


@request_mapping("/miau")
class QueryParametersResource(Resource):
    @request_body({"application/x-www-form-urlencoded": RequestBodySchema()}, description="Huhu")
    def post(self, request: Request) -> Response:
        return Response(request.get_request_body_as_type(dict))


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
            "<title>422 Unprocessable Entity</title>\n"
            "<h1>Unprocessable Entity</h1>\n"
            "<p>Request body schema deserialization failed ({'param1': ['Not a valid integer.']})</p>\n", response.text
        )

    def test_request_body_schema_type_not_supported(self):
        @request_mapping("/dummy")
        class DummyResource(Resource):

            @request_body({"text/plain": str}, description="Not supported type")
            def get(self, request: Request, **path_params) -> Response:
                return Response("")

        restit_test_app = RestitTestApp(RestitApp(resources=[DummyResource()]))
        response = restit_test_app.get("/dummy", data="plain string")
        self.assertEqual(200, response.get_status_code())
