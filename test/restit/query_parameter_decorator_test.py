import unittest
from typing import List
from uuid import UUID

from restit import RestitApp, RestitTestApp, Request
from restit.query_parameter_decorator import query_parameter
from restit.request_mapping_decorator import request_mapping
from restit.resource import Resource
from restit.response import Response


@request_mapping("/1")
class QueryParametersResource(Resource):
    @query_parameter("param1", description="First parameter", type=int)
    @query_parameter("uuid", description="uuid parameter", type=UUID)
    def get(self, request: Request) -> Response:
        assert isinstance(request.get_query_parameters()["uuid"], UUID)

        return Response(
            {
                "param1": request.get_query_parameters()["param1"],
                "uuid": str(request.get_query_parameters()["uuid"])
            }
        )


@request_mapping("/2")
class QueryParameterListResource(Resource):
    @query_parameter("int_list", description="A list of ints", type=List[int])
    def get(self, request: Request, **path_params) -> Response:
        return Response(request.get_query_parameters())


class QueryParameterTest(unittest.TestCase):
    def setUp(self) -> None:
        restit_app = RestitApp(resources=[
            QueryParametersResource(),
            QueryParameterListResource()
        ])
        self.restit_test_app = RestitTestApp(restit_app)

    def test_query_parameter(self):
        response = self.restit_test_app.get("/1?param1=3&uuid=08695ead-392a-40ab-99fa-2fe64c3b48b4")
        self.assertEqual(200, response.get_status_code())
        self.assertEqual({"param1": 3, "uuid": '08695ead-392a-40ab-99fa-2fe64c3b48b4'}, response.json())

    def test_query_parameter_list(self):
        response = self.restit_test_app.get("/2?int_list=[1,2,3,4]")
        self.assertEqual(200, response.get_status_code())
        self.assertEqual({"int_list": [1, 2, 3, 4]}, response.json())
