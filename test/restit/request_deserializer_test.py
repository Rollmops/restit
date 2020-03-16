import unittest

from restit.internal.request_deserializer_service import RequestDeserializerService


class RequestDeserializerTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        RequestDeserializerService.restore_default_request_deserializers()
        RequestDeserializerService.clear_all_request_deserializers()
