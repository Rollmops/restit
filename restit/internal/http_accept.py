from typing import List, Tuple, Union

from restit.internal.mime_type import MIMEType


class HttpAccept:
    def __init__(self, mime_types: List[MIMEType]):
        self.mime_types: List[MIMEType] = sorted(mime_types, reverse=True)

    @staticmethod
    def from_accept_string(accept_string: str) -> "HttpAccept":
        return HttpAccept(
            [
                MIMEType.from_string(mime_type_string)
                for mime_type_string in accept_string.split(",")
            ]
        )

    def get_best_match(self, mime_type_strings: List[str]) -> Union[None, Tuple[str, MIMEType]]:
        for mime_type in self.mime_types:
            for mime_type_string in mime_type_strings:
                if mime_type.matches_mime_type_string(mime_type_string):
                    return mime_type_string, mime_type

    def __str__(self):
        return f"HttpAccept({[str(m) for m in self.mime_types]})"

    def __eq__(self, other: "HttpAccept") -> bool:
        return self.mime_types == other.mime_types
