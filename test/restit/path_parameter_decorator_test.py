import unittest
from collections import namedtuple

from restit import request_mapping, Request, Response, path_parameter, RestitApp, RestitTestApp
from restit.resource import Resource

PathParam = namedtuple("PathParam", ["name", "schema", "description"])


@request_mapping("/path/:id1/and/:id2/and/:id3")
@path_parameter("id1", type=int, description="First path parameter")
@path_parameter("id2", type=float, description="Second path parameter")
@path_parameter("id3")
class Resource1(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response(path_params)


class PathParameterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        restit_app = RestitApp(resources=[Resource1()])
        self.restit_test_app = RestitTestApp(restit_app)

    def test_path_parameters(self):
        response = self.restit_test_app.get("/path/1/and/10/and/20")
        self.assertEqual(200, response.get_status_code())
        self.assertEqual({'id1': 1, 'id2': 10.0, 'id3': '20'}, response.json())

    def test_conversion_exception(self):
        response = self.restit_test_app.get("/path/1/and/hans/and/20")
        self.assertEqual(400, response.get_status_code())
        self.assertEqual(
            "<title>400 Bad Request</title>\n"
            "<h1>Bad Request</h1>\n"
            "<p>Path parameter value 'hans' is not matching 'PathParameter(name='id2', type=<class 'float'>, "
            "description='Second path parameter', format=None)' (could not convert string to float: 'hans')</p>\n",
            response.text
        )
