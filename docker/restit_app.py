from restit import Resource, Response, Request, RestItApp, request_mapping


@request_mapping("/")
class MyFirstResource(Resource):
    def get(self, request: Request) -> Response:
        return Response(request.headers)


app = RestItApp(resources=[MyFirstResource()], debug=True)
