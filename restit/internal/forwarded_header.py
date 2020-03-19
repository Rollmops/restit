import re
from typing import List, Union


class ForwardedHeader:
    _FOR_REGEX = re.compile(r"for=\"?([\[\]:.a-z0-9]+)\"?", flags=re.IGNORECASE)
    _BY_REGEX = re.compile(r".*by=\"?([\[\]:.a-z0-9]+)\"?.*", flags=re.IGNORECASE)
    _PROTO_REGEX = re.compile(r".*proto=([a-z]+).*", flags=re.IGNORECASE)
    _HOST_REGEX = re.compile(r".*host=([:.a-z0-9-_]+).*", flags=re.IGNORECASE)

    def __init__(
            self, for_list: List[str] = None, by: str = None, host: str = None, proto: str = None, server: str = None
    ):
        self.for_list = for_list or []
        self.by = by
        self.host = host
        self.proto = proto
        self.server = server

    @staticmethod
    def from_string(forwarded_string: str) -> "ForwardedHeader":
        for_directives = ForwardedHeader._FOR_REGEX.findall(forwarded_string)
        by_directive = ForwardedHeader._BY_REGEX.match(forwarded_string)
        by_directive = by_directive.group(1) if by_directive is not None else None

        proto_directive = ForwardedHeader._PROTO_REGEX.match(forwarded_string)
        proto_directive = proto_directive.group(1) if proto_directive is not None else None

        host_directive = ForwardedHeader._HOST_REGEX.match(forwarded_string)
        host_directive = host_directive.group(1) if host_directive is not None else None

        return ForwardedHeader(
            for_list=for_directives,
            by=by_directive,
            proto=proto_directive,
            host=host_directive
        )

    @staticmethod
    def from_headers(headers: dict) -> Union["ForwardedHeader", None]:
        if "Forwarded" in headers:
            return ForwardedHeader.from_string(headers["Forwarded"])
        else:
            return ForwardedHeader(
                host=headers.get("X-Forwarded-Host"),
                for_list=[fs.strip() for fs in headers.get("X-Forwarded-For", "").split(",")],
                proto=headers.get("X-Forwarded-Proto"),
                server=headers.get("X-Forwarded-Server")
            )
