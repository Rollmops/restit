from restit._response import Response
from restit.exception.http_error import HttpError
from restit.internal.http_accept import HttpAccept
from restit.internal.response_serializer_service import ResponseSerializerService


class HttpErrorResponseMaker:

    def __init__(self, http_error: HttpError, debug: bool = False):
        self.http_error = http_error
        self.debug = debug

    def create_response(self, http_accept: HttpAccept) -> Response:
        supported_media_types = [
            "text/html", "application/xhtml+xml", "application/json", "application/problem+json"
        ]
        best_match = http_accept.get_best_match(supported_media_types)
        if best_match is None:
            response = self.create_plain_text_response()
        else:
            best_match = best_match[0]

            if best_match in ["text/html", "application/xhtml+xml"]:
                response = self.create_html_response()
            else:
                response = self.create_rfc7807_json_response()

        ResponseSerializerService.validate_and_serialize_response_body(response, http_accept, None)
        return response

    def create_html_response(self) -> Response:
        response = Response(
            response_body=self.http_error.to_html(self.debug),
            status_code=self.http_error.status_code,
            headers={"Content-Type": "text/html"}
        )
        return response

    def create_rfc7807_json_response(self) -> Response:
        """https://tools.ietf.org/html/rfc7807
        https://tools.ietf.org/html/rfc7807#section-3.1
        """
        response = Response(
            response_body=self.http_error.to_rfc7807_json(),
            status_code=self.http_error.status_code,
            headers={"Content-Type": "application/problem+json"}
        )
        return response

    def create_plain_text_response(self) -> Response:
        return Response(
            response_body=self.http_error.to_text(self.debug),
            status_code=self.http_error.status_code
        )
