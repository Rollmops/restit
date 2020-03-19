import unittest
from io import BytesIO

from restit import Request
from restit.internal.http_accept import HttpAccept


class RequestTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.wsgi_environment = self._create_wsgi_environment()

    def test_request_attributes(self):
        request = Request(self.wsgi_environment, {})

        self.assertEqual(b"1234567890", request.body)
        self.assertEqual("text/plain", request.content_type.to_string())
        self.assertEqual("gzip, deflate", request.content_encoding)
        self.assertEqual("utf-8", request.headers["Accept-Charset"])
        self.assertEqual("*/*", request.headers["Accept"])
        self.assertEqual("gzip, deflate", request.headers["Accept-Encoding"])
        self.assertEqual(HttpAccept.from_accept_string("*/*"), request.http_accept_object)
        self.assertEqual("/path", request.path)
        self.assertEqual({"param": "value", "param2": "value2"}, request.query_parameters)
        self.assertEqual("http://localhost:8080", request.host)
        self.assertEqual("http://localhost:8080/path?param=value&param2=value2", request.original_url)
        self.assertEqual("GET", request.request_method_name)

    def test_request_path_params(self):
        request = Request(self.wsgi_environment, {"id": 1})

        self.assertEqual({"id": 1}, request.path_parameters)

    def test_typed_body_json(self):
        self.wsgi_environment.update({
            "wsgi.input": BytesIO(b'{"key": "value"}'),
            "CONTENT_LENGTH": 16,
            "CONTENT_TYPE": "application/json"
        })
        request = Request(self.wsgi_environment, {})
        self.assertEqual({'key': 'value'}, request.typed_body[dict])

    @staticmethod
    def _create_wsgi_environment():
        return {
            "HTTP_ACCEPT": "*/*",
            "HTTP_ACCEPT_CHARSET": "utf-8",
            "CONTENT_ENCODING": "gzip, deflate",
            "HTTP_ACCEPT_ENCODING": "gzip, deflate",
            "REQUEST_METHOD": "GET",
            "PATH_INFO": "/path",
            "CONTENT_LENGTH": 10,
            "wsgi.input": BytesIO(b"1234567890"),
            "QUERY_STRING": "param=value&param2=value2",
            "CONTENT_TYPE": "text/plain",
            "wsgi.url_scheme": "http",
            "SERVER_PORT": "8080",
            "SERVER_NAME": "localhost",

        }
