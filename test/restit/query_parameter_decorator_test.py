import unittest
from uuid import UUID

from marshmallow import fields

from restit import RestItApp, RestItTestApp, Request
from restit._response import Response
from restit.decorator import path, query_parameter
from restit.internal.query_parameter import QueryParameter
from restit.resource import Resource


@path("/1")
class QueryParametersResource(Resource):
    @query_parameter("param1", description="First parameter", field_type=fields.Integer())
    @query_parameter("uuid", description="uuid parameter", field_type=fields.UUID())
    def get(self, request: Request) -> Response:
        assert isinstance(request.query_parameters["uuid"], UUID)

        return Response(
            {
                "param1": request.query_parameters["param1"],
                "uuid": str(request.query_parameters["uuid"])
            }
        )


@path("/2")
class QueryParameterListResource(Resource):
    @query_parameter("int_list", description="A list of ints", field_type=fields.List(fields.Integer()))
    def get(self, request: Request) -> Response:
        return Response(request.query_parameters)


class QueryParameterTest(unittest.TestCase):
    def setUp(self) -> None:
        restit_app = RestItApp(resources=[
            QueryParametersResource(),
            QueryParameterListResource()
        ])
        self.restit_test_app = RestItTestApp.from_restit_app(restit_app)

    def test_query_parameter(self):
        response = self.restit_test_app.get("/1?param1=3&uuid=08695ead-392a-40ab-99fa-2fe64c3b48b4")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"param1": 3, "uuid": '08695ead-392a-40ab-99fa-2fe64c3b48b4'}, response.json())

    def test_query_parameter_list(self):
        response = self.restit_test_app.get("/2?int_list=[1,2,3,4]")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"int_list": [1, 2, 3, 4]}, response.json())

    def test_unsupported_query_field_type(self):
        with self.assertRaises(QueryParameter.UnsupportedQueryFieldTypeException):
            @query_parameter("wrong", "I have a wrong field type", int)
            def dummy():
                pass
