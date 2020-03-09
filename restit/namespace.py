from functools import lru_cache
from typing import List

from restit.resource import Resource


class Namespace:
    def __init__(self, path: str, resources: List[Resource] = None):
        self.__path = path
        self.__resources: List[Resource] = resources or []

    def register_resources(self, resources: List[Resource]):
        self.__resources.extend(resources)

    @lru_cache(maxsize=1)
    def get_adapted_resources(self) -> List[Resource]:
        for resource in self.__resources:
            resource.__request_mapping__ = self._prepend_path(resource.__request_mapping__)

        return self.__resources

    def _prepend_path(self, url: str) -> str:
        return "/".join([self.__path.rstrip("/"), url.lstrip("/")])
