from restit import Resource, Response, Request, request_mapping


@request_mapping("/favicon.ico")
class DefaultFaviconResource(Resource):
    def get(self, request: Request) -> Response:
        return Response("")
