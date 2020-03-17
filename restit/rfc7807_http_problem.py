from werkzeug.exceptions import HTTPException


class Rfc7807HttpProblem(Exception):
    def __init__(self, title: str, detail: str, status: int, instance: str = None, type: str = "about:blank"):
        self.title = title
        self.detail = detail
        self.status = status
        self.instance = instance
        self.type = type

    @staticmethod
    def from_http_exception(http_exception: HTTPException) -> "Rfc7807HttpProblem":
        return Rfc7807HttpProblem(
            title=http_exception.name,
            detail=http_exception.description,
            status=http_exception.code
        )

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "detail": self.detail,
            "status": self.status,
            "instance": self.instance,
            "type": self.type
        }

    def __str__(self):
        return f"{self.status} {self.title}: {self.detail} ({self.instance}, {self.type})"
