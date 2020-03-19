import logging
import traceback
from contextlib import contextmanager
from functools import lru_cache
from typing import Iterable, Callable, List, Tuple, Dict, Union

from restit.development_server import DevelopmentServer
from restit.exception import InternalServerError, NotFound
from restit.exception.http_error import HttpError
from restit.internal.default_favicon_resource import DefaultFaviconResource
from restit.internal.http_error_response_maker import HttpErrorResponseMaker
from restit.namespace import Namespace
from restit.open_api.open_api_documentation import OpenApiDocumentation
from restit.open_api.open_api_resource import OpenApiResource
from restit.request import Request
from restit.resource import Resource
from restit.response import Response

LOGGER = logging.getLogger(__name__)


class RestitApp:
    def __init__(
            self, resources: List[Resource] = None,
            namespaces: List[Namespace] = None,
            debug: bool = False,
            raise_exceptions: bool = False,
            open_api_documentation: OpenApiDocumentation = None

    ):
        self._debug = debug
        self._namespaces: List[Namespace] = []
        self._resources: List[Resource] = []
        self._raise_exceptions = raise_exceptions
        self._open_api_documentation = open_api_documentation
        self.register_namespaces(namespaces or [])
        self.register_resources(resources or [])

        self.__development_server: Union[DevelopmentServer, None] = None

        self._init_called = False

    def set_open_api_documentation(self, open_api_documentation: OpenApiDocumentation):
        self._open_api_documentation = open_api_documentation

    def set_raise_on_exceptions(self, raise_on_exceptions: bool):
        self._raise_exceptions = raise_on_exceptions

    def set_debug(self, debug: bool):
        self._debug = debug

    def register_resources(self, resources: List[Resource]):
        self.__check_resource_request_mapping(resources)
        self._resources.extend(resources)
        self._resources = Resource.sort_resources(self._resources)

    def register_namespaces(self, namespaces: List[Namespace]):
        for namespace in namespaces:
            self.register_resources(namespace.get_adapted_resources())

    def start_development_server(self, host: str = None, port: int = 5000, blocking: bool = True) -> int:
        self.__development_server = DevelopmentServer(self, host, port)
        self.__development_server.start(blocking=blocking)
        return self.__development_server.server.server_port

    def stop_development_server(self):
        self.__development_server.stop()

    @contextmanager
    def start_development_server_in_context(self, host: str = None, port: int = 5000) -> int:
        self.__development_server = DevelopmentServer(self, host, port)
        with self.__development_server.start_in_context() as port:
            yield port

    @staticmethod
    def __check_resource_request_mapping(resources):
        for resource in resources:
            if resource.__request_mapping__ is None:
                raise RestitApp.MissingRequestMappingException(
                    f"The resource class {resource.__class__.__name__} does not appear to have a @request_mapping(...)"
                )

    def _init(self):
        self._resources.append(DefaultFaviconResource())
        if self._open_api_documentation:
            self._resources.append(OpenApiResource(self._open_api_documentation))
        for resource in self._resources:
            resource.init()
            if self._open_api_documentation:
                self._open_api_documentation.register_resource(resource)
        self._init_called = True

    def __call__(self, wsgi_environ: dict, start_response: Callable) -> Iterable:
        if not self._init_called:
            self._init()

        resource, path_params = self._find_resource_for_url(wsgi_environ["PATH_INFO"])
        request = Request(wsgi_environ, path_params)
        response = self._create_response_and_handle_exceptions(path_params, request, resource)
        header_as_list = [(key, str(value)) for key, value in response.get_headers().items()]
        start_response(response.get_status_string(), header_as_list)

        return [response.content]

    def _create_response_and_handle_exceptions(
            self, path_params: dict, request: Request, resource: Resource
    ) -> Response:
        try:
            response = self._get_response_or_raise_not_found(path_params, request, resource)
        except HttpError as error:
            error.traceback = traceback.format_exc()
            response = HttpErrorResponseMaker(error, self._debug).create_response(request.http_accept_object)
        except Exception as error:
            if self._raise_exceptions:
                raise
            LOGGER.error(str(error))
            _traceback = traceback.format_exc()
            LOGGER.error(_traceback)
            internal_server_error = InternalServerError(
                description=f"{error.__class__.__name__}: {error}", traceback=_traceback
            )
            response = HttpErrorResponseMaker(
                internal_server_error, self._debug
            ).create_response(request.http_accept_object)
        return response

    @staticmethod
    def _create_http_exception_response(request: Request, http_exception: HttpError) -> Response:
        exception_response_maker = HttpErrorResponseMaker(http_exception)
        response = exception_response_maker.create_response(request.http_accept_object)
        return response

    @staticmethod
    def _get_response_or_raise_not_found(path_params: dict, request: Request, resource: Resource) -> Response:
        if resource is not None:
            # noinspection PyBroadException
            # noinspection PyProtectedMember
            response = resource.handle_request(
                request_method=request.request_method_name,
                request=request,
                path_params=path_params
            )

        else:
            raise NotFound()
        return response

    @lru_cache()
    def _find_resource_for_url(self, url: str) -> Union[Tuple[None, None], Tuple[Resource, Dict]]:
        for resource in self._resources:
            # noinspection PyProtectedMember
            is_matching, path_params = resource._get_match(url)
            if is_matching:
                return resource, path_params

        return None, None

    class MissingRequestMappingException(Exception):
        pass
