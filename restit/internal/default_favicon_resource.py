from restit.request import Request
from restit.request_mapping_decorator import request_mapping
from restit.resource import Resource
from restit.response import Response


@request_mapping("/favicon.ico")
class DefaultFaviconResource(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response("")
