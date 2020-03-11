import requests

from restit.request import Request
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response
from restit.restit_app import RestitApp
from test.base_test_server_test_case import BaseTestServerTestCase


@request_mapping("/")
class MyResource(Resource):
    def get(self, request: Request) -> Response:
        return Response("Hallo")


@request_mapping("/no_methods")
class NoMethodsResource(Resource):
    pass


@request_mapping("/miau")
class MyResource2(Resource):
    def get(self, request: Request) -> Response:
        return Response("wuff", 201)


# @request_mapping("/parts")
# class PartsResource(Resource):
#     def get(self, id: int):
#         return Response({})
#
#     def put(self, id: int):
#         return Response("", 201)


# @request_mapping("/parts/:id")
# class PartResource(Resource):
#     def get(self, id: int):
#         return Response({})
#
#     def put(self, id: int):
#         return Response("", 201)
#

# @request_mapping(
#     path="/miau/:id/jdasdsa/:id2",
#     path_params = [
#         path_parameter("id", type=int, description="dsadjwqjhdjq"),
#         path_parameter("id2", type=int, description="dsadjwqjhdjq")
#     ]
# )
# @path_parameter("id", type=int, description="dsadjwqjhdjq")
# @path_parameter("id2", type=int, description="dsadjwqjhdjq")
@request_mapping("/miau/:id")
class ResourceWithPathParams(Resource):

    def get(self, request: Request, **path_params) -> Response:
        return Response(path_params)


@request_mapping("/error")
class ErrorResource(Resource):
    def get(self, request: Request) -> Response:
        raise Exception()


@request_mapping("/send-json")
class SendJsonResource(Resource):
    def get(self, request: Request) -> Response:
        return Response({"key": "value"})


class RestitAppTestCase(BaseTestServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseTestServerTestCase.resources = [
            MyResource(),
            MyResource2(),
            ResourceWithPathParams(),
            ErrorResource(),
            NoMethodsResource(),
            SendJsonResource()
        ]
        BaseTestServerTestCase.setUpClass()

    def test_simple_get_resource(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/")
        self.assertEqual(200, response.status_code)
        self.assertEqual("Hallo", response.text)

        response = requests.get(f"http://127.0.0.1:{self.port}/miau")
        self.assertEqual(201, response.status_code)
        self.assertEqual("wuff", response.text)

    def test_method_not_allowed_405(self):
        for method in ["get", "delete", "put", "post", "patch", "trace", "options", "connect"]:
            response = requests.request(method, f"http://127.0.0.1:{self.port}/no_methods")
            self.assertEqual(405, response.status_code)
            self.assertIn("405 Method Not Allowed", response.text)

        response = requests.head(f"http://127.0.0.1:{self.port}/no_methods")
        self.assertEqual(405, response.status_code)
        self.assertEqual("", response.text)

    def test_url_not_found(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/NOT_THERE")
        self.assertEqual(404, response.status_code)

    def test_resource_with_path_params(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/miau/21")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"id": "21"}, response.json())

    def test_internal_server_error(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/error")
        self.assertEqual(500, response.status_code)

    def test_internal_server_error_as_json(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/error", headers={'Accept': "application/json"})
        self.assertEqual(500, response.status_code)
        self.assertEqual('{"code": 500, "name": "Internal Server Error", "description": ""}', response.text)

    def test_missing_request_mapping(self):
        class ResourceWithoutRequestMapping(Resource):
            pass

        with self.assertRaises(RestitApp.MissingRequestMappingException):
            RestitApp(resources=[ResourceWithoutRequestMapping()])
