import unittest

import requests

from restit._response import Response
from restit.decorator import path
from restit.namespace import Namespace
from restit.request import Request
from restit.resource import Resource
from restit.restit_app import RestItApp
from test.start_server_with_wsgi_app import start_server_with_wsgi_app


@path("/subpath")
class MyResource(Resource):
    def get(self, request: Request) -> Response:
        return Response("Hallo")


@path("/subpath2")
class MyResource2(Resource):
    def get(self, request: Request) -> Response:
        return Response("Hallo from subpath 2")


class NamespaceTestCase(unittest.TestCase):
    def test_something(self):
        namespace = Namespace("/huhu", resources=[MyResource()])
        namespace.register_resources([MyResource2()])

        restit_app = RestItApp(namespaces=[namespace])

        with start_server_with_wsgi_app(restit_app) as port:
            response = requests.get(f"http://127.0.0.1:{port}/huhu/subpath")
            self.assertEqual(200, response.status_code)
            self.assertEqual("Hallo", response.text)
            response = requests.get(f"http://127.0.0.1:{port}/huhu/subpath2")
            self.assertEqual(200, response.status_code)
            self.assertEqual("Hallo from subpath 2", response.text)
