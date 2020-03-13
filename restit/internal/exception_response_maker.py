from werkzeug.datastructures import MIMEAccept

from restit.response import Response
from restit.rfc7807_http_problem import Rfc7807HttpProblem


class HttpExceptionResponseMaker:
    HTML_TEMPLATE = """<title>{code} {name}</title>
<h1>{name}</h1>
<p>{description}</p>
"""

    def __init__(self, rfc7807_http_problem: Rfc7807HttpProblem):
        self.rfc7807_http_problem = rfc7807_http_problem

    def create_response(self, media_type: MIMEAccept) -> Response:
        supported_media_types = [
            "text/html", "application/xhtml+xml", "application/json", "text/plain", "application/problem+json"
        ]
        best_match = media_type.best_match(supported_media_types)

        if best_match in ["text/html", "application/xhtml+xml"]:
            response = self.create_html_response()
        elif best_match in ["application/json", "application/problem+json"]:
            response = self.create_rfc7807_json_response()
        else:
            response = self.create_plain_text_response()

        response.serialize_response_body(media_type)
        return response

    def create_html_response(self) -> Response:
        html_text = HttpExceptionResponseMaker.HTML_TEMPLATE.format(
            code=self.rfc7807_http_problem.status,
            name=self.rfc7807_http_problem.title,
            description=self.rfc7807_http_problem.detail
        )
        response = Response(
            response_body=html_text,
            status_code=self.rfc7807_http_problem.status,
            headers={"Content-Type": "text/html"}
        )
        return response

    def create_rfc7807_json_response(self) -> Response:
        """https://tools.ietf.org/html/rfc7807
        https://tools.ietf.org/html/rfc7807#section-3.1
        """
        response = Response(
            response_body=self.rfc7807_http_problem.to_json(),
            status_code=self.rfc7807_http_problem.status,
            headers={"Content-Type": "application/problem+json"}
        )
        return response

    def create_plain_text_response(self) -> Response:
        return Response(
            response_body=str(self.rfc7807_http_problem),
            status_code=self.rfc7807_http_problem.status
        )
