from restit.common import get_open_api_resource_path
from restit.open_api.open_api_documentation import OpenApiDocumentation
from restit.request import Request
from restit.response import Response
from restit.static_directory_resource import StaticDirectoryResource


class OpenApiResource(StaticDirectoryResource):
    def __init__(self, open_api_documentation: OpenApiDocumentation):
        self.open_api_documentation = open_api_documentation
        super().__init__(open_api_documentation.path, get_open_api_resource_path())

    def get(self, request: Request, **path_params) -> Response:
        if path_params["file_name"] == "swagger.json":
            return Response(self.open_api_documentation.generate_spec())

        return super().get(request, **path_params)
