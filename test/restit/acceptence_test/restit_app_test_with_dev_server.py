import unittest

from restit import RestItApp, Namespace
from restit.open_api import OpenApiDocumentation
from restit.open_api.info_object import InfoObject
from test.restit.acceptence_test.example_resource import TodosResource
from test.restit.acceptence_test.todo_repo import TodoRepo


class RestitAppWithDevSeverTestCase(unittest.TestCase):
    def setUp(self) -> None:
        repo = TodoRepo()

        todo_namespace = Namespace("/todos", resources=[TodosResource(repo)])

        self.restit_app = RestItApp(
            namespaces=[todo_namespace],
            open_api_documentation=OpenApiDocumentation(
                info=InfoObject(title="Sample TODO Api", version="1.0.0", description="Demonstrate the RestIt library"),
                path="/todos/api.rst"
            ), debug=True
        )

    @unittest.skip("")
    def test_generate_spec(self):
        self.restit_app._init()

        self.restit_app.start_development_server()

        spec = self.restit_app._open_api_documentation.generate_spec()

        self.assertEqual({}, spec)
