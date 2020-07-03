import unittest
from http import HTTPStatus
from typing import List, Tuple, Any, Union

from marshmallow import fields, ValidationError, Schema

from restit._response import Response
from restit.exception import NotAcceptable
from restit.internal.default_response_serializer.default_dict_json_response_serializer import \
    DefaultDictJsonResponseSerializer
from restit.internal.default_response_serializer.default_dict_text_response_serializer import \
    DefaultDictTextResponseSerializer
from restit.internal.default_response_serializer.dict_fallback_response_serializer import DictFallbackResponseSerializer
from restit.internal.default_response_serializer.str_fallback_response_serializer import \
    StringFallbackResponseSerializer
from restit.internal.http_accept import HttpAccept
from restit.internal.mime_type import MIMEType
from restit.internal.response_serializer_service import ResponseSerializerService
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.response_serializer import ResponseSerializer, CanHandleResultType


class ResponseSerializerTestCase(unittest.TestCase):
    def tearDown(self) -> None:
        ResponseSerializerService.restore_default_response_serializer()

    def test_default_dict_to_json(self):
        response = Response({"key": "value"})
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept([MIMEType("application", "json")])
        )

        self.assertEqual(b'{"key": "value"}', response.content)

    def test_default_list_to_json(self):
        response = Response(["1", 2])
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept([MIMEType("application", "json")])
        )

        self.assertEqual(b'["1", 2]', response.content)

    def test_default_dict_to_text(self):
        response = Response({"key": "value"})
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept.from_accept_string("text/plain")
        )

        self.assertEqual(b'{"key": "value"}', response.content)

    def test_default_list_to_text(self):
        response = Response(["1", 2])
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept.from_accept_string("text/plain")
        )

        self.assertEqual(b'["1", 2]', response.content)

    def test_default_str_to_text(self):
        response = Response("Test")
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept.from_accept_string("text/plain")
        )

        self.assertEqual(b'Test', response.content)

    def test_clear_all_default_serializer(self):
        ResponseSerializerService.clear_all_response_serializer()
        response = Response("Test")
        with self.assertRaises(NotAcceptable):
            ResponseSerializerService.validate_and_serialize_response_body(
                response, HttpAccept.from_accept_string("text/plain")
            )

    def test_register_response_serializer(self):
        class MyResponseSerializer(ResponseSerializer):
            def get_response_data_type(self) -> type:
                return str

            def get_media_type_strings(self) -> List[str]:
                return ["my/type"]

            def validate_and_serialize(
                    self,
                    response_input: Any,
                    response_status_parameter: Union[None, ResponseStatusParameter],
                    can_handle_result: CanHandleResultType
            ) -> Tuple[bytes, str]:
                assert can_handle_result.mime_type.charset == "ascii"
                return "".join(reversed(response_input)).encode(encoding=can_handle_result.mime_type.charset), "my/type"

        ResponseSerializerService.register_response_serializer(MyResponseSerializer())
        response = Response("Test")
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept.from_accept_string("my/type; charset=ascii")
        )

        self.assertEqual(b'tseT', response.content)

    def test_prioritize_media_type(self):
        http_accept = HttpAccept([MIMEType("application", "json"), MIMEType("text", "plain", 0.7)])

        ResponseSerializerService.clear_all_response_serializer()

        ResponseSerializerService.register_response_serializer(DefaultDictJsonResponseSerializer())
        ResponseSerializerService.register_response_serializer(DefaultDictTextResponseSerializer())

        response = Response({"key": "value"})
        ResponseSerializerService.validate_and_serialize_response_body(response, http_accept)

        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual("application/json", response._headers["Content-Type"])

    def test_dict_fallback_response_serializer(self):
        ResponseSerializerService.register_response_serializer(DictFallbackResponseSerializer())
        response = Response({"key": "value"})
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept.from_accept_string("wuff/miau")
        )

        self.assertEqual(b'{"key": "value"}', response.content)
        self.assertEqual("application/json", response._headers["Content-Type"])

    def test_string_fallback_response_serializer(self):
        ResponseSerializerService.register_response_serializer(StringFallbackResponseSerializer())
        response = Response("huhu")
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept.from_accept_string("wuff/miau")
        )

        self.assertEqual(b'huhu', response.content)
        self.assertEqual("text/plain", response._headers["Content-Type"])

    def test_response_body_type_not_supported(self):
        response = Response(1.0)
        with self.assertRaises(Response.ResponseBodyTypeNotSupportedException):
            ResponseSerializerService.validate_and_serialize_response_body(
                response, HttpAccept.from_accept_string("application/json")
            )

    def test_str_response_body_with_schema(self):
        response = Response("1234")
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept.from_accept_string("text/plain"),
            ResponseStatusParameter(200, "", {"text/plain": fields.Integer()})
        )

        self.assertEqual(b"1234", response.content)
        self.assertEqual("1234", response.text)
        self.assertEqual("text/plain", response.headers["Content-Type"])

    def test_bytes_response_body_with_schema(self):
        response = Response(b"1234")
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept.from_accept_string("text/plain"),
            ResponseStatusParameter(200, "", {"text/plain": fields.Integer()})
        )

        self.assertEqual(b"1234", response.content)
        self.assertEqual("1234", response.text)
        self.assertEqual("text/plain", response.headers["Content-Type"])

    def test_str_response_validation_failed(self):
        response = Response("1234")
        with self.assertRaises(ValidationError):
            ResponseSerializerService.validate_and_serialize_response_body(
                response, HttpAccept.from_accept_string("text/plain"),
                ResponseStatusParameter(200, "", {"text/plain": fields.Email()})
            )

    def test_response_serializer_with_schema(self):
        class MySchema(Schema):
            field1 = fields.Integer()
            field2 = fields.String()

        response = Response({"field1": 1, "field2": "hello", "not_expected": "wuff"})
        ResponseSerializerService.validate_and_serialize_response_body(
            response, HttpAccept.from_accept_string("application/json"),
            ResponseStatusParameter(200, "", {"application/json": MySchema()})
        )

        self.assertIn('"field1": 1', response.text)
        self.assertIn('"field2": "hello"', response.text)
        self.assertNotIn("not_expected", response.text)
        self.assertIn(b'"field1": 1', response.content)
        self.assertIn(b'"field2": "hello"', response.content)
        self.assertNotIn(b"not_expected", response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.headers["Content-Type"])

    def test_not_implemented(self):
        response_serializer = ResponseSerializer()
        with self.assertRaises(NotImplementedError):
            response_serializer.get_media_type_strings()

        with self.assertRaises(NotImplementedError):
            response_serializer.get_response_data_type()

        with self.assertRaises(NotImplementedError):
            response_serializer.validate_and_serialize("", None, CanHandleResultType("", MIMEType.from_string("*/*")))

    def test_content_type_not_expected_exception(self):
        with self.assertRaises(ResponseSerializer.ContentTypeNotExpectedForResponseStatusException):
            ResponseSerializer.find_schema("hans/wurst", ResponseStatusParameter(HTTPStatus.OK, "", {}))
