import unittest
from contextlib import contextmanager
from threading import Thread
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

import requests


def wsgi_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    ret = [
        f"{key}: {value}\n".encode("utf-8")
        for key, value in environ.items()
    ]
    return ret


class WsgiLearningTestCase(unittest.TestCase):
    def test_wsgi_application_get(self):
        with self._start_server() as port:
            response = requests.get(f"http://127.0.0.1:{port}")
            self.assertEqual(200, response.status_code)
            self.assertIn("REQUEST_METHOD: GET", response.text)

    def test_wsgi_application_post(self):
        with self._start_server() as port:
            response = requests.post(f"http://127.0.0.1:{port}")
            self.assertEqual(200, response.status_code)
            self.assertIn("REQUEST_METHOD: POST", response.text)

    @contextmanager
    def _start_server(self):
        with make_server('', 0, wsgi_app) as httpd:
            thread = Thread(target=httpd.handle_request)
            thread.start()
            yield httpd.server_port
