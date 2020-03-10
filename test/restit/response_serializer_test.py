import unittest

from werkzeug.datastructures import MIMEAccept
from werkzeug.exceptions import NotAcceptable

from restit.response import Response
from restit.response_serializer import ResponseSerializer


class ResponseSerializerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        Response.restore_default_response_serializer()

    def test_default_dict_to_json(self):
        response = Response({"key": "value"})
        response.serialize_response_body(MIMEAccept([("application/json", 1)]))

        self.assertEqual(b'{"key": "value"}', response.body_as_bytes)

    def test_default_dict_to_text(self):
        response = Response({"key": "value"})
        response.serialize_response_body(MIMEAccept([("text/plain", 1)]))

        self.assertEqual(b'{"key": "value"}', response.body_as_bytes)

    def test_default_str_to_text(self):
        response = Response("Test")
        response.serialize_response_body(MIMEAccept([("text/plain", 1)]))

        self.assertEqual(b'Test', response.body_as_bytes)

    def test_clear_all_default_serializer(self):
        Response.clear_all_response_serializer()
        response = Response("Test")
        with self.assertRaises(NotAcceptable):
            response.serialize_response_body(MIMEAccept([("text/plain", 1)]))

    def test_register_response_serializer(self):
        class MyResponseSerializer(ResponseSerializer):
            def is_responsible_for_response_data_type(self, response_data_type: type) -> bool:
                return response_data_type == str

            def is_responsible_for_media_type(self, media_type: MIMEAccept) -> bool:
                return "my/type" in media_type

            def get_content_type(self) -> str:
                return "my/type"

            def serialize(self, response_input: str) -> bytes:
                return "".join(reversed(response_input)).encode()

        Response.register_response_serializer(MyResponseSerializer())
        response = Response("Test")
        response.serialize_response_body(MIMEAccept([("my/type", 1)]))

        self.assertEqual(b'tseT', response.body_as_bytes)
