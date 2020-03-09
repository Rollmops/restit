import logging
from contextlib import contextmanager
from threading import Thread
from typing import Union, Callable, Generator
from wsgiref.simple_server import make_server, WSGIServer

LOGGER = logging.getLogger(__name__)


class DevelopmentServer:
    def __init__(self, wsgi_app: Callable, host: str = None, port: int = 0):
        self.wsgi_app = wsgi_app
        self.host = host or ""
        self.port = port
        self.server: Union[WSGIServer, None] = None
        self._thread: Union[Thread, None] = None

    def start(self, blocking: bool = True) -> int:
        LOGGER.debug("Creating WSGI server for host %s and port %d", self.host, self.port)
        self.server = make_server(self.host, self.port, self.wsgi_app)
        if blocking:
            LOGGER.debug("Starting development server in blocking mode")
            self.server.serve_forever()
        else:
            LOGGER.debug("Starting development server in non-blocking mode")
            self._thread = Thread(target=self.server.serve_forever)
            self._thread.start()
            return self.server.server_port

    def stop(self):
        LOGGER.debug("Stopping development server")
        self.server.shutdown()
        self._thread.join()

    @contextmanager
    def start_in_context(self) -> Generator[int, None, None]:
        port = self.start(blocking=False)
        try:
            yield port
        finally:
            self.stop()
