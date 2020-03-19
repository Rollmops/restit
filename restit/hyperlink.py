from typing import Type

from restit.internal.resource_path import ResourcePath
from restit.request import Request
from restit.resource import Resource


class Hyperlink:
    def __init__(self, resource_class: Type[Resource]):
        self.resource_class = resource_class

    def generate(self, request: Request, **path_parameter) -> str:
        request_mapping_with_values = \
            ResourcePath.generate_url_with_path_parameter_values(
                self.resource_class.__request_mapping__, path_parameter
            )

        return request.host.rstrip("/") + "/" + request_mapping_with_values.lstrip("/")
