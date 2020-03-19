from restit import Resource, Response, Request, RestitApp, request_mapping


@request_mapping("/")
class MyFirstResource(Resource):
    def get(self, request: Request) -> Response:
        return Response(request.headers)


app = RestitApp(resources=[MyFirstResource()], debug=True)
