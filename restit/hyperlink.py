from typing import Type, Union

from restit.internal.resource_path import ResourcePath
from restit.request import Request
from restit.resource import Resource


class Hyperlink:
    def __init__(self, resource_class_or_path: Union[str, Type[Resource]], request: Request):
        if isinstance(resource_class_or_path, str):
            self._path = resource_class_or_path
        else:
            self._path = resource_class_or_path.__request_mapping__
        self.request = request

    def generate(self, **path_parameter) -> str:
        request_mapping_with_values = \
            ResourcePath.generate_url_with_path_parameter_values(self._path, path_parameter)

        return self.request.host.rstrip("/") + "/" + request_mapping_with_values.lstrip("/")
