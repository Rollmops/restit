from typing import Callable, Iterable


class WSGIBaseApp:
    def __call__(self, environ: dict, start_response: Callable) -> Iterable:
        pass
