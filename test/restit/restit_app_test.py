import unittest
from http import HTTPStatus

import requests

from restit.request import Request
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response
from restit.restit_app import RestitApp
from test.helper import start_server_with_wsgi_app


class TestResource(Resource):
    __url__ = "/"

    def get(self, request: Request):
        return Response("Hallo")


class TestResource2(Resource):
    __url__ = "/miau"

    def get(self, request: Request) -> Response:
        return Response("wuff", 201)


@request_mapping("/miau/<id:int>")
class TestResourceWithPathParams(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response(path_params)


@request_mapping("/post")
class TestRequestBodyResource(Resource):
    def post(self, request: Request) -> Response:
        return Response({
            "query_parameters": request.query_parameters,
            "body": request.body.decode(),
            "body_as_json": request.body_as_json
        }, HTTPStatus.CREATED)


@request_mapping("/error")
class ErrorResource(Resource):
    def get(self, request: Request) -> Response:
        raise Exception()


class RestitAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.restit_app = RestitApp(resources=[
            TestResource(),
            TestResource2(),
            TestResourceWithPathParams(),
            TestRequestBodyResource(),
            ErrorResource()
        ])

    def test_simple_get_resource(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.get(f"http://127.0.0.1:{port}/")
            self.assertEqual(200, response.status_code)
            self.assertEqual("Hallo", response.text)

            response = requests.get(f"http://127.0.0.1:{port}/miau")
            self.assertEqual(201, response.status_code)
            self.assertEqual("wuff", response.text)

    def test_pass_request_body_as_json(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.post(
                f"http://127.0.0.1:{port}/post", json={"key": "value"}
            )
            self.assertEqual(201, response.status_code)
            self.assertEqual({
                'body': '{"key": "value"}',
                'body_as_json': {'key': 'value'},
                'query_parameters': {}
            }, response.json())

    def test_pass_request_body_as_form(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.post(
                f"http://127.0.0.1:{port}/post", data={"key": "value"}
            )
            self.assertEqual(201, response.status_code)
            self.assertEqual({
                'body': 'key=value', 'body_as_json': {'key': 'value'}, 'query_parameters': {}
            }, response.json())

    def test_method_not_allowed_405(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.delete(f"http://127.0.0.1:{port}/")
            self.assertEqual(405, response.status_code)
            self.assertEqual("Specified method is invalid for this resource", response.text)

    def test_url_not_found(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.get(f"http://127.0.0.1:{port}/NOT_THERE")
            self.assertEqual(404, response.status_code)

    def test_resource_with_path_params(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.get(f"http://127.0.0.1:{port}/miau/21")
            self.assertEqual(200, response.status_code)
            self.assertEqual({"id": 21}, response.json())

    def test_internal_server_error(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.get(f"http://127.0.0.1:{port}/error")
            self.assertEqual(500, response.status_code)
