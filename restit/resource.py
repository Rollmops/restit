from typing import Tuple, AnyStr, Dict, Union

from werkzeug import Request
from werkzeug.exceptions import MethodNotAllowed

from restit._internal.resource_path import ResourcePath
from restit.response import Response


class Resource:
    __request_mapping__ = None

    def __init__(self):
        self._resource_path = None

    def init(self):
        self._resource_path = ResourcePath(self.__request_mapping__)

    def get(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def put(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def delete(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def patch(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def options(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def trace(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def connect(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def head(self, request: Request) -> Response:
        raise MethodNotAllowed()

    def _handle_request(self, request_method: str, request: Request, path_params: Dict) -> Response:
        method = getattr(self, request_method.lower())
        return method(request, **path_params)

    def _get_match(self, url: str) -> Tuple[bool, Union[None, Dict[str, AnyStr]]]:
        assert self._resource_path
        return self._resource_path.get_match(url)
