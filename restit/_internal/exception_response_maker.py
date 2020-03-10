from werkzeug.datastructures import MIMEAccept
from werkzeug.exceptions import HTTPException

from restit.response import Response


class ExceptionResponseMaker:
    HTML_TEMPLATE = """<title>{code} {name}</title>
<h1>{name}</h1>
<p>{description}</p>
"""

    def __init__(self, http_exception: HTTPException):
        self.http_exception = http_exception

    def create_response(self, accept: MIMEAccept) -> Response:
        if accept.accept_html:
            response = self.create_html_response()
        elif accept.accept_json:
            response = self.create_json_response()
        else:
            response = self.create_plain_text_response()

        response.set_body_as_bytes(accept)
        return response

    def create_html_response(self) -> Response:
        html_text = ExceptionResponseMaker.HTML_TEMPLATE.format(
            code=self.http_exception.code,
            name=self.http_exception.name,
            description=self.http_exception.description
        )
        response = Response(html_text, status_code=self.http_exception.code)
        return response

    def create_json_response(self) -> Response:
        response_dict = {
            "code": self.http_exception.code,
            "name": self.http_exception.name,
            "description": self.http_exception.description
        }
        response = Response(response_dict, self.http_exception.code)
        return response

    def create_plain_text_response(self) -> Response:
        return Response(
            f"{self.http_exception.name}: {self.http_exception.description} ({self.http_exception.code})",
            self.http_exception.code
        )
