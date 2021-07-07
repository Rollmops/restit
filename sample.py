from restit import Request, Resource, Response, RestItApp
from restit.decorator import path
from restit.open_api import OpenApiDocumentation, InfoObject


@path("/")
class IndexResource(Resource):
    def get(self, request: Request) -> Response:
        return Response("Hello from index.")


app = RestItApp(
    resources=[IndexResource()],
    open_api_documentation=OpenApiDocumentation(info=InfoObject(title="RestIt Sample", version="1.0.0"))
)


if __name__ == "__main__":
    # start a development server on http://127.0.0.1:5000
    app.start_development_server()