from restit import Response, Request
from restit.common import get_open_api_resource_path
from restit.internal.open_api.open_api_spec import OpenApiSpec
from restit.static_directory_resource import StaticDirectoryResource


class OpenApiResource(StaticDirectoryResource):
    def __init__(self, open_api_spec: OpenApiSpec, path: str = "/api"):
        self.open_api_spec = open_api_spec
        super().__init__(path, get_open_api_resource_path())

    def get(self, request: Request, **path_params) -> Response:
        if path_params["file_name"] == "swagger.json":
            return Response(self.open_api_spec.generate())

        return super().get(request, **path_params)
