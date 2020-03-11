import unittest

import requests

from restit.development_server import DevelopmentServer
from restit.request import Request
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response
from restit.restit_app import RestitApp


@request_mapping("/")
class MyResource(Resource):
    def get(self, request: Request) -> Response:
        return Response("Hello")


class DevelopmentServerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.restit_app = RestitApp(resources=[MyResource()])
        self.development_server = DevelopmentServer(self.restit_app)

    def test_start_in_context(self):
        with self.development_server.start_in_context() as port:
            response = requests.get(f"http://127.0.0.1:{port}/")
            self.assertEqual(200, response.status_code)
            self.assertEqual("Hello", response.text)

    def test_restit_app_in_context(self):
        with self.restit_app.start_development_server_in_context(port=0) as port:
            response = requests.get(f"http://127.0.0.1:{port}/")
            self.assertEqual(200, response.status_code)
            self.assertEqual("Hello", response.text)