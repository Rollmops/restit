import json
import unittest
from datetime import datetime
from typing import Union, List, Type

from restit.common import get_default_encoding
from restit.internal.request_deserializer_service import RequestDeserializerService
from restit.request_deserializer import RequestDeserializer


class RequestDeserializerTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        RequestDeserializerService.clear_all_request_deserializers()
        RequestDeserializerService.restore_default_request_deserializers()

    def test_application_json_to_dict(self):
        json_bytes = json.dumps({"key": "value"}).encode()

        json_dict = RequestDeserializerService.deserialize_request_body(
            json_bytes, "application/json", dict, get_default_encoding()
        )

        self.assertEqual(json_dict, {"key": "value"})

    def test_form_data_to_dict(self):
        json_dict = RequestDeserializerService.deserialize_request_body(
            b"key=value&key2=value", "application/x-www-form-urlencoded", dict, get_default_encoding()
        )

        self.assertEqual({'key': 'value', 'key2': 'value'}, json_dict)

    def test_request_deserializer_not_found_content_type(self):
        json_bytes = json.dumps({"key": "value"}).encode()
        with self.assertRaises(RequestDeserializerService.NoRequestDeserializerFoundException) as exception:
            RequestDeserializerService.deserialize_request_body(
                json_bytes, "whats/up", dict, get_default_encoding()
            )

        self.assertEqual(
            "Unable to find a request deserializer for content type whats/up to type <class 'dict'>",
            str(exception.exception)
        )

    def test_request_deserializer_not_found_for_python_type(self):
        json_bytes = json.dumps({"key": "value"}).encode()
        with self.assertRaises(RequestDeserializerService.NoRequestDeserializerFoundException) as exception:
            RequestDeserializerService.deserialize_request_body(
                json_bytes, "application/json", datetime, get_default_encoding()
            )

        self.assertEqual(
            "Unable to find a request deserializer for content type application/json to type "
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
            b"hello", "whats/up", str, get_default_encoding()
        )

        self.assertEqual("olleh", deserialized_value)
