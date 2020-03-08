import unittest

import requests

from restit.request import Request
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


class RestitAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.restit_app = RestitApp(resources=[
            TestResource(),
            TestResource2()
        ])

    def test_simple_get_resource(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.get(f"http://127.0.0.1:{port}/")
            self.assertEqual(200, response.status_code)
            self.assertEqual("Hallo", response.text)

            response = requests.get(f"http://127.0.0.1:{port}/miau")
            self.assertEqual(201, response.status_code)
            self.assertEqual("wuff", response.text)

    def test_method_not_allowed_405(self):
        with start_server_with_wsgi_app(self.restit_app) as port:
            response = requests.delete(f"http://127.0.0.1:{port}/")
            self.assertEqual(405, response.status_code)
            self.assertEqual("Specified method is invalid for this resource", response.text)
