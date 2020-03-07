from werkzeug.exceptions import NotFound

from restit._internal.wsgi_request_environment import RequestType
from restit.request import Request
from restit.response import Response


class Resource:
    def get(self, request: Request) -> Response:
        raise NotFound()

    def _handle_request(self, request_method: RequestType, request: Request) -> Response:
        return {
            RequestType.GET: self.get
        }[request_method](request)
