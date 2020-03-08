from http import HTTPStatus
from typing import Tuple, AnyStr, Dict, Union

from restit._internal.resource_path import ResourcePath
from restit._internal.wsgi_request_environment import RequestType
from restit.request import Request
from restit.response import Response


class Resource:
    __url__ = None

    def __init__(self):
        self._resource_path = None
        self.__request_type_mapping = {
            RequestType.GET: self.get,
            RequestType.PUT: self.put,
            RequestType.POST: self.post,
            RequestType.DELETE: self.delete,
            RequestType.OPTIONS: self.options,
            RequestType.PATCH: self.patch,
            RequestType.CONNECT: self.connect,
            RequestType.HEAD: self.head,
            RequestType.TRACE: self.trace
        }

    def init(self):
        self._resource_path = ResourcePath(self.__url__)

    def get(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def put(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def delete(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def patch(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def options(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def trace(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def connect(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def head(self, request: Request) -> Response:
        return Response.from_http_status(HTTPStatus.METHOD_NOT_ALLOWED)

    def _handle_request(self, request_method: RequestType, request: Request, path_params: Dict) -> Response:
        return self.__request_type_mapping[request_method](request, **path_params)

    def _get_match(self, url: str) -> Tuple[bool, Union[None, Dict[str, AnyStr]]]:
        if self.__url__ is None:
            raise Resource.NoRegisteredUrlForResourceException(self)

        if not self._resource_path:
            raise Resource.InitFunctionNotCalledException()

        return self._resource_path.get_match(url)

    class NoRegisteredUrlForResourceException(Exception):
        pass

    class InitFunctionNotCalledException(Exception):
        pass
