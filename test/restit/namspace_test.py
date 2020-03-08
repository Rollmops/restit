import unittest

import requests

from restit.namespace import Namespace
from restit.request import Request
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response
from restit.restit_app import RestitApp
from test.helper import start_server_with_wsgi_app


@request_mapping("/subpath")
class MyResource(Resource):

    def get(self, request: Request) -> Response:
        return Response("Hallo")


class NamespaceTestCase(unittest.TestCase):
    def test_something(self):
        namespace = Namespace("/huhu", resources=[MyResource()])

        restit_app = RestitApp(namespaces=[namespace])

        with start_server_with_wsgi_app(restit_app) as port:
            response = requests.get(f"http://127.0.0.1:{port}/huhu/subpath")
            self.assertEqual(200, response.status_code)
            self.assertEqual("Hallo", response.text)
