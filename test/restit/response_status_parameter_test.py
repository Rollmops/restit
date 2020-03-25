import logging
import unittest

from marshmallow import Schema, fields

from restit import Resource, Request, Response, RestItTestApp
from restit.decorator import path, response
from restit.rfc7807_schema import RFC7807Schema


class MySchema(Schema):
    field1 = fields.String()
    field2 = fields.Integer()


@path("/")
class MyResource(Resource):
    @response(200, {"application/json": MySchema()}, "Everything is ok")
    @response(404, {"application/json": RFC7807Schema()}, "Something was not found")
    def get(self, request: Request, **path_params) -> Response:
        request_body = request.deserialized_body
        return Response({"field1": "Hans", "field2": "10"}, status_code=request_body["status"])

    def post(self, request: Request) -> Response:
        return Response({}, 204)


class ResponseStatusParameterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.restit_test_app = RestItTestApp(resources=[MyResource()])

    def test_status_supported(self):
        r = self.restit_test_app.get("/", json={"status": 200})
        self.assertEqual(200, r.status_code)
        self.assertEqual({'field1': 'Hans', 'field2': 10}, r.json())

    def test_status_unsupported(self):
        with self.assertLogs(level=logging.WARNING) as logs:
            r = self.restit_test_app.get("/", json={"status": 201})
            self.assertEqual(201, r.status_code)

            self.assertIn("WARNING:restit.resource:Response status code 201 is not expected for ", logs.output[0])

    def test_no_status_unsupported_if_no_decorator(self):
        with self.assertRaises(AssertionError):
            with self.assertLogs(level=logging.WARNING):
                self.restit_test_app.post("/")
