from functools import lru_cache
from http import HTTPStatus
from typing import Iterable, Callable, List, Tuple, Dict, Union

# noinspection PyProtectedMember
from restit._internal.wsgi_request_environment import WsgiRequestEnvironment
from restit.namespace import Namespace
from restit.request import Request
from restit.resource import Resource
from restit.response import Response


class RestitApp:
    def __init__(
            self, resources: List[Resource] = None,
            namespaces: List[Namespace] = None
    ):
        self.__namespaces: List[Namespace] = []
        self.__resources: List[Resource] = []
        self.register_namespaces(namespaces or [])
        self.register_resources(resources or [])

        self.__init_called = False

    def register_resources(self, resources: List[Resource]):
        self._check_resource_request_mapping(resources)
        self.__resources.extend(resources)
        self._create_url_ordered_resource()

    def _check_resource_request_mapping(self, resources):
        for resource in resources:
            if resource.__url__ is None:
                raise RestitApp.MissingRequestMappingException(resource)

    def register_namespaces(self, namespaces: List[Namespace]):
        for namespace in namespaces:
            self.register_resources(namespace.get_adapted_resources())

    def __init(self):
        for resource in self.__resources:
            resource.init()
        self.__init_called = True

    def __call__(self, environ: dict, start_response: Callable) -> Iterable:
        if not self.__init_called:
            self.__init()

        wsgi_request_environment = WsgiRequestEnvironment.create_from_wsgi_environment_dict(environ)

        resource, path_params = self._find_resource_for_url(wsgi_request_environment.path)

        request = Request(
            query_parameters=wsgi_request_environment.query_parameters,
            wsgi_environment=wsgi_request_environment.wsgi_environment,
            body=wsgi_request_environment.body
        )
        response = self._get_response(path_params, request, resource, wsgi_request_environment)

        response_body_as_bytes = response.get_body_as_bytes()
        response.adapt_header()

        header_as_list = [(key, value) for key, value in response.header.items()]

        start_response(response.get_status(), header_as_list)

        return [response_body_as_bytes]

    @staticmethod
    def _get_response(path_params, request, resource, wsgi_request_environment) -> Response:
        if resource is not None:
            # noinspection PyBroadException
            try:
                # noinspection PyProtectedMember
                response = resource._handle_request(
                    request_method=wsgi_request_environment.request_method,
                    request=request,
                    path_params=path_params
                )
            except Exception:
                response = Response.from_http_status(HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            response = Response.from_http_status(HTTPStatus.NOT_FOUND)
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
        self.__resources = sorted(self.__resources, key=lambda r: r.__url__, reverse=True)

    class MissingRequestMappingException(Exception):
        pass
