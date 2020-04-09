import unittest

from restit.decorator import path
from restit.exception import PathIsNotStartingWithSlashException
from restit.resource import Resource


class CommonTestCase(unittest.TestCase):
    def test_request_mapping_is_not_starting_with_slash(self):
        with self.assertRaises(PathIsNotStartingWithSlashException):
            @path("not_starting_with_slash")
            class _(Resource):
                pass
