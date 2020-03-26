import re
from functools import lru_cache
from typing import List, Tuple, Union, Match

from restit.common import get_response_status_parameters_for_method
from restit.internal.request_body_properties import RequestBodyProperties
from restit.internal.response_status_parameter import ResponseStatusParameter
from restit.open_api.info_object import InfoObject
from restit.open_api.open_api_schema_converter import \
    OpenApiSchemaConverter
from restit.resource import PathParameter
from restit.resource import Resource


class OpenApiDocumentation:
    """Class that that is responsible for creating the `OpenApi`_ documentation.

    If you want to create a *OpenApi* documentation, you have to instantiate this class and pass it your
    :class:`~restit.RestItApp`.

    Example:

    .. code-block:: python

        from restit import RestItApp
        from restit.open_api import OpenApiDocumentation, InfoObject, ContactObject, LicenseObject

        open_api_documentation = OpenApiDocumentation(
            info=InfoObject(
                title="First OpenApi Test",
                description="Super description",
                version="1.2.3",
                contact=ContactObject("API Support", "http://www.example.com/support", "support@example.com"),
                license=LicenseObject("Apache 2.0", "https://www.apache.org/licenses/LICENSE-2.0.html"),
                terms_of_service="http://example.com/terms/"
            ),
            path="/some/custom/api/path"
        )

        restit_app = RestItApp(resource=[...], open_api_documentation=open_api_documentation)

        ...

    Once your app is running, you can access ``http://<host>:<port>/some/custom/api/path/`` to see your API
    documentation.

    :param info: Metadata about the API
    :type info: InfoObject
    :param path: The path where the API is served
    :type path: str
    """

    _IGNORE_RESOURCE_CLASS_NAMES = ["DefaultFaviconResource", "OpenApiResource"]
    _SPEC_VERSION = "3.0.0"

    def __init__(self, info: InfoObject, path: str = "/api"):
        self.info = info
        self.path = path
        self._resources: List[Resource] = []
        self._servers = []

    def register_resource(self, resource: Resource):
        """Register a resource that should be documented.

        .. note:: Only use this function if you want to generate the API specification outside your app.

        :param resource: The resource that should be registered
        :type resource: Resource
        """
        if resource not in self._resources and \
                resource.__class__.__name__ not in OpenApiDocumentation._IGNORE_RESOURCE_CLASS_NAMES:
            self._resources.append(resource)

    @lru_cache()
    def generate_spec(self) -> dict:
        """Generate the `OpenApi`_ specification as a dictionary

        .. note:: Only use this function if you want to generate the API specification outside your app.

        :return: The generated specification
        :rtype: dict
        """
        self._resources.sort(key=lambda r: r.__request_mapping__)
        root_spec = self._generate_root_spec()
        self._generate_paths(root_spec)
        return root_spec

    def _generate_paths(self, root_spec: dict):
        paths = root_spec["paths"]
        for resource in self._resources:
            if resource.__request_mapping__:
                self._add_resource(paths, resource, root_spec)

    def _add_resource(self, paths: dict, resource: Resource, root_spec: dict):
        path, inferred_path_parameters = \
            self._infer_path_params_and_open_api_path_syntax(resource.__request_mapping__)
        # noinspection PyTypeChecker
        summary, description = self._get_summary_and_description_from_doc(resource.__doc__)
        paths[path] = {
            "summary": summary,
            "description": description
        }
        for method_name, method_object in self._get_allowed_resource_methods(resource).items():
            paths[path][method_name] = {
                "responses": {},
                "parameters": []
            }

            method_spec = paths[path][method_name]
            self._add_summary_and_description_to_method(method_spec, method_object)
            self._add_path_parameters(method_spec, resource, inferred_path_parameters)
            self._add_query_parameters(method_spec, method_object, root_spec)
            self._add_request_body(method_spec, method_object, root_spec)
            self._add_responses(method_spec, method_object, root_spec)

    @staticmethod
    def _add_responses(method_spec: dict, method_object: object, root_spec: dict):
        response_status_parameters = get_response_status_parameters_for_method(method_object)
        if response_status_parameters:
            for response_status_parameter in response_status_parameters:  # type: ResponseStatusParameter
                method_spec["responses"][response_status_parameter.status or "default"] = {
                    "description": response_status_parameter.description,
                    "content": OpenApiDocumentation._create_content_field(
                        response_status_parameter.content_types, root_spec
                    )
                }

    @staticmethod
    def _add_request_body(method_spec: dict, method_object: object, root_spec: dict):
        request_body_parameter = getattr(
            method_object, "__request_body_properties__", None)  # type: RequestBodyProperties
        if request_body_parameter:
            method_spec["requestBody"] = {
                "description": request_body_parameter.description,
                "required": request_body_parameter.required,
                "content": OpenApiDocumentation._create_content_field(request_body_parameter.content_types, root_spec)
            }

    @staticmethod
    def _create_content_field(content_types: dict, root_spec: dict):
        return {
            content_type:
                {
                    "schema": OpenApiSchemaConverter.convert(schema, root_spec)
                }
            for content_type, schema in content_types.items()
        }

    @staticmethod
    def _add_query_parameters(method_spec: dict, method_object: object, root_spec: dict):
        method_spec["parameters"].extend([
            {
                "name": query_parameter.name,
                "in": "query",
                "description": query_parameter.description,
                "required": query_parameter.field_type.required,
                "schema": OpenApiSchemaConverter.convert(query_parameter.field_type, root_spec)
            }
            for query_parameter in getattr(method_object, "__query_parameters__", [])
        ])

    @staticmethod
    def _add_path_parameters(method_spec: dict, resource: Resource, inferred_path_parameters: List[PathParameter]):
        parameter_definitions = getattr(resource, "__path_parameters__", [])
        path_parameters = {
            path_parameter.name: path_parameter for path_parameter in inferred_path_parameters
        }
        path_parameters.update({
            path_parameter.name: path_parameter for path_parameter in parameter_definitions
        })

        method_spec["parameters"].extend([
            {
                "name": name,
                "in": "path",
                "required": True,
                "description": path_parameter.description,
                "schema": OpenApiSchemaConverter.convert_field(path_parameter.field_type)

            } for name, path_parameter in path_parameters.items()
        ])

    @staticmethod
    def _infer_path_params_and_open_api_path_syntax(path: str) -> Tuple[str, List[PathParameter]]:
        path_parameter_list = []

        def _handle_path_parameter(match: Match) -> str:
            path_parameter_list.append(
                PathParameter(match.group(1), "", eval(match.group(2)) if match.group(2) else str)
            )
            return "{%s}" % match.group(1)

        openapi_path_syntax = re.sub(r":(\w+)(?:<(\w+)>)?", _handle_path_parameter, path)
        return openapi_path_syntax, path_parameter_list

    def _add_summary_and_description_to_method(self, method_spec: dict, method_object: object):
        summary, description = self._get_summary_and_description_from_doc(method_object.__doc__)
        method_spec["summary"] = summary
        method_spec["description"] = description

    @staticmethod
    def _get_summary_and_description_from_doc(doc: str) -> Tuple[Union[str, None], Union[str, None]]:
        if not doc:
            return None, None

        doc_split = doc.split("\n")
        summary = doc_split[0]
        description = "\n".join(doc_split[1:]) if len(doc) > 1 else None
        return summary.strip("\n "), description.strip("\n ")

    @staticmethod
    def _get_allowed_resource_methods(resource: Resource) -> dict:
        allowed_methods_dict = {
            allowed: getattr(resource, allowed) for allowed in resource.get_allowed_methods()
            if allowed not in ["options", "head"]
        }
        return allowed_methods_dict

    def _generate_root_spec(self) -> dict:
        return {
            "openapi": OpenApiDocumentation._SPEC_VERSION,
            "info": self.info.to_dict(),
            "paths": {},
            "components": {
                "schemas": {}
            }
        }
