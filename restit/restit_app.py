import logging
import traceback
from contextlib import contextmanager
from functools import lru_cache
from typing import Iterable, Callable, List, Tuple, Dict, Union

# noinspection PyProtectedMember
from werkzeug.exceptions import HTTPException, InternalServerError, NotFound

from restit.development_server import DevelopmentServer
from restit.internal.default_favicon_resource import DefaultFaviconResource
from restit.internal.exception_response_maker import HttpExceptionResponseMaker
from restit.internal.open_api_resource import OpenApiResource
from restit.namespace import Namespace
from restit.open_api_documentation import OpenApiDocumentation
from restit.request import Request
from restit.resource import Resource
from restit.response import Response
from restit.rfc7807_http_problem import Rfc7807HttpProblem

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

    def register_resources(self, resources: List[Resource]):
        self.__check_resource_request_mapping(resources)
        self._resources.extend(resources)
        self._create_url_ordered_resource()

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

        request = Request(wsgi_environ)
        resource, path_params = self._find_resource_for_url(request.get_path())

        response = self._create_response_and_handle_exceptions(path_params, request, resource)

        header_as_list = [(key, str(value)) for key, value in response.get_headers().items()]
        start_response(response.get_status_string(), header_as_list)

        return [response.content]

    def _create_response_and_handle_exceptions(
            self, path_params: dict, request: Request, resource: Resource
    ) -> Response:
        try:
            response = self._get_response_or_raise_not_found(path_params, request, resource)
        except HTTPException as exception:
            rfc7807_http_problem = Rfc7807HttpProblem.from_http_exception(exception)
            response = self._create_rfc7807_response(request, rfc7807_http_problem)
        except Rfc7807HttpProblem as problem:
            response = self._create_rfc7807_response(request, problem)
        except Exception as exception:
            if self._raise_exceptions:
                raise
            LOGGER.error(str(exception))
            LOGGER.error(traceback.format_exc())
            internal_exception = InternalServerError(str(exception) if self._debug else "")
            exception_response_maker = HttpExceptionResponseMaker(
                Rfc7807HttpProblem.from_http_exception(internal_exception)
            )
            response = exception_response_maker.create_response(request.get_accepted_media_types())
        return response

    @staticmethod
    def _create_rfc7807_response(request, rfc7807_http_problem):
        LOGGER.info(str(rfc7807_http_problem))
        exception_response_maker = HttpExceptionResponseMaker(rfc7807_http_problem)
        response = exception_response_maker.create_response(request.get_accepted_media_types())
        return response

    @staticmethod
    def _get_response_or_raise_not_found(path_params: dict, request: Request, resource: Resource) -> Response:
        if resource is not None:
            # noinspection PyBroadException
            # noinspection PyProtectedMember
            response = resource._handle_request(
                request_method=request.get_request_method_name(),
                request=request,
                path_params=path_params
            )
            response.serialize_response_body(request.get_accepted_media_types())
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

    def _create_url_ordered_resource(self):
        self._resources = sorted(self._resources, key=lambda r: r.__request_mapping__, reverse=True)

    class MissingRequestMappingException(Exception):
        pass
