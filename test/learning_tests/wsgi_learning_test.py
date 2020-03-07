import unittest
from threading import Thread
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults

import requests
from requests import Response


def wsgi_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    ret = [("%s: %s\n" % (key, value)).encode("utf-8")
           for key, value in environ.items()]
    return ret


class WsgiLearningTestCase(unittest.TestCase):
    def test_wsgi_application(self):
        with make_server('', 0, wsgi_app) as httpd:
            thread = Thread(target=httpd.serve_forever)
            thread.start()

            response: Response = requests.get(f"http://127.0.0.1:{httpd.server_port}")
            self.assertEqual(200, response.status_code)
            print(response.text)
            httpd.shutdown()
            thread.join()
