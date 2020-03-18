from typing import Union

from .http_error_css import _ERROR_BOOTSTRAP_CSS

_DEBUG_HTML_TEMPLATE = """<html>
<head>
<style>
{css}
</style>
</head>
<title>{status_code} {title}</title>
<body>
<br><br>
<div class="container">
<h1>{title}</h1>
<br>
<br>
<div class="alert alert-danger" role="alert">{description}</div>
<br>
<div class="jumbotron">
<pre><code>{traceback}</code></pre>
</div>
<h5>Get more information about this error <a href={rfc7807_type}>here</a></a></h5>
</div>
<body>
</html>
"""

_HTML_TEMPLATE = """<title>{status_code} {title}</title>
<h1>{title}</h1>
<p>{description}</p>
"""


class HttpError(RuntimeError):
    STATUS_CODE: Union[int, None] = None
    TITLE: Union[str, None] = None
    DEFAULT_DESCRIPTION: Union[str, None] = None
    DEFAULT_RFC7807_TYPE: Union[str, None] = "about:blank"

    def __init__(
            self,
            description: str = None,
            traceback: str = None,
            rfc7807_type: str = None,
            rfc7807_instance: str = None
    ):
        self.description = description or self.DEFAULT_DESCRIPTION
        self.traceback = traceback
        self.rfc7807_type = rfc7807_type or self.DEFAULT_RFC7807_TYPE
        self.rfc7807_instance = rfc7807_instance

    @property
    def status_code(self) -> int:
        return self.STATUS_CODE

    def to_rfc7807_json(self) -> dict:
        """https://tools.ietf.org/html/rfc7807
        https://tools.ietf.org/html/rfc7807#section-3.1
        """
        return {
            "type": self.rfc7807_type,
            "title": self.TITLE,
            "status": self.STATUS_CODE,
            "detail": self.description,
            "instance": self.rfc7807_instance
        }

    def to_html(self, debug: bool = False) -> str:
        if debug:
            html_string = _DEBUG_HTML_TEMPLATE.format(
                title=self.TITLE,
                status_code=self.STATUS_CODE,
                description=self.description.strip("\n "),
                traceback=self.traceback.replace("\n", "<br>"),
                css=_ERROR_BOOTSTRAP_CSS,
                rfc7807_type=self.rfc7807_type
            )
        else:
            html_string = _HTML_TEMPLATE.format(
                title=self.TITLE,
                status_code=self.STATUS_CODE,
                description=self.description.strip("\n "),
            )

        return html_string

    def to_text(self, debug: bool = False) -> str:
        traceback_suffix = "\n\n{self.traceback if debug else ''}" if debug else ""
        return f"{self.STATUS_CODE} {self.TITLE}: {self.description}{traceback_suffix}"
