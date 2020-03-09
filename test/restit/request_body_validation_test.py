import unittest

import requests
from marshmallow import Schema, fields

from restit.expect_request_body_decorator import expect_request_body
from restit.request import Request
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response
from restit.restit_app import RestitApp
from test.helper import start_server_with_wsgi_app


class RequestBodySchema(Schema):
    param1 = fields.Int(required=True)
    param2 = fields.Str(required=True)


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