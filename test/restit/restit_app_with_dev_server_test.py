import requests

from restit import Hyperlink
from restit._response import Response
from restit.decorator import path
from restit.exception import MissingRequestMappingException
from restit.internal.default_favicon_resource import DefaultFaviconResource
from restit.request import Request
from restit.resource import Resource
from restit.restit_app import RestItApp
from test.base_test_server_test_case import BaseTestServerTestCase


@path("/")
class MyResource(Resource):
    def get(self, request: Request, **kwargs) -> Response:
        return Response("Hallo")


@path("/no_methods")
class NoMethodsResource(Resource):
    pass


@path("/miau")
class MyResource2(Resource):
    def get(self, request: Request) -> Response:
        return Response("wuff")

    def post(self, request: Request) -> Response:
        return Response("", 204)


@path("/miau/:id")
class ResourceWithPathParams(Resource):

    def get(self, request: Request) -> Response:
        return Response(request.path_parameters)


@path("/error")
class ErrorResource(Resource):
    def get(self, request: Request) -> Response:
        raise Exception("OH NOOOO")


@path("/resource_with_hyperlink")
class ResourceWithHyperLink(Resource):
    def get(self, request: Request) -> Response:
        return Response({
            "hyperlink_with_path_params": Hyperlink(ResourceWithPathParams, request).generate(id=10),
            "hyperlink": Hyperlink(MyResource, request).generate(),
            "hyperlink_with_path": Hyperlink("/path/to/hyperlink/:id", request).generate(id=10)
        })


@path("/resource_with_hyperlink_error")
class ResourceWithHyperLinkError(Resource):
    def get(self, request: Request) -> Response:
        return Response({
            "hyperlink_with_path_params": Hyperlink(ResourceWithPathParams, request).generate(not_there=10),
        })


class RestitAppTestCase(BaseTestServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseTestServerTestCase.resources = [
            MyResource(),
            MyResource2(),
            ResourceWithPathParams(),
            ErrorResource(),
            NoMethodsResource(),
            ResourceWithHyperLink(),
            ResourceWithHyperLinkError(),
            DefaultFaviconResource()
        ]
        BaseTestServerTestCase.setUpClass()

    def test_simple_get_resource(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/")
        self.assertEqual(200, response.status_code)
        self.assertEqual("Hallo", response.text)

        response = requests.get(f"http://127.0.0.1:{self.port}/miau")
        self.assertEqual(200, response.status_code)
        self.assertEqual("wuff", response.text)

    def test_method_not_allowed_405(self):
        for method in ["get", "delete", "put", "post", "patch", "trace", "connect"]:
            response = requests.request(method, f"http://127.0.0.1:{self.port}/no_methods")
            self.assertEqual(405, response.status_code)
            self.assertIn("405 Method Not Allowed", response.text)

        response = requests.head(f"http://127.0.0.1:{self.port}/no_methods")
        self.assertEqual(405, response.status_code)
        self.assertEqual("", response.text)

    def test_options_method(self):
        response = requests.options(f"http://127.0.0.1:{self.port}/miau")
        self.assertEqual(204, response.status_code)
        self.assertEqual("GET POST OPTIONS", response.headers["Allow"])

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
        self.assertIn("<title>500 Internal Server Error</title>", response.text)
        self.assertIn("<h1>Internal Server Error</h1>", response.text)
        self.assertIn("OH NOOOO", response.text)

    def test_internal_server_error_as_rfc7807_json(self):
        response = requests.get(
            f"http://127.0.0.1:{self.port}/error", headers={'Accept': "application/json", "Accept-Charset": "utf-8"}
        )
        self.assertEqual(500, response.status_code)
        self.assertEqual("Internal Server Error", response.json()["title"])
        self.assertEqual(500, response.json()["status"])
        self.assertEqual("application/problem+json", response.headers["Content-Type"])

    def test_missing_request_mapping(self):
        class ResourceWithoutRequestMapping(Resource):
            pass

        with self.assertRaises(MissingRequestMappingException):
            RestItApp(resources=[ResourceWithoutRequestMapping()])

    def test_hyperlink(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/resource_with_hyperlink")
        self.assertEqual(200, response.status_code)
        self.assertEqual({
            "hyperlink_with_path_params": f"http://127.0.0.1:{self.port}/miau/10",
            'hyperlink_with_path': f'http://127.0.0.1:{self.port}/path/to/hyperlink/10',
            "hyperlink": f"http://127.0.0.1:{self.port}/"
        }, response.json())

    def test_hyperlink_with_x_forwarded(self):
        response = requests.get(
            f"http://127.0.0.1:{self.port}/resource_with_hyperlink",
            headers={"X-Forwarded-Host": "my.server.com:8080", "X-Forwarded-Proto": "https"}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual({
            "hyperlink_with_path_params": 'https://my.server.com:8080/miau/10',
            'hyperlink_with_path': 'https://my.server.com:8080/path/to/hyperlink/10',
            "hyperlink": 'https://my.server.com:8080/'
        }, response.json())

    def test_hyperlink_with_forwarded(self):
        response = requests.get(
            f"http://127.0.0.1:{self.port}/resource_with_hyperlink",
            headers={"Forwarded": "for=123.0.2.33; host=my.server.com:8080;proto=https"}
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual({
            "hyperlink_with_path_params": 'https://my.server.com:8080/miau/10',
            'hyperlink_with_path': 'https://my.server.com:8080/path/to/hyperlink/10',
            "hyperlink": 'https://my.server.com:8080/'
        }, response.json())

    def test_hyperlink_path_param_not_found(self):
        self.restit_app.debug = False
        response = requests.get(f"http://127.0.0.1:{self.port}/resource_with_hyperlink_error")
        self.assertEqual(500, response.status_code)
        self.assertEqual(
            "<title>500 Internal Server Error</title>\n"
            "<h1>Internal Server Error</h1>\n"
            "<p>ExpectedPathParameterForRequestMappingNotFoundException: The path parameter id in request "
            "mapping '/miau/:id' was not found in the provided path parameters {'not_there': 10}</p>\n",
            response.text
        )

    def test_default_favicon(self):
        response = requests.get(f"http://127.0.0.1:{self.port}/favicon.ico")
        self.assertEqual(200, response.status_code)
        self.assertEqual("", response.text)
