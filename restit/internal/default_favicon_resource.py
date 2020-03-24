from restit._response import Response
from restit.decorator import path
from restit.request import Request
from restit.resource import Resource


@path("/favicon.ico")
class DefaultFaviconResource(Resource):
    def get(self, request: Request, **path_params) -> Response:
        return Response("")
