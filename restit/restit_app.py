import logging
import traceback
from contextlib import contextmanager
from functools import lru_cache
from typing import Iterable, Callable, List, Tuple, Dict, Union

# noinspection PyProtectedMember
from werkzeug.exceptions import HTTPException, InternalServerError, NotFound

from restit._internal.exception_response_maker import ExceptionResponseMaker
from restit.development_server import DevelopmentServer
from restit.namespace import Namespace
from restit.request import Request
from restit.resource import Resource
from restit.response import Response

LOGGER = logging.getLogger(__name__)


class RestitApp:
    def __init__(
            self, resources: List[Resource] = None,
            namespaces: List[Namespace] = None,
            expose_exceptions_to_sever: bool = False

    ):
        self.expose_exceptions_to_sever = expose_exceptions_to_sever
        self.__namespaces: List[Namespace] = []
        self.__resources: List[Resource] = []
        self.register_namespaces(namespaces or [])
        self.register_resources(resources or [])

        self.__init_called = False

    def register_resources(self, resources: List[Resource]):
        self.__check_resource_request_mapping(resources)
        self.__resources.extend(resources)
        self._create_url_ordered_resource()

    def register_namespaces(self, namespaces: List[Namespace]):
        for namespace in namespaces:
            self.register_resources(namespace.get_adapted_resources())

    def start_development_server(self, host: str = None, port: int = 5000, blocking: bool = True):
        development_server = DevelopmentServer(self, host, port)
        development_server.start(blocking=blocking)

    @contextmanager
    def start_development_server_in_context(self, host: str = None, port: int = 5000) -> int:
        development_server = DevelopmentServer(self, host, port)
        with development_server.start_in_context() as port:
            yield port

    @staticmethod
    def __check_resource_request_mapping(resources):
        for resource in resources:
            if resource.__request_mapping__ is None:
                raise RestitApp.MissingRequestMappingException(resource)

    def __init(self):
        for resource in self.__resources:
            resource.init()
        self.__init_called = True

    def __call__(self, environ: dict, start_response: Callable) -> Iterable:
        if not self.__init_called:
            self.__init()

        request = Request(environ)
        resource, path_params = self._find_resource_for_url(request.path)

        response = self._create_response_and_handle_exceptions(path_params, request, resource)

        header_as_list = [(key, value) for key, value in response.header.items()]
        start_response(response.get_status(), header_as_list)

        return [response.body_as_bytes]

    def _create_response_and_handle_exceptions(self, path_params: dict, request: Request, resource: Resource) \
            -> Response:
        try:
            response = self._get_response_or_raise_not_found(path_params, request, resource)
        except HTTPException as exception:
            LOGGER.info(str(exception))
            exception_response_maker = ExceptionResponseMaker(exception)
            response = exception_response_maker.create_response(request.accept_mimetypes)
        except Exception as exception:
            LOGGER.error(str(exception))
            LOGGER.error(traceback.format_exc())
            internal_exception = InternalServerError(str(exception) if self.expose_exceptions_to_sever else "")
            exception_response_maker = ExceptionResponseMaker(internal_exception)
            response = exception_response_maker.create_response(request.accept_mimetypes)
        return response

    @staticmethod
    def _get_response_or_raise_not_found(path_params: dict, request: Request, resource: Resource) -> Response:
        if resource is not None:
            # noinspection PyBroadException
            # noinspection PyProtectedMember
            response = resource._handle_request(
                request_method=request.method,
                request=request,
                path_params=path_params
            )
            response.serialize_response_body(request.accept_mimetypes)
        else:
            raise NotFound()
        return response

    @lru_cache()
    def _find_resource_for_url(self, url: str) -> Union[Tuple[None, None], Tuple[Resource, Dict]]:
        for resource in self.__resources:
            # noinspection PyProtectedMember
            is_matching, path_params = resource._get_match(url)
            if is_matching:
                return resource, path_params

        return None, None

    def _create_url_ordered_resource(self):
        self.__resources = sorted(self.__resources, key=lambda r: r.__request_mapping__, reverse=True)

    class MissingRequestMappingException(Exception):
        pass
