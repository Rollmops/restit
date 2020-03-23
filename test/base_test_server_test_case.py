import unittest
from typing import List, Union

from restit.resource import Resource
from restit.restit_app import RestItApp


class BaseTestServerTestCase(unittest.TestCase):
    test_server = None
    thread = None
    resources: List[Resource] = []
    restit_app: Union[RestItApp, None]

    @classmethod
    def setUpClass(cls) -> None:
        cls.restit_app = RestItApp(resources=BaseTestServerTestCase.resources, debug=True)
        cls.port = cls.restit_app.start_development_server(port=0, blocking=False)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.restit_app.stop_development_server()
