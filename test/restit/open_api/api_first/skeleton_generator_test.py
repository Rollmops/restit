import unittest
from typing import Tuple

from restit.open_api.api_first.resource_template import RESOURCE_TEMPLATE


class RestitImports:
    def __init__(self, marshmallow_imports: set, restit_root_imports: set, restit_decorator_imports: set):
        self.marshmallow_imports = marshmallow_imports
        self.restit_root_imports = restit_root_imports
        self.restit_decorator_imports = restit_decorator_imports

    def to_string(self) -> str:
        return_string = f"from restit import {', '.join(list(self.restit_root_imports))}\n" \
                        f"from restit.decorator import {', '.join(list(self.restit_decorator_imports))}"

        if len(self.marshmallow_imports):
            return_string = f"from marshmallow import {', '.join(list(self.marshmallow_imports))}"

        return return_string


class SkeletonGenerator:
    @staticmethod
    def generate(directory_path: str, spec: dict):
        SkeletonGenerator._generate_resources(directory_path, spec)

    @staticmethod
    def _generate_resources(directory_path: str, spec: dict):
        for path, path_spec in spec["paths"].items():
            SkeletonGenerator._generate_resource(path, path_spec)

    @staticmethod
    def _generate_resource(path: str, path_spec: dict):
        restit_imports = RestitImports(set(), {"Resource"}, {"path"})
        resource_class_name = SkeletonGenerator._generate_resource_class_name(path)
        request_methods, restit_imports = SkeletonGenerator._generate_request_methods(
            path_spec, restit_imports, resource_class_name
        )
        resource_string = RESOURCE_TEMPLATE.format(
            path=path,
            resource_class_name=resource_class_name,
            imports=restit_imports.to_string(),
            request_methods=request_methods
        )
        print(resource_string)

    @staticmethod
    def _generate_resource_class_name(path: str) -> str:
        if path == "/":
            return "IndexResource"
        return path.replace("/", " ").title().replace(" ", "") + "Resource"

    @staticmethod
    def _generate_request_methods(
            path_spec: dict, restit_imports: RestitImports, resource_class_name: str) -> Tuple[str, RestitImports]:
        request_method_strings = []
        for request_method, request_spec in path_spec.items():
            restit_imports.restit_root_imports.add("Response")
            restit_imports.restit_root_imports.add("Request")
            restit_imports.restit_decorator_imports.add("response")
            response_decorators = SkeletonGenerator._generate_response_decorator(request_spec.get("responses", {}))

            request_method_string = \
                f"{' ' * 4}{response_decorators}" \
                f"{' ' * 4}def {request_method}(request: Request) -> Response:\n" \
                f"{' ' * 8}\"\"\"{request_spec.get('description', 'No description')}\"\"\"\n" \
                f"{' ' * 8}# ToDo implement {request_method} method in {resource_class_name}\n" \
                f"{' ' * 8}return Response(\"\")\n"
            request_method_strings.append(request_method_string)

        return "\n\n".join(request_method_strings), restit_imports

    @staticmethod
    def _generate_response_decorator(responses: dict) -> str:
        response_decorator = ""
        for status_code, response_spec in responses.items():
            content_types = '{"%s": %s}' % ("application/json", "Wuff")
            response_decorator += f'@response({status_code}, {content_types}, "")\n'

        return response_decorator


class SkeletonGeneratorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = {
            "paths": {
                "/": {
                    "get": {
                        "description": "Index get description",
                        "responses": {
                            200: {
                                "description": "OK status",
                                "content": {
                                    "application/json": {

                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

    def test_generate_skeleton(self):
        SkeletonGenerator.generate("", self.spec)
