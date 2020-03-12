from collections import namedtuple, defaultdict
from typing import Tuple, AnyStr, Dict, Union

from werkzeug import Request
from werkzeug.exceptions import MethodNotAllowed, BadRequest

from restit.internal.resource_path import ResourcePath
from restit.response import Response

PathParameter = namedtuple("PathParameter", ["name", "type", "description", "format"])

_PATH_PARAMETER_MAPPING = defaultdict(dict)


class Resource:
    __request_mapping__ = None

    def __init__(self):
        self._resource_path = None

    @classmethod
    def add_path_parameter(cls, path_parameter: PathParameter):
        _PATH_PARAMETER_MAPPING[cls][path_parameter.name] = path_parameter

    @classmethod
    def get_path_parameters(cls) -> dict:
        return _PATH_PARAMETER_MAPPING[cls]

    def init(self):
        self._resource_path = ResourcePath(self.__request_mapping__)

    def get(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def put(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def delete(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def patch(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def options(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def trace(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def connect(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def head(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    def _handle_request(self, request_method: str, request: Request, path_params: Dict) -> Response:
        method = getattr(self, request_method.lower())

        passed_path_parameters = self._collect_and_convert_path_parameters(path_params)

        return method(request, **passed_path_parameters)

    def _collect_and_convert_path_parameters(self, path_params: dict):
        for path_parameter in _PATH_PARAMETER_MAPPING[self.__class__].values():
            try:
                path_parameter_value = path_params[path_parameter.name]
            except KeyError:
                raise Resource.PathParameterNotFoundException(
                    f"Unable to find {path_parameter} in incoming path parameters {path_params}"
                )
            try:
                path_params[path_parameter.name] = path_parameter.type(path_parameter_value)
            except ValueError as error:
                raise BadRequest(
                    f"Path parameter value '{path_parameter_value}' is not matching '{path_parameter}' "
                    f"({str(error)})"
                )

        return path_params

    def _get_match(self, url: str) -> Tuple[bool, Union[None, Dict[str, AnyStr]]]:
        assert self._resource_path
        return self._resource_path.get_match(url)

    class PathParameterNotFoundException(Exception):
        pass
