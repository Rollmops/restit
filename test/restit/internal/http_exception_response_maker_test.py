import unittest

from restit.internal.http_accept import HttpAccept
from restit.internal.http_exception_response_maker import HttpExceptionResponseMaker
from restit.rfc7807_http_problem import Rfc7807HttpProblem


class HttpExceptionResponseMakerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.response_maker = HttpExceptionResponseMaker(
            Rfc7807HttpProblem("ERROR!", detail="Something is not working", status=500)
        )

    def test_make_application_json_error(self):
        response = self.response_maker.create_response(HttpAccept.from_accept_string("application/json"))

        self.assertEqual(500, response.get_status_code())
        self.assertEqual({
            'detail': 'Something is not working',
            'instance': None,
            'status': 500,
            'title': 'ERROR!',
            'type': 'about:blank'
        }, response.json())

    def test_make_html_response(self):
        response = self.response_maker.create_response(HttpAccept.from_accept_string("text/html"))

        self.assertEqual(500, response.get_status_code())
        self.assertEqual(
            "<title>500 ERROR!</title>\n"
            "<h1>ERROR!</h1>\n"
            "<p>Something is not working</p>\n",
            response.text
        )

    def test_fallback_text_error_response(self):
        response = self.response_maker.create_response(HttpAccept.from_accept_string("unknown/muh"))
        self.assertEqual(500, response.get_status_code())
        self.assertEqual(
            "500 ERROR!: Something is not working (None, about:blank)", response.text
        )
