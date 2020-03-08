from functools import lru_cache
from http import HTTPStatus
from typing import Iterable, Callable, List, Tuple, Dict, Union

from restit._internal.wsgi_request_environment import WsgiRequestEnvironment
from restit.request import Request
from restit.resource import Resource
from restit.response import Response


class RestitApp:
    def __init__(self, resources: List[Resource] = None):
        self.__resources: List[Resource] = resources or []
        self._create_url_ordered_resource()

    def register_resources(self, resources: List[Resource]):
        self.__resources.extend(resources)
        self._create_url_ordered_resource()

    def __call__(self, environ: dict, start_response: Callable) -> Iterable:
        wsgi_request_environment = WsgiRequestEnvironment.create_from_wsgi_environment_dict(environ)

        resource, path_params = self._find_resource_for_url(wsgi_request_environment.path)

        request = Request()
        response = self._get_response(path_params, request, resource, wsgi_request_environment)

        response_body_as_bytes = response.get_body_as_bytes()
        response.adapt_header()

        header_as_list = [(key, value) for key, value in response.header.items()]

        start_response(response.get_status(), header_as_list)

        return [response_body_as_bytes]

    @staticmethod
    def _get_response(path_params, request, resource, wsgi_request_environment):
        if resource is not None:
            response = resource._handle_request(
                request_method=wsgi_request_environment.request_method,
                request=request,
                path_params=path_params
            )
        else:
            response = Response.from_http_status(HTTPStatus.NOT_FOUND)
        return response

    @lru_cache()
    def _find_resource_for_url(self, url: str) -> Union[Tuple[None, None], Tuple[Resource, Dict]]:
        for resource in self.__resources:
            is_matching, path_params = resource.get_match(url)
            if is_matching:
                return resource, path_params

        return None, None

    def _create_url_ordered_resource(self):
        self.__resources = sorted(self.__resources, key=lambda r: r.__url__, reverse=True)
