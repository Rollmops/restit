import logging
import traceback
from contextlib import contextmanager
from functools import lru_cache
from time import time
from typing import Iterable, Callable, List, Tuple, Dict, Union

from restit._response import Response
from restit.development_server import DevelopmentServer
from restit.exception import InternalServerError, NotFound, MissingRequestMappingException
from restit.exception.http_error import HttpError
from restit.internal.default_favicon_resource import DefaultFaviconResource
from restit.internal.http_error_response_maker import HttpErrorResponseMaker
from restit.namespace import Namespace
from restit.open_api.open_api_documentation import OpenApiDocumentation
from restit.open_api.open_api_resource import OpenApiResource
from restit.request import Request
from restit.resource import Resource

LOGGER = logging.getLogger(__name__)


class RestItApp:
    """This class represents your *REST* application and is used to glue everything together.

    Since it is a `WSGI <https://www.python.org/dev/peps/pep-0333/>`_-Application, its instance can be passed to servers
    like `Gunicorn <https://gunicorn.org/>`_.

    :param resources: A list of :class:`Resource` instances
    :type resources: List[Resource]
    :param namespaces: A list of :class:`Namespace` instances
    :type namespaces: List[Namespace]
    :param debug: If set to `True`, you will get a detailed *HTML* stacktrace if an error is raised inside your application
    :type debug: bool
    :param raise_exceptions: If set to `True`, exceptions will not cause error responses but will raise an error
    :type raise_exceptions: bool
    :param open_api_documentation: An instance of :class:`OpenApiDocumentation`. If not set, no
           `OpenApi <https://swagger.io/docs/specification/about/>`_ documentation will be generated.
    :type open_api_documentation: OpenApiDocumentation
    """

    def __init__(
            self, resources: List[Resource] = None,
            namespaces: List[Namespace] = None,
            debug: bool = False,
            raise_exceptions: bool = False,
            open_api_documentation: OpenApiDocumentation = None
    ):
        self._namespaces: List[Namespace] = []
        self._resources: List[Resource] = []
        self.debug = debug
        self.raise_exceptions = raise_exceptions
        self._open_api_documentation = open_api_documentation
        self.register_namespaces(namespaces or [])
        self.register_resources(resources or [])

        self.__development_server: Union[DevelopmentServer, None] = None

        self._init_called = False

    def set_open_api_documentation(self, open_api_documentation: OpenApiDocumentation):
        """Set an instance of :class:`OpenApiDocumentation`.

        If not set, no `OpenApi <https://swagger.io/docs/specification/about/>`_ documenation will be generated.

        Can also be set in the constructor.

        """

        self._open_api_documentation = open_api_documentation

    def register_resources(self, resources: List[Resource]):
        """Register an instance of :class:`Resource` to your application.

        A list of resource instances can also be set in the constructor.
        """

        self.__check_resource_request_mapping(resources)
        self._resources.extend(resources)
        self._resources = Resource.sort_resources(self._resources)

    def register_namespaces(self, namespaces: List[Namespace]):
        for namespace in namespaces:
            self.register_resources(namespace.get_adapted_resources())

    def start_development_server(self, host: str = None, port: int = 5000, blocking: bool = True) -> int:
        """This function starts a development server

        .. warning::

           Do not use the development server in production!

        :param host: The host name, defaults to 127.0.0.1
        :type host: str
        :param port: The port number. If set to 0, the OS will assign a free port number for you. The port number will
            then be returned by that function, defaults to 5000
        :type port: int
        :param blocking: If set to `True`, the function will block. Otherwise, the server will run in a thread and can
            be stopped by calling :func:`stop_development_server`.
        :type blocking: bool
        :return: The port the development server is running on
        :rtype: int
        """

        self.__development_server = DevelopmentServer(self, host, port)
        self.__development_server.start(blocking=blocking)
        return self.__development_server.server.server_port

    def stop_development_server(self) -> None:
        """Stops the development server if started in non blocking mode."""
        self.__development_server.stop()

    @contextmanager
    def start_development_server_in_context(self, host: str = None, port: int = 5000) -> int:
        """Starts a development server in a context.

        Example:

        .. code:: python

            import requests

            from restit import RestitApp, Request, Response, Resource, request_mapping


            @request_mapping("/path")
            class MyResource(Resource):
                def get(self, request: Request) -> Response:
                    return Response("Hello")


            my_restit_app = RestitApp(resources=[MyResource()])

            with my_restit_app.start_development_server_in_context(port=0) as port:
                response = requests.get(f"http://127.0.0.1:{port}/path")
                assert response.status_code == 200
                assert response.text == "Hello"

            # here the development server has stopped


        :param host: The host name, defaults to 127.0.0.1
        :type host: str
        :param port: The port number. If set to 0, the OS will assign a free port number for you. The port number will
            then be returned by that function, defaults to 5000
        :return: The port the development server is running on
        :rtype: int
        """
        self.__development_server = DevelopmentServer(self, host, port)
        with self.__development_server.start_in_context() as port:
            yield port

    @staticmethod
    def __check_resource_request_mapping(resources):
        for resource in resources:
            if resource.__request_mapping__ is None:
                raise MissingRequestMappingException(
                    f"The resource class {resource.__class__.__name__} does not appear to have a @path(...)"
                )

    def _init(self):
        self._resources.append(DefaultFaviconResource())
        if self._open_api_documentation:
            self._resources.append(OpenApiResource(self._open_api_documentation))
        for resource in self._resources:
            resource.init()
            if self._open_api_documentation:
                self._open_api_documentation.register_resource(resource)
        self._resources = Resource.sort_resources(self._resources)
        self._init_called = True

    def __call__(self, wsgi_environ: dict, start_response: Callable) -> Iterable:
        if not self._init_called:
            self._init()
        start_time = time()
        resource, path_params = self._find_resource_for_url(wsgi_environ["PATH_INFO"])
        request = Request(wsgi_environ, path_params)
        LOGGER.debug("Start handling %s request %s", request.request_method_name.upper(), request)
        response = self._create_response_and_handle_exceptions(path_params, request, resource)
        LOGGER.debug("Got response %s", response)
        header_as_list = [(key, str(value)) for key, value in response.headers.items()]
        start_response(response.status_string, header_as_list)
        end_time = time()
        LOGGER.debug("Request processing took %d seconds", (end_time - start_time))
        return [response.content]

    def _create_response_and_handle_exceptions(
            self, path_params: dict, request: Request, resource: Resource
    ) -> Response:
        try:
            response = self._get_response_or_raise_not_found(path_params, request, resource)
        except HttpError as error:
            error.traceback = traceback.format_exc()
            response = HttpErrorResponseMaker(error, self.debug).create_response(request.http_accept_object)
        except Exception as error:
            response = self._get_response_from_common_exception(error, request)
        return response

    def _get_response_from_common_exception(self, error: Exception, request: Request) -> Response:
        if self.raise_exceptions:
            raise error
        LOGGER.error(str(error))
        _traceback = traceback.format_exc()
        LOGGER.error(_traceback)
        internal_server_error = InternalServerError(
            description=f"{error.__class__.__name__}: {error}", traceback=_traceback
        )
        response = HttpErrorResponseMaker(internal_server_error, self.debug).create_response(request.http_accept_object)
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
