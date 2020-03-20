import unittest
from unittest.mock import Mock

from restit import Resource


class ResourceTestCase(unittest.TestCase):
    def test_sort_resources(self):
        resources = [Mock() for _ in range(7)]
        resources[0].__request_mapping__ = "/users"
        resources[1].__request_mapping__ = "/"
        resources[2].__request_mapping__ = "/users/api.rst/"
        resources[3].__request_mapping__ = "/users/:id"
        resources[4].__request_mapping__ = "/:wuff/:id"
        resources[5].__request_mapping__ = "/users/:id/size/:id2"
        resources[6].__request_mapping__ = "/users/:id/size/api.rst"

        resources = Resource.sort_resources(resources)

        self.assertEqual([
            "/users/:id/size/api.rst",
            "/users/:id/size/:id2",
            "/users/api.rst/",
            "/users/:id",
            "/:wuff/:id",
            "/users",
            "/"
        ], [r.__request_mapping__ for r in resources])
