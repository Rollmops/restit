from contextlib import contextmanager
from threading import Thread
from wsgiref.simple_server import make_server


@contextmanager
def start_server_with_wsgi_app(wsgi_app):
    with make_server('', 0, wsgi_app) as httpd:
        thread = Thread(target=httpd.serve_forever)
        thread.start()
        try:
            yield httpd.server_port
        finally:
            httpd.shutdown()
            thread.join()
