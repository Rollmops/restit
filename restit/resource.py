import inspect
import re
from typing import Tuple, AnyStr, Dict, Union, List

from werkzeug.exceptions import MethodNotAllowed, BadRequest

from restit.internal.resource_path import ResourcePath
from restit.internal.type_converter.string_type_converter import StringTypeConverter
from restit.path_parameter_decorator import PathParameter
from restit.query_parameter_decorator import QueryParameter
from restit.request import Request
from restit.response import Response


class Resource:
    __request_mapping__ = None
    _METHOD_NAMES = ["get", "post", "put", "delete", "patch", "options", "trace", "connect", "head"]

    def __init__(self):
        self._resource_path = None

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
    def delete(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def patch(self, request: Request, **path_params) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def options(self, request: Request, **path_params) -> Response:
        """Identifying allowed request methods.

        The HTTP OPTIONS method is used to describe the communication options for the target resource.
        """
        allow = " ".join(self.get_allowed_methods()).upper()
        return Response("", 204, headers={"Allow": allow})

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
        method_object = getattr(self, request_method.lower())
        passed_path_parameters = self._collect_and_convert_path_parameters(path_params)
        self._process_query_parameters(method_object, request)
        request = self._validate_request_body(method_object, request)
        response = method_object(request, **passed_path_parameters)
        return response

    @staticmethod
    def _validate_request_body(method_object: object, request: Request) -> Request:
        request_body_parameter = getattr(method_object, "__request_body_parameter__", None)
        if request_body_parameter:
            request.set_body_from_string(request_body_parameter.validate(request))

        return request

    @staticmethod
    def _process_query_parameters(method_object, request):
        for query_parameter in getattr(method_object, "__query_parameters__", []):  # type: QueryParameter
            value = request.get_query_parameters().get(query_parameter.name, query_parameter.default)
            if value is None and query_parameter.required:
                # ToDo message
                raise BadRequest()

            # noinspection PyProtectedMember
            request._query_parameters[query_parameter.name] = StringTypeConverter.convert(value, query_parameter.type)

    def _collect_and_convert_path_parameters(self, path_params: dict):
        for path_parameter in getattr(self, "__path_parameters__", []):  # type: PathParameter
            try:
                path_parameter_value = path_params[path_parameter.name]
            except KeyError:
                raise Resource.PathParameterNotFoundException(
                    f"Unable to find {path_parameter} in incoming path parameters {path_params}"
                )
            try:
                path_params[path_parameter.name] = \
                    StringTypeConverter.convert(path_parameter_value, path_parameter.type)
            except ValueError as error:
                raise BadRequest(
                    f"Path parameter value '{path_parameter_value}' is not matching '{path_parameter}' "
                    f"({str(error)})"
                )

        return path_params

    def get_allowed_methods(self) -> List[str]:
        allowed = []
        for method_name in Resource._METHOD_NAMES:
            method_object = getattr(self, method_name)
            resource_method_code = inspect.getsource(method_object)
            match = re.match(
                r"^.+def\s+\w+\(self,\s*request:\s*Request.+\)\s*->\s*Response:.+raise\s+MethodNotAllowed\(\).*$",
                resource_method_code, flags=re.DOTALL | re.IGNORECASE
            )
            if match is None:
                allowed.append(method_name)

        return allowed

    def _get_match(self, url: str) -> Tuple[bool, Union[None, Dict[str, AnyStr]]]:
        assert self._resource_path
        return self._resource_path.get_match(url)

    class PathParameterNotFoundException(Exception):
        pass
