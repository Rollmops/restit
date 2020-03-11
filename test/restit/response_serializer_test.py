import unittest
from typing import List

from werkzeug.datastructures import MIMEAccept
from werkzeug.exceptions import NotAcceptable

from restit.response import Response
from restit.response_serializer import ResponseSerializer
from restit.response_serializer.default_dict_json_response_serializer import DefaultDictJsonResponseSerializer
from restit.response_serializer.default_dict_text_response_serializer import DefaultDictTextResponseSerializer
from restit.response_serializer.dict_fallback_response_serializer import DictFallbackResponseSerializer
from restit.response_serializer.str_fallback_response_serializer import StringFallbackResponseSerializer


class ResponseSerializerTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        Response.restore_default_response_serializer()

    def test_default_dict_to_json(self):
        response = Response({"key": "value"})
        response.serialize_response_body(MIMEAccept([("application/json", 1)]))

        self.assertEqual(b'{"key": "value"}', response.content)

    def test_default_dict_to_text(self):
        response = Response({"key": "value"})
        response.serialize_response_body(MIMEAccept([("text/plain", 1)]))

        self.assertEqual(b'{"key": "value"}', response.content)

    def test_default_str_to_text(self):
        response = Response("Test")
        response.serialize_response_body(MIMEAccept([("text/plain", 1)]))

        self.assertEqual(b'Test', response.content)

    def test_clear_all_default_serializer(self):
        Response.clear_all_response_serializer()
        response = Response("Test")
        with self.assertRaises(NotAcceptable):
            response.serialize_response_body(MIMEAccept([("text/plain", 1)]))

    def test_register_response_serializer(self):
        class MyResponseSerializer(ResponseSerializer):
            def get_response_data_type(self) -> type:
                return str

            def get_media_type_strings(self) -> List[str]:
                return ["my/type"]

            def get_content_type(self) -> str:
                return "my/type"

            def serialize(self, response_input: str) -> bytes:
                return "".join(reversed(response_input)).encode()

        Response.register_response_serializer(MyResponseSerializer())
        response = Response("Test")
        response.serialize_response_body(MIMEAccept([("my/type", 1)]))

        self.assertEqual(b'tseT', response.content)

    def test_prioritize_media_type(self):
        media_type = MIMEAccept([("application/json", 1), ("text/plain", 0.7)])

        Response.clear_all_response_serializer()

        Response.register_response_serializer(DefaultDictJsonResponseSerializer())
        Response.register_response_serializer(DefaultDictTextResponseSerializer())

        response = Response({"key": "value"})
        response.serialize_response_body(media_type)

        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual("application/json", response._headers["Content-Type"])

    def test_dict_fallback_response_serializer(self):
        Response.register_response_serializer(DictFallbackResponseSerializer())
        response = Response({"key": "value"})
        response.serialize_response_body(MIMEAccept([("wuff/miau", 1)]))

        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual("application/json", response._headers["Content-Type"])

    def test_string_fallback_response_serializer(self):
        Response.register_response_serializer(StringFallbackResponseSerializer())
        response = Response("huhu")
        response.serialize_response_body(MIMEAccept([("wuff/miau", 1)]))

        self.assertEqual(b'huhu', response.content)
        self.assertEqual("text/plain", response._headers["Content-Type"])
