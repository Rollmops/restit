import logging
import signal
from contextlib import contextmanager
from threading import Thread
from time import sleep
from typing import Union, Callable, Generator, List
from wsgiref.simple_server import make_server, WSGIServer

LOGGER = logging.getLogger(__name__)


class DevelopmentServer:
    def __init__(self, wsgi_app: Callable, host: str = None, port: int = 0, stop_signals: List[int] = None):
        self.wsgi_app = wsgi_app
        self.host = host or "127.0.0.1"
        self.port = port
        self.stop_signals = stop_signals or [signal.SIGTERM, signal.SIGINT]
        self.server: Union[WSGIServer, None] = None
        self._thread: Union[Thread, None] = None
        self._is_running = False

    def start(self, blocking: bool = True) -> int:
        LOGGER.debug("Creating WSGI server for host %s and port %d", self.host, self.port)
        self._register_stop_signals()
        self.server = make_server(self.host, self.port, self.wsgi_app)
        self._thread = Thread(target=self.server.serve_forever)
        self._thread.start()
        self._is_running = True
        if blocking:
            LOGGER.info(
                "Starting development server in blocking mode at http://%s:%d/", self.host, self.server.server_port
            )
            self._wait_until_stopped()
        else:
            LOGGER.info("Development server is now running at http://%s:%d/", self.host, self.port)
            return self.server.server_port

    def _wait_until_stopped(self):
        while self._is_running:
            sleep(0.5)

    def _register_stop_signals(self):
        for stop_signal in self.stop_signals:
            LOGGER.debug("Registering signal %d as stop signal", stop_signal)
            signal.signal(stop_signal, self._stop_from_signal)

    def _stop_from_signal(self, signum: int, __):
        LOGGER.info("Received signal %d", signum)
        self.stop()

    def stop(self):
        LOGGER.info("Stopping development server")
        self._is_running = False
        self.server.shutdown()

    @contextmanager
    def start_in_context(self) -> Generator[int, None, None]:
        port = self.start(blocking=False)
        try:
            yield port
        finally:
            self.stop()
