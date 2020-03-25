import unittest

from restit import Hyperlink
from restit._response import Response
from restit.decorator import path
from restit.exception import MethodNotAllowed
from restit.request import Request
from restit.resource import Resource
from restit.restit_app import RestItApp
from restit.restit_test_app import RestItTestApp


@path("/")
class MyResource(Resource):
    def get(self, request: Request, **kwargs) -> Response:
        return Response(request.typed_body[dict])

    def post(self, request: Request, **kwargs) -> Response:
        return Response(request.typed_body[dict], 201)

    def put(self, request: Request, **kwargs) -> Response:
        return Response(request.typed_body[dict], 201)

    def delete(self, request: Request, **kwargs) -> Response:
        return Response(request.typed_body[dict], 201)


@path("/no_response_exception")
class NoResponseExceptionResource(Resource):
    def get(self, request: Request) -> Response:
        pass


@path("/no_methods")
class NoMethodsResource(Resource):
    pass


@path("/miau/:id")
class ResourceWithPathParams(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response(path_params)


@path("/resource_with_hyperlink")
class ResourceWithHyperLink(Resource):
    def get(self, request: Request, **kwargs) -> Response:
        return Response({
            "hyperlink_with_path_params": Hyperlink(ResourceWithPathParams, request).generate(id=10),
            "hyperlink": Hyperlink(MyResource, request).generate()
        })


@path("/pass_headers")
class PassHeadersResource(Resource):
    def get(self, request: Request, **kwargs) -> Response:
        headers = request.headers
        return Response(
            {
                'Accept': headers["Accept"],
                'Accept-Encoding': headers["Accept-Encoding"],
                'Content-Type': headers["Content-Type"],
                'Content-Encoding': headers["Content-Encoding"],
                'Accept-Charset': headers["Accept-Charset"]
            })


class RestitTestAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        resit_app = RestItApp(resources=[
            MyResource(),
            NoMethodsResource(),
            PassHeadersResource(),
            ResourceWithHyperLink(),
            ResourceWithPathParams(),
            NoResponseExceptionResource()
        ])
        self.resit_test_app = RestItTestApp.from_restit_app(resit_app)

    def test_get_json_body(self):
        response = self.resit_test_app.get("/", json={"key": "value"})
        self.assertEqual("Response(200 OK)", str(response))
        self.assertEqual(200, response.status_code)
        self.assertEqual({"key": "value"}, response.json())
        self.assertEqual('{"key": "value"}', response.text)
        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual({
            'Content-Encoding': None,
            'Content-Length': 16,
            'Content-Type': 'application/json'
        }, response._headers)

    def test_get_data_body(self):
        response = self.resit_test_app.get("/", data={"key": "value", "key2": "value2"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({'key': 'value', 'key2': 'value2'}, response.json())
        self.assertEqual('{"key": "value", "key2": "value2"}', response.text)
        self.assertEqual(b'{"key": "value", "key2": "value2"}', response.content)
        self.assertEqual({
            'Content-Encoding': None,
            'Content-Length': 34,
            'Content-Type': 'application/json'
        }, response._headers)

    def test_post(self):
        response = self.resit_test_app.post("/", json={"key": "value"})
        self.assertEqual(201, response.status_code)
        self.assertEqual({'key': 'value'}, response.json())
        self.assertEqual('{"key": "value"}', response.text)
        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual({
            'Content-Encoding': None,
            'Content-Length': 16,
            'Content-Type': 'application/json'
        }, response.headers)

    def test_put(self):
        response = self.resit_test_app.put("/", json={"key": "value"})
        self.assertEqual(201, response.status_code)
        self.assertEqual({'key': 'value'}, response.json())
        self.assertEqual('{"key": "value"}', response.text)
        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual({
            'Content-Encoding': None,
            'Content-Length': 16,
            'Content-Type': 'application/json'
        }, response._headers)

    def test_delete(self):
        response = self.resit_test_app.delete("/", json={"key": "value"})
        self.assertEqual(201, response.status_code)
        self.assertEqual({'key': 'value'}, response.json())
        self.assertEqual('{"key": "value"}', response.text)
        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual({
            'Content-Encoding': None,
            'Content-Length': 16,
            'Content-Type': 'application/json'
        }, response._headers)

    def test_no_method(self):
        self.assertEqual(405, self.resit_test_app.get("/no_methods").status_code)
        self.assertEqual(405, self.resit_test_app.post("/no_methods").status_code)
        self.assertEqual(405, self.resit_test_app.put("/no_methods").status_code)
        self.assertEqual(405, self.resit_test_app.delete("/no_methods").status_code)
        self.assertEqual(405, self.resit_test_app.patch("/no_methods").status_code)
        self.assertEqual(204, self.resit_test_app.options("/no_methods").status_code)

    def test_raise_if_enabled(self):
        self.resit_test_app.raise_exceptions = True
        with self.assertRaises(MethodNotAllowed):
            self.assertEqual(405, self.resit_test_app.get("/no_methods").status_code)
        with self.assertRaises(MethodNotAllowed):
            self.assertEqual(405, self.resit_test_app.get("/no_methods").status_code)
        with self.assertRaises(MethodNotAllowed):
            self.assertEqual(405, self.resit_test_app.post("/no_methods").status_code)
        with self.assertRaises(MethodNotAllowed):
            self.assertEqual(405, self.resit_test_app.put("/no_methods").status_code)
        with self.assertRaises(MethodNotAllowed):
            self.assertEqual(405, self.resit_test_app.delete("/no_methods").status_code)
        with self.assertRaises(MethodNotAllowed):
            self.assertEqual(405, self.resit_test_app.patch("/no_methods").status_code)

    def test_pass_headers(self):
        response = self.resit_test_app.get("/pass_headers", headers={"Accept-Charset": "utf-8"})
        self.assertEqual(200, response.status_code)
        self.assertEqual({
            'Accept': '*/*',
            'Accept-Charset': 'utf-8',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Encoding': 'gzip, deflate',
            'Content-Type': 'application/octet-stream'
        }, response.json())

    def test_hyperlinks(self):
        response = self.resit_test_app.get("/resource_with_hyperlink")

        self.assertEqual(200, response.status_code)
        self.assertEqual({
            'hyperlink': 'http://127.0.0.1/',
            'hyperlink_with_path_params': 'http://127.0.0.1/miau/10'
        }, response.json())

    def test_no_response_exception(self):
        self.resit_test_app.raise_exceptions = True
        with self.assertRaises(Resource.NoResponseReturnException):
            self.resit_test_app.get("/no_response_exception")
