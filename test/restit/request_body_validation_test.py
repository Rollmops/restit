import requests
from marshmallow import Schema, fields, post_load

from restit._response import Response
from restit.decorator import path, request_body
from restit.internal.request_body_properties import RequestBodyProperties
from restit.request import Request
from restit.resource import Resource
from test.base_test_server_test_case import BaseTestServerTestCase


class SchemaClass:
    def __init__(self, param1: int, param2: str):
        self.param1 = param1
        self.param2 = param2


class RequestBodySchema(Schema):
    param1 = fields.Int(required=True)
    param2 = fields.Str(required=True)


class RequestBodyObjectSchema(Schema):
    param1 = fields.Int(required=True)
    param2 = fields.Str(required=True)

    @post_load
    def create_object(self, data, **kwargs) -> SchemaClass:
        return SchemaClass(**data)


@path("/miau")
class QueryParametersResource(Resource):
    @request_body({"application/x-www-form-urlencoded": RequestBodySchema()}, description="Huhu")
    def post(self, request: Request) -> Response:
        return Response(request.deserialized_body)


@path("/request-with-object")
class RequestWithObjectResource(Resource):
    @request_body({"application/json": RequestBodyObjectSchema()}, "")
    def post(self, request: Request) -> Response:
        schema_object: SchemaClass = request.deserialized_body
        return Response(
            {
                "param1": schema_object.param1,
                "param2": schema_object.param2
            }
        )


class RequestBodyValidationTestCase(BaseTestServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseTestServerTestCase.resources = [
            QueryParametersResource(),
            RequestWithObjectResource()
        ]
        BaseTestServerTestCase.setUpClass()

    def test_request_body_validation(self):
        response = requests.post(f"http://127.0.0.1:{self.port}/miau", data={"param1": "1", "param2": "huhu"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({'param1': 1, 'param2': 'huhu'}, response.json())

    def test_request_body_validation_fails(self):
        response = requests.post(f"http://127.0.0.1:{self.port}/miau", data={"param1": "hans", "param2": 222})
        self.assertEqual(422, response.status_code)
        self.assertIn("<title>422 Unprocessable Entity</title>", response.text)
        self.assertIn("<h1>Unprocessable Entity</h1>", response.text)
        self.assertIn("Request body schema deserialization failed ({'param1': ['Not a valid integer.']})",
                      response.text)

    def test_request_body_schema_type_not_supported(self):
        with self.assertRaises(RequestBodyProperties.UnsupportedSchemaTypeException):
            # noinspection PyTypeChecker
            RequestBodyProperties({"text/plain": str}, "", True)

    def test_unsupported_media_type(self):
        response = requests.post(f"http://127.0.0.1:{self.port}/miau", json={"param1": "hans", "param2": 222})
        self.assertEqual(415, response.status_code)

    def test_request_body_object(self):
        response = requests.post(
            f"http://127.0.0.1:{self.port}/request-with-object", json={"param1": "312", "param2": "hans"}
        )
        self.assertEqual(200, response.status_code)
