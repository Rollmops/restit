import re

from restit.resource import Resource


class ResourceMapping:
    def __init__(self, url: str, resource: Resource):
        self.url = url
        self.resource = resource
        self.__url_regex = re.compile(url)

    def matches_url(self, url: str) -> bool:
        return self.__url_regex.match(url) is not None
