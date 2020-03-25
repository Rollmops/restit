import re

from restit.common import create_dict_from_assignment_syntax, get_default_encoding


class MIMEType:
    _REGEX = re.compile(r"^([*a-zA-Z0-9_-]+)/([+*a-zA-Z0-9_-]+)(.+)?$")

    # noinspection PyShadowingBuiltins
    def __init__(self, type: str, subtype: str, quality: float = 1.0, details: dict = None, charset: str = None):
        self.type = type if type != "*" else None
        self.subtype = subtype if subtype != "*" else None
        self.quality = quality
        self.details = details or {}
        self.charset = charset or get_default_encoding()

        if "q" not in self.details and quality != 1.0:
            self.details["q"] = str(quality)

        if self.type is None and self.subtype is not None:
            raise MIMEType.MIMETypeWildcardHierarchyException(type, subtype)

    @staticmethod
    def from_string(mime_type_string: str) -> "MIMEType":
        match = MIMEType._REGEX.match(mime_type_string.strip())
        if not match:
            raise MIMEType.MIMETypeParsingException(mime_type_string)

        details = create_dict_from_assignment_syntax(match.group(3), group_delimiter=";")

        return MIMEType(
            type=match.group(1),
            subtype=match.group(2),
            quality=float(details.get("q", 1)),
            details=details,
            charset=details.get("charset")
        )

    def matches_mime_type_string(self, mime_type_string: str) -> bool:
        _type, _subtype = mime_type_string.split("/")
        matches_type = self.type is None or _type == "*" or self.type == _type
        matches_subtype = self.subtype is None or _subtype == "*" or self.subtype == _subtype

        return matches_type and matches_subtype

    def to_string(self, with_details: bool = False) -> str:
        _to_string = f"{self.type or '*'}/{self.subtype or '*'}"
        if with_details:
            _to_string += ";" + ";".join([f"{key}={value}" for key, value in self.details.items()])

        return _to_string

    def __eq__(self, other: "MIMEType") -> bool:
        return \
            self.type == other.type and \
            self.subtype == other.subtype and \
            self.details == other.details and \
            self.charset == other.charset

    def __gt__(self, other: "MIMEType") -> bool:
        return self.quality > other.quality

    def __str__(self):
        return f"MIMEType(" \
               f"type={self.type}, subtype={self.subtype}, quality={self.quality}, details={self.details})"

    def __repr__(self):
        return str(self)

    class MIMETypeParsingException(Exception):
        pass

    class MIMETypeWildcardHierarchyException(Exception):
        pass
