import unittest

from restit.internal.http_accept import HttpAccept
from restit.internal.mime_type import MIMEType


class HttpAcceptTestCase(unittest.TestCase):
    def test_create_http_accept_from_string(self):
        http_accept_string = \
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,' \
            '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

        http_accept = HttpAccept.from_accept_string(http_accept_string)
        self.assertEqual(7, len(http_accept.mime_types))
        self.assertEqual(MIMEType("text", "html"), http_accept.mime_types[0])
        self.assertEqual(MIMEType("application", "xhtml+xml"), http_accept.mime_types[1])
        self.assertEqual(MIMEType("image", "webp"), http_accept.mime_types[2])
        self.assertEqual(MIMEType("image", "apng"), http_accept.mime_types[3])
        self.assertEqual(MIMEType("application", "xml", 0.9, {"q": "0.9"}), http_accept.mime_types[4])
        self.assertEqual(MIMEType(
            "application", "signed-exchange", 0.9, {"v": "b3", "q": "0.9"}), http_accept.mime_types[5]
        )
        self.assertEqual(MIMEType("*", "*", 0.8, {"q": "0.8"}), http_accept.mime_types[6])

    def test_get_best_match(self):
        http_accept = HttpAccept([
            MIMEType("application", "json", 0.8),
            MIMEType("application", "xml", 0.9),
        ])

        self.assertEqual(
            ("application/xml", MIMEType("application", "xml", 0.9)),
            http_accept.get_best_match(["application/json", "application/xml"])
        )

    def test_get_best_match_wildcard(self):
        http_accept = HttpAccept([
            MIMEType("text", "*"),
            MIMEType("application", "xml"),
        ])

        self.assertEqual(
            ("text/html", MIMEType("text", "*")),
            http_accept.get_best_match(["text/html", "application/json"])
        )

    def test_get_best_match_wildcard_in_input(self):
        http_accept = HttpAccept([
            MIMEType("text", "html"),
            MIMEType("application", "xml", 0.9),
        ])

        self.assertEqual(
            ("text/*", MIMEType("text", "html")),
            http_accept.get_best_match(["text/*", "application/xml"])
        )

    def test_str_hook(self):
        http_accept = HttpAccept([MIMEType("text", "html")])

        self.assertEqual(
            "HttpAccept(['MIMEType(type=text, subtype=html, quality=1.0, details={})'])", str(http_accept)
        )
