from enum import Enum


class RequestType(Enum):
    GET = "GET"


class WsgiRequestEnvironment:
    request_method: RequestType = None

    def __init__(self, request_method):
        self.request_method = request_method

    @staticmethod
    def create_from_wsgi_environment_dict(environ: dict) -> "WsgiRequestEnvironment":
        wsgi_request_environment = WsgiRequestEnvironment(
            request_method=RequestType(environ["REQUEST_METHOD"])
        )

        return wsgi_request_environment
