from enum import Enum


class RequestType(Enum):
    GET = "GET"


class WsgiRequestEnvironment:
    def __init__(self, request_method: RequestType, path: str):
        self.request_method = request_method
        self.path = path

    @staticmethod
    def create_from_wsgi_environment_dict(environ: dict) -> "WsgiRequestEnvironment":
        wsgi_request_environment = WsgiRequestEnvironment(
            request_method=RequestType(environ["REQUEST_METHOD"]),
            path=environ["PATH_INFO"]
        )

        return wsgi_request_environment
