import json
import unittest
from datetime import datetime
from typing import Union, List, Type

from restit.internal.mime_type import MIMEType
from restit.internal.request_deserializer_service import RequestDeserializerService
from restit.request_deserializer import RequestDeserializer


class RequestDeserializerTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        RequestDeserializerService.clear_all_request_deserializers()
        RequestDeserializerService.restore_default_request_deserializers()

    def test_application_json_to_dict(self):
        json_bytes = json.dumps({"key": "value"}).encode()

        json_dict = RequestDeserializerService.deserialize_request_body(
            json_bytes, MIMEType.from_string("application/json"), dict
        )

        self.assertEqual(json_dict, {"key": "value"})

    def test_form_data_to_dict(self):
        json_dict = RequestDeserializerService.deserialize_request_body(
            b"key=value&key2=value", MIMEType.from_string("application/x-www-form-urlencoded"), dict
        )

        self.assertEqual({'key': 'value', 'key2': 'value'}, json_dict)

    def test_request_deserializer_content_type_fallback(self):
        json_bytes = json.dumps({"key": "value"}).encode()
        with self.assertLogs(level="WARNING") as log:
            RequestDeserializerService.deserialize_request_body(
                json_bytes, MIMEType.from_string("whats/up"), dict
            )

        self.assertIn(
            'WARNING:restit.internal.default_request_deserializer.default_fallback_dict_deserializer:Trying to '
            'parse JSON from content type != application/json',
            log.output
        )

    def test_request_deserializer_not_found_for_python_type(self):
        json_bytes = json.dumps({"key": "value"}).encode()
        with self.assertRaises(RequestDeserializerService.NoRequestDeserializerFoundException) as exception:
            RequestDeserializerService.deserialize_request_body(
                json_bytes, MIMEType.from_string("application/json"), datetime
            )

        self.assertEqual(
            "Unable to find a request deserializer for content type MIMEType(type=application, subtype=json, "
            "quality=1.0, details={}) to type "
            "<class 'datetime.datetime'>", str(exception.exception)
        )

    def test_custom_request_deserializer(self):
        class MyRequestDeserializer(RequestDeserializer):
            def get_content_type_list(self) -> Union[List[str], None]:
                return ["whats/up"]

            def get_deserialized_python_type(self) -> Type:
                return str

            def deserialize(self, request_input: bytes, encoding: str = None) -> str:
                return "".join(reversed(request_input.decode()))

        RequestDeserializerService.register_request_deserializer(MyRequestDeserializer())

        deserialized_value = RequestDeserializerService.deserialize_request_body(
            b"hello", MIMEType.from_string("whats/up"), str
        )

        self.assertEqual("olleh", deserialized_value)

    def test_not_implemented_error(self):
        request_deserializer = RequestDeserializer()
        with self.assertRaises(NotImplementedError):
            request_deserializer.get_content_type_list()
        with self.assertRaises(NotImplementedError):
            request_deserializer.get_deserialized_python_type()
        with self.assertRaises(NotImplementedError):
            request_deserializer.deserialize(b"", "")
