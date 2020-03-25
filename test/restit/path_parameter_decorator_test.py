import unittest

from marshmallow import fields

from restit import Request, Response, RestItApp, RestItTestApp
from restit._path_parameter import PathParameter
from restit.decorator import path, path_parameter
from restit.resource import Resource


@path("/path/:id1/and/:id2/and/:id3")
@path_parameter("id1", field_type=fields.Integer(), description="First path parameter")
@path_parameter("id2", field_type=fields.Float(), description="Second path parameter")
@path_parameter("id3", description="Id3")
class Resource1(Resource):
    def get(self, request: Request) -> Response:
        return Response(request.path_parameters)


@path(
    "/path/:id", path_parameters=[PathParameter("id", "Super path parameter", fields.Integer())]
)
class Resource2(Resource):
    def get(self, request: Request) -> Response:
        return Response(request.path_parameters)


class PathParameterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        restit_app = RestItApp(resources=[Resource1(), Resource2()])
        self.restit_test_app = RestItTestApp.from_restit_app(restit_app)

    def test_path_parameters(self):
        response = self.restit_test_app.get("/path/1/and/10/and/20")
        self.assertEqual(200, response.status_code)
        self.assertEqual({'id1': 1, 'id2': 10.0, 'id3': '20'}, response.json())

    def test_path_parameters_alternative_declaration(self):
        response = self.restit_test_app.get("/path/1")
        self.assertEqual(200, response.status_code)
        self.assertEqual({'id': 1}, response.json())

    def test_conversion_exception(self):
        response = self.restit_test_app.get("/path/1/and/hans/and/20")
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            "<title>400 Bad Request</title>\n"
            "<h1>Bad Request</h1>\n"
            "<p>Path parameter value 'hans' is not matching 'PathParameter(name='id2', "
            "description='Second path parameter', field_type=<fields.Float(default=<marshmallow.missing>, "
            "attribute=None, validate=None, required=False, load_only=False, dump_only=False, "
            "missing=<marshmallow.missing>, allow_none=False, error_messages={'required': 'Missing data for "
            "required field.', 'null': 'Field may not be null.', 'validator_failed': 'Invalid value.', 'invalid': "
            "'Not a valid number.', 'too_large': 'Number too large.', 'special': 'Special numeric values "
            "(nan or infinity) are not permitted.'})>)' (Not a valid number.)</p>\n",
            response.text
        )
