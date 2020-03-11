import unittest

from werkzeug.exceptions import MethodNotAllowed

from restit import Hyperlink
from restit.request import Request
from restit.request_mapping import request_mapping
from restit.resource import Resource
from restit.response import Response
from restit.restit_app import RestitApp
from restit.restit_test_app import RestitTestApp


@request_mapping("/")
class MyResource(Resource):
    def get(self, request: Request) -> Response:
        return Response(request.get_body_as_dict())

    def post(self, request: Request) -> Response:
        return Response(request.get_body_as_dict(), 201)

    def put(self, request: Request) -> Response:
        return Response(request.get_body_as_dict(), 201)

    def delete(self, request: Request) -> Response:
        return Response(request.get_body_as_dict(), 201)


@request_mapping("/no_methods")
class NoMethodsResource(Resource):
    pass


@request_mapping("/miau/:id")
class ResourceWithPathParams(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response(path_params)


@request_mapping("/resource_with_hyperlink")
class ResourceWithHyperLink(Resource):
    def get(self, request: Request) -> Response:
        return Response({
            "hyperlink_with_path_params": Hyperlink(ResourceWithPathParams).generate(request, id=10),
            "hyperlink": Hyperlink(MyResource).generate(request)
        })


@request_mapping("/pass_headers")
class PassHeadersResource(Resource):
    def get(self, request: Request) -> Response:
        return Response(request.get_headers())


class RestitTestAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        resit_app = RestitApp(resources=[
            MyResource(),
            NoMethodsResource(),
            PassHeadersResource(),
            ResourceWithHyperLink(),
            ResourceWithPathParams()
        ])
        self.resit_test_app = RestitTestApp(resit_app)

    def test_get_json_body(self):
        response = self.resit_test_app.get("/", json={"key": "value"})
        self.assertEqual(200, response.get_status_code())
        self.assertEqual({"key": "value"}, response.json())
        self.assertEqual('{"key": "value"}', response.text)
        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual({
            'Content-Encoding': 'utf-8',
            'Content-Length': 16,
            'Content-Type': 'application/json'
        }, response._headers)

    def test_get_data_body(self):
        response = self.resit_test_app.get("/", data={"key": "value", "key2": "value2"})
        self.assertEqual(200, response.get_status_code())
        self.assertEqual({'key': 'value', 'key2': 'value2'}, response.json())
        self.assertEqual('{"key": "value", "key2": "value2"}', response.text)
        self.assertEqual(b'{"key": "value", "key2": "value2"}', response.content)
        self.assertEqual({
            'Content-Encoding': 'utf-8',
            'Content-Length': 34,
            'Content-Type': 'application/json'
        }, response._headers)

    def test_post(self):
        response = self.resit_test_app.post("/", json={"key": "value"})
        self.assertEqual(201, response.get_status_code())
        self.assertEqual({'key': 'value'}, response.json())
        self.assertEqual('{"key": "value"}', response.text)
        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual({
            'Content-Encoding': 'utf-8',
            'Content-Length': 16,
            'Content-Type': 'application/json'
        }, response._headers)

    def test_put(self):
        response = self.resit_test_app.put("/", json={"key": "value"})
        self.assertEqual(201, response.get_status_code())
        self.assertEqual({'key': 'value'}, response.json())
        self.assertEqual('{"key": "value"}', response.text)
        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual({
            'Content-Encoding': 'utf-8',
            'Content-Length': 16,
            'Content-Type': 'application/json'
        }, response._headers)

    def test_delete(self):
        response = self.resit_test_app.delete("/", json={"key": "value"})
        self.assertEqual(201, response.get_status_code())
        self.assertEqual({'key': 'value'}, response.json())
        self.assertEqual('{"key": "value"}', response.text)
        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual({
            'Content-Encoding': 'utf-8',
            'Content-Length': 16,
            'Content-Type': 'application/json'
        }, response._headers)

    def test_no_method(self):
        self.assertEqual(405, self.resit_test_app.get("/no_methods").get_status_code())
        self.assertEqual(405, self.resit_test_app.post("/no_methods").get_status_code())
        self.assertEqual(405, self.resit_test_app.put("/no_methods").get_status_code())
        self.assertEqual(405, self.resit_test_app.delete("/no_methods").get_status_code())
        self.assertEqual(405, self.resit_test_app.patch("/no_methods").get_status_code())
        self.assertEqual(405, self.resit_test_app.options("/no_methods").get_status_code())

    def test_raise_if_enabled(self):
        self.resit_test_app.set_raise_on_exceptions(True)
        with self.assertRaises(MethodNotAllowed):
            self.assertEqual(405, self.resit_test_app.get("/no_methods").get_status_code())
            self.assertEqual(405, self.resit_test_app.post("/no_methods").get_status_code())
            self.assertEqual(405, self.resit_test_app.put("/no_methods").get_status_code())
            self.assertEqual(405, self.resit_test_app.delete("/no_methods").get_status_code())
            self.assertEqual(405, self.resit_test_app.patch("/no_methods").get_status_code())
            self.assertEqual(405, self.resit_test_app.options("/no_methods").get_status_code())

    def test_pass_headers(self):
        response = self.resit_test_app.get("/pass_headers")
        self.assertEqual(200, response.get_status_code())
        self.assertEqual({
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': '*/*',
            'Host': '127.0.0.1'
        }, response.json())

    def test_hyperlinks(self):
        response = self.resit_test_app.get("/resource_with_hyperlink")

        self.assertEqual(200, response.get_status_code())
        self.assertEqual({
            'hyperlink': 'http://127.0.0.1/',
            'hyperlink_with_path_params': 'http://127.0.0.1/miau/10'
        }, response.json())
