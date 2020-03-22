import unittest

from restit.exception import InternalServerError
from restit.internal.http_accept import HttpAccept
from restit.internal.http_error_response_maker import HttpErrorResponseMaker


class HttpExceptionResponseMakerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.response_maker = HttpErrorResponseMaker(
            InternalServerError("Something is not working")
        )

    def test_make_application_json_error(self):
        response = self.response_maker.create_response(HttpAccept.from_accept_string("application/json"))

        self.assertEqual(500, response.status_code)
        self.assertEqual({
            'detail': 'Something is not working',
            'instance': None,
            'status': 500,
            'title': 'Internal Server Error',
            'type': 'https://developer.mozilla.org/de/docs/Web/HTTP/Status/500'
        }, response.json())

    def test_make_html_response_no_debug(self):
        response = self.response_maker.create_response(HttpAccept.from_accept_string("text/html"))

        self.assertEqual(500, response.status_code)
        self.assertIn("<title>500 Internal Server Error</title>", response.text)
        self.assertIn("<h1>Internal Server Error</h1>", response.text)
        self.assertIn("<p>Something is not working</p>", response.text)

    def test_make_html_response_debug(self):
        response = HttpErrorResponseMaker(
            InternalServerError("Something is not working", traceback="traceback"), debug=True
        ).create_response(HttpAccept.from_accept_string("text/html"))

        self.assertEqual(500, response.status_code)
        self.assertIn("<title>500 Internal Server Error</title>", response.text)
        self.assertIn("<h1>Internal Server Error</h1>", response.text)
        self.assertIn("Something is not working", response.text)
        self.assertIn("traceback", response.text)

    def test_fallback_text_error_response(self):
        response = self.response_maker.create_response(HttpAccept.from_accept_string("unknown/muh"))
        self.assertEqual(500, response.status_code)
        self.assertEqual(
            "500 Internal Server Error: Something is not working", response.text
        )
