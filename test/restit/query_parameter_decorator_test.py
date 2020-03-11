import unittest

from marshmallow import Schema, fields
from werkzeug import Request
from werkzeug.exceptions import BadRequest

from restit import RestitApp, RestitTestApp
from restit.query_parameters_decorator import query_parameters
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response


class QueryParameterSchema(Schema):
    param1 = fields.Int(required=True)
    param2 = fields.Str(required=True)


@request_mapping("/queryparams")
class QueryParametersResource(Resource):
    @query_parameters(schema=QueryParameterSchema())
    def get(self, request: Request) -> Response:
        return Response(request.query_parameters)


@request_mapping("/custom-error-class")
class CustomErrorClassResource(Resource):
    @query_parameters(schema=QueryParameterSchema(), validation_error_class=BadRequest)
    def get(self, request: Request) -> Response:
        return Response(request.query_parameters)


class QueryParameterDecoratorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        restit_app = RestitApp(resources=[
            QueryParametersResource(),
            CustomErrorClassResource()
        ])
        self.restit_test_app = RestitTestApp(restit_app)

    def test_query_parameter(self):
        response = self.restit_test_app.get("/queryparams?param1=1&param2=huhu")
        self.assertEqual(200, response.get_status_code())
        self.assertEqual({'param1': 1, 'param2': 'huhu'}, response.json())

    def test_validation_error_gives_422_status(self):
        response = self.restit_test_app.get(f"/queryparams?param1=1&")
        self.assertEqual(422, response.get_status_code())
        self.assertEqual(
            "<title>422 Unprocessable Entity</title>\n"
            "<h1>Unprocessable Entity</h1>\n"
            "<p>Query parameter validation failed ({'param2': ['Missing data for required field.']})</p>\n",
            response.text
        )

    def test_validation_error_custom_error_class(self):
        response = self.restit_test_app.get(f"/custom-error-class?param1=1&")
        self.assertEqual(400, response.get_status_code())
        self.assertEqual(
            "<title>400 Bad Request</title>\n"
            "<h1>Bad Request</h1>\n"
            "<p>Query parameter validation failed ({'param2': ['Missing data for required field.']})</p>\n",
            response.text
        )
