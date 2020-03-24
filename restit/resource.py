import ast
import inspect
import logging
import re
from typing import Tuple, AnyStr, Dict, Union, List, Callable

from marshmallow import ValidationError

from restit._path_parameter import PathParameter
from restit._response import Response
from restit.common import get_response_status_parameters_for_method, get_exception_mapping_for_method
from restit.exception import MethodNotAllowed
from restit.exception.client_errors_4xx import BadRequest
from restit.internal.query_parameter import QueryParameter
from restit.internal.request_body_properties import RequestBodyProperties
from restit.internal.request_body_schema_deserializer import RequestBodySchemaDeserializer
from restit.internal.resource_path import ResourcePath
from restit.internal.response_serializer_service import ResponseSerializerService
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.internal.schema_or_field_deserializer import SchemaOrFieldDeserializer
from restit.request import Request

LOGGER = logging.getLogger(__name__)


class Resource:
    """Base class you have to inherit from when implementing your resource.

    It provides the interface for all `HTTP request methods <https://developer.mozilla.org/de/docs/Web/HTTP/Methods>`_
    and implicit implementation for the `OPTIONS <https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS>`_
    method.

    If an *HTTP* method is not implemented but requested by the client, a :class:`~restit.exception.MethodNotAllowed`
    error will be raised leading to a `405 <https://developer.mozilla.org/de/docs/Web/HTTP/Status/405>`_
    response status code on the client.

    .. note::

        You have to map your resource with an *URI* using the :func:`request_mapping` decorator.

    """

    __request_mapping__ = None
    _METHOD_NAMES = ["get", "post", "put", "delete", "patch", "options", "trace", "connect", "head"]

    def __init__(self):
        self._resource_path = None

    def init(self):
        self._resource_path = ResourcePath(self.__request_mapping__)

    def get(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def put(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def delete(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def patch(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def options(self, request: Request) -> Response:
        """Identifying allowed request methods.

        The HTTP OPTIONS method is used to describe the communication options for the target resource.
        """
        allow = " ".join(self.get_allowed_methods()).upper()
        return Response("", 204, headers={"Allow": allow})

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def trace(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def connect(self, request: Request) -> Response:
        raise MethodNotAllowed()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def head(self, request: Request) -> Response:
        raise MethodNotAllowed()

    def handle_request(self, request_method: str, request: Request, path_params: Dict) -> Response:
        method_object = getattr(self, request_method.lower())
        request._path_params = self._collect_and_convert_path_parameters(path_params)
        self._process_query_parameters(method_object, request)
        request = self._validate_request_body(method_object, request)
        response: Response = self._execute_request_with_exception_mapping(method_object, request)
        if not isinstance(response, Response):
            raise Resource.NoResponseReturnException(
                f"Resource method {method_object} does not return a response object"
            )
        response_status_parameter = Resource._find_response_schema_by_status(response.status_code, method_object)
        ResponseSerializerService.validate_and_serialize_response_body(
            response, request.http_accept_object, response_status_parameter
        )
        return response

    @staticmethod
    def _execute_request_with_exception_mapping(method_object: Callable, request: Request) -> Response:
        exception_mapping = get_exception_mapping_for_method(method_object)
        try:
            return method_object(request)
        except Exception as exception:
            for source_exception_class, target_exception_tuple_or_class in exception_mapping.items():
                if isinstance(exception, source_exception_class):
                    if isinstance(target_exception_tuple_or_class, tuple):
                        LOGGER.debug(
                            "Mapping exception class %s to %s with description: %s",
                            type(exception), target_exception_tuple_or_class[0], target_exception_tuple_or_class[1]
                        )
                        raise target_exception_tuple_or_class[0](target_exception_tuple_or_class[1])
                    else:
                        LOGGER.debug(
                            "Mapping exception class %s to %s", type(exception), target_exception_tuple_or_class
                        )
                        raise target_exception_tuple_or_class(str(exception))

            raise exception

    @staticmethod
    def _find_response_schema_by_status(status: int, method_object: object) -> Union[None, ResponseStatusParameter]:
        response_status_parameters = get_response_status_parameters_for_method(method_object)
        if response_status_parameters:
            for response_status_parameter in response_status_parameters:  # type: ResponseStatusParameter
                if response_status_parameter.status == status:
                    return response_status_parameter

            LOGGER.warning("Response status code %d is not expected for %s", status, method_object)

    @staticmethod
    def _validate_request_body(method_object: object, request: Request) -> Request:
        request_body_properties: RequestBodyProperties = \
            getattr(method_object, "__request_body_properties__", None)
        if request_body_properties:
            RequestBodySchemaDeserializer.deserialize(request, request_body_properties)

        return request

    @staticmethod
    def _process_query_parameters(method_object: object, request: Request):
        for query_parameter in getattr(method_object, "__query_parameters__", []):  # type: QueryParameter
            value: str = request.query_parameters.get(query_parameter.name, )
            if value is None and query_parameter.field_type.required:
                # ToDo message
                raise BadRequest()

            if value is not None:
                value = ast.literal_eval(value) if value.startswith("[") else value
            # noinspection PyProtectedMember
            request._query_parameters[query_parameter.name] = SchemaOrFieldDeserializer.deserialize(
                value, query_parameter.field_type
            )

    def _collect_and_convert_path_parameters(self, path_params: dict) -> dict:
        for path_parameter in getattr(self, "__path_parameters__", []):  # type: PathParameter
            try:
                path_parameter_value = path_params[path_parameter.name]
            except KeyError:
                raise Resource.PathParameterNotFoundException(
                    f"Unable to find {path_parameter} in incoming path parameters {path_params}"
                )
            try:
                path_params[path_parameter.name] = \
                    SchemaOrFieldDeserializer.deserialize(path_parameter_value, path_parameter.field_type)
            except ValidationError as error:
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
                r"^.+def\s+\w+\(self,\s*request:\s*Request\s*\)\s*->\s*Response:.+raise\s+MethodNotAllowed\(\).*$",
                resource_method_code, flags=re.DOTALL | re.IGNORECASE
            )
            if match is None:
                allowed.append(method_name)

        return allowed

    def _get_match(self, url: str) -> Tuple[bool, Union[None, Dict[str, AnyStr]]]:
        assert self._resource_path
        return self._resource_path.get_match(url)

    @staticmethod
    def sort_resources(resources: List["Resource"]) -> List["Resource"]:
        def key_function(resource: Resource):
            return resource.__request_mapping__.count("/"), resource.__request_mapping__.count(":") * -1

        return sorted(resources, key=key_function, reverse=True)

    class PathParameterNotFoundException(Exception):
        pass

    class NoResponseReturnException(Exception):
        pass
