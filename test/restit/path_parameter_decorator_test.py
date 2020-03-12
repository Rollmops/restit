import unittest

from restit import request_mapping, Request, Response, path_parameter, RestitApp, RestitTestApp
from restit.path_parameter import PathParameter
from restit.resource import Resource


@request_mapping("/path/:id1/and/:id2/and/:id3")
@path_parameter("id1", type=int, description="First path parameter")
@path_parameter("id2", type=float, description="Second path parameter")
@path_parameter("id3", description="Id3")
class Resource1(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response(path_params)


@request_mapping(
    "/path/:id", path_parameters=[PathParameter("id", "Super path parameter", int)]
)
class Resource2(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response(path_params)


class PathParameterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        restit_app = RestitApp(resources=[Resource1(), Resource2()])
        self.restit_test_app = RestitTestApp(restit_app)

    def test_path_parameters(self):
        response = self.restit_test_app.get("/path/1/and/10/and/20")
        self.assertEqual(200, response.get_status_code())
        self.assertEqual({'id1': 1, 'id2': 10.0, 'id3': '20'}, response.json())

    def test_path_parameters_alternative_declaration(self):
        response = self.restit_test_app.get("/path/1")
        self.assertEqual(200, response.get_status_code())
        self.assertEqual({'id': 1}, response.json())

    def test_conversion_exception(self):
        response = self.restit_test_app.get("/path/1/and/hans/and/20")
        self.assertEqual(400, response.get_status_code())
        self.assertEqual(
            "<title>400 Bad Request</title>\n"
            "<h1>Bad Request</h1>\n"
            "<p>Path parameter value 'hans' is not matching 'PathParameter(name='id2', "
            "description='Second path parameter', type=<class 'float'>)' "
            "(could not convert string to float: 'hans')</p>\n",
            response.text
        )
