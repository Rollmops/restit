from http import HTTPStatus

import requests

from restit._response import Response
from restit.decorator import path
from restit.request import Request
from restit.resource import Resource
from test.base_test_server_test_case import BaseTestServerTestCase


@path("/")
class RequestBodyResource(Resource):
    def get(self, request: Request) -> Response:
        return Response({
            "body_dict": dict(request.typed_body[dict]),
            "body": request.body.decode(),
            "query_string": request.query_string,
            "query_parameters": request.query_parameters,
            "content_type": request.content_type.to_string()
        })

    def post(self, request: Request) -> Response:
        return Response({
            "body_dict": request.typed_body[dict],
            "body": request.body.decode(),
            "query_string": request.query_string,
            "query_parameters": request.query_parameters,
            "content_type": request.content_type.to_string()
        }, HTTPStatus.CREATED)


class RestitAppTestCase(BaseTestServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseTestServerTestCase.resources = [RequestBodyResource()]
        BaseTestServerTestCase.setUpClass()

    def test_request_value_test_post_with_json(self):
        port = self.port
        response = requests.post(f"http://127.0.0.1:{port}/", json={"key": "value"})

        self.assertEqual(201, response.status_code)
        self.assertEqual({
            'body': '{"key": "value"}',
            'body_dict': {"key": "value"},
            'query_parameters': {},
            'query_string': '',
            'content_type': 'application/json'
        }, response.json())

    def test_request_value_test_get_with_json(self):
        port = self.port
        response = requests.get(f"http://127.0.0.1:{port}/", json={"key": "value"})

        self.assertEqual(200, response.status_code)
        self.assertEqual({
            'body': '{"key": "value"}',
            'body_dict': {'key': 'value'},
            'query_parameters': {},
            'query_string': '',
            'content_type': 'application/json'
        }, response.json())

    def test_request_value_test_post_with_data(self):
        port = self.port
        response = requests.post(f"http://127.0.0.1:{port}/", data={"key": "value"})
        self.assertEqual(201, response.status_code)
        self.assertEqual({
            'body': 'key=value',
            'body_dict': {'key': 'value'},
            'query_parameters': {},
            'query_string': '',
            'content_type': 'application/x-www-form-urlencoded'
        }, response.json())

    def test_request_value_test_get_with_data(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/", data={"key": "value"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({
            'body': 'key=value',
            'body_dict': {'key': 'value'},
            'query_parameters': {},
            'query_string': '',
            'content_type': 'application/x-www-form-urlencoded'
        }, response.json())

    def test_query_parameters_in_post(self):
        response = requests.post(f"http://127.0.0.1:{self.port}/?key=value")
        self.assertEqual(201, response.status_code)
        self.assertEqual({
            'body': '',
            'body_dict': {},
            'query_parameters': {"key": "value"},
            'query_string': 'key=value',
            'content_type': 'text/plain'
        }, response.json())

    def test_query_parameters_in_get(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/?key=value")
        self.assertEqual(200, response.status_code)
        self.assertEqual({
            'body': '',
            'body_dict': {},
            'query_parameters': {"key": "value"},
            'query_string': 'key=value',
            'content_type': 'text/plain'
        }, response.json())
