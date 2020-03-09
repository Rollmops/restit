import unittest
from threading import Thread
from typing import List
from wsgiref.simple_server import make_server

from restit.resource import Resource
from restit.restit_app import RestitApp


class BaseTestServerTestCase(unittest.TestCase):
    test_server = None
    thread = None
    resources: List[Resource] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.restit_app = RestitApp(resources=BaseTestServerTestCase.resources)

        cls.test_server = make_server("", 0, cls.restit_app)
        cls.thread = Thread(target=cls.test_server.serve_forever)
        cls.thread.start()
        cls.port = cls.test_server.server_port

    @classmethod
    def tearDownClass(cls) -> None:
        cls.test_server.shutdown()
        cls.thread.join()
