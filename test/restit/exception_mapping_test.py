import unittest

from restit import Resource, Request, Response, RestItTestApp
from restit.decorator import path, exception_mapping
from restit.exception import BadRequest, NotFound


class MyException1(Exception):
    pass


@path("/")
@exception_mapping({MyException1: BadRequest})
class MyResource(Resource):
    def get(self, request: Request) -> Response:
        raise MyException1("Hello")

    @exception_mapping({MyException1: (NotFound, "Miau")})
    def post(self, request: Request) -> Response:
        raise MyException1()


class ExceptionMappingTestTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.restit_test_app = RestItTestApp(resources=[MyResource()], raise_exceptions=True)

    def test_map_exception(self):
        with self.assertRaises(BadRequest) as exception:
            self.restit_test_app.get("/")

        self.assertEqual("Hello", str(exception.exception))

    def test_override(self):
        with self.assertRaises(NotFound) as exception:
            self.restit_test_app.post("/")

        self.assertEqual("Miau", str(exception.exception))
