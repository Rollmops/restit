import unittest

import requests

from restit.request import Request
from restit.resource import Resource
from restit.resource_mapping import ResourceMapping
from restit.response import Response
from restit.restit_app import RestitApp
from test.helper import start_server_with_wsgi_app


class TestResource(Resource):

    def get(self, request: Request):
        return Response("Hallo")


class RestitAppTestCase(unittest.TestCase):
    def test_simple_get_resource(self):
        restit_app = RestitApp(resource_mapping=[
            ResourceMapping("/", TestResource())
        ])

        with start_server_with_wsgi_app(restit_app) as port:
            response = requests.get(f"http://127.0.0.1:{port}/")
            self.assertEqual(200, response.status_code)
