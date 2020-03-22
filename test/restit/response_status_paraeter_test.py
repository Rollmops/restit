import logging
import unittest

from marshmallow import Schema, fields

from restit import Resource, Request, Response, RestitTestApp, RestitApp, request_mapping
from restit.response_status_decorator import response_status


class MySchema(Schema):
    field1 = fields.String()
    field2 = fields.Integer()


@request_mapping("/")
class MyResource(Resource):

    @response_status(200, {"application/json": MySchema()}, "Everything is ok")
    def get(self, request: Request, **path_params) -> Response:
        request_body = request.typed_body[dict]
        return Response({"field1": "Hans", "field2": "10"}, status_code=request_body["status"])


class ResponseStatusParameterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.restit_test_app = RestitTestApp(RestitApp(resources=[MyResource()]))

    def test_status_supported(self):
        response = self.restit_test_app.get("/", json={"status": 200})
        self.assertEqual(200, response.status_code)
        self.assertEqual({'field1': 'Hans', 'field2': 10}, response.json())

    def test_status_unsupported(self):
        with self.assertLogs(level=logging.WARNING) as logs:
            response = self.restit_test_app.get("/", json={"status": 201})
            self.assertEqual(201, response.status_code)

            self.assertIn("WARNING:restit.resource:Response status code 201 is not expected for ", logs.output[0])
