from restit.request import Request
from restit.resource import Resource
from restit.response import Response


class Default404Resource(Resource):
    def get(self, request: Request) -> Response:
        return Response("Not found", status_code=404)
