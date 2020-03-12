import unittest

from restit.request_mapping_decorator import PathIsNotStartingWithSlashException, request_mapping
from restit.resource import Resource


class CommonTestCase(unittest.TestCase):
    def test_request_mapping_is_not_starting_with_slash(self):
        with self.assertRaises(PathIsNotStartingWithSlashException):
            @request_mapping("not_starting_with_slash")
            class _(Resource):
                pass
