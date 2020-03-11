import unittest
from typing import List, Union

from restit.resource import Resource
from restit.restit_app import RestitApp


class BaseTestServerTestCase(unittest.TestCase):
    test_server = None
    thread = None
    resources: List[Resource] = []
    restit_app: Union[RestitApp, None]

    @classmethod
    def setUpClass(cls) -> None:
        cls.restit_app = RestitApp(resources=BaseTestServerTestCase.resources)
        cls.port = cls.restit_app.start_development_server(port=0, blocking=False)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.restit_app.stop_development_server()
