from functools import lru_cache
from typing import Iterable, Callable, List

from restit._internal.default_404_resource import Default404Resource
from restit._internal.wsgi_request_environment import WsgiRequestEnvironment
from restit.request import Request
from restit.resource import Resource


class RestitApp:
    def __init__(self, resources: List[Resource] = None):
        self.__resources = resources or []
        self._create_url_ordered_resource()

    def register_resources(self, resources: List[Resource]):
        self.__resources.extend(resources)
        self._create_url_ordered_resource()

    def __call__(self, environ: dict, start_response: Callable) -> Iterable:
        wsgi_request_environment = WsgiRequestEnvironment.create_from_wsgi_environment_dict(environ)

        resource = self._find_resource_for_url(wsgi_request_environment.path)

        request = Request()

        response = resource._handle_request(
            request_method=wsgi_request_environment.request_method,
            request=request
        )

        response_body_as_bytes = response.get_body_as_bytes()
        response.adapt_header()

        header_as_list = [(key, value) for key, value in response.header.items()]

        start_response(response.get_status(), header_as_list)

        return [response_body_as_bytes]

    @lru_cache()
    def _find_resource_for_url(self, url: str) -> Resource:
        for resource in self.__resources:
            if resource.matches_url(url):
                return resource

        return Default404Resource()

    def _create_url_ordered_resource(self):
        self.__resources = sorted(self.__resources, key=lambda r: r.__url__, reverse=True)
