import unittest

from restit.internal.forwarded_header import ForwardedHeader


class ForwardedHeaderFieldTestCase(unittest.TestCase):
    def test_parse_forwarded_for_ipv4_addresses(self):
        full_syntax = "for=192.0.2.43, for=198.51.100.17:1234"
        forwarded_header = ForwardedHeader.from_string(full_syntax)

        self.assertIn("192.0.2.43", forwarded_header.for_list)
        self.assertIn("198.51.100.17:1234", forwarded_header.for_list)

    def test_parse_forwarded_for_ipv6_addresses(self):
        full_syntax = 'For="[2001:db8:cafe::17]:4711", For="[2002:db8:cafe::17]:4712"'
        forwarded_header = ForwardedHeader.from_string(full_syntax)

        self.assertEqual("[2001:db8:cafe::17]:4711", forwarded_header.for_list[0])
        self.assertEqual("[2002:db8:cafe::17]:4712", forwarded_header.for_list[1])

    def test_parse_for_mixed_ipv4_and_ipv6(self):
        forwarded_header = ForwardedHeader.from_string('for=192.0.2.43, for="[2001:db8:cafe::17]"')

        self.assertEqual("192.0.2.43", forwarded_header.for_list[0])
        self.assertEqual("[2001:db8:cafe::17]", forwarded_header.for_list[1])

        self.assertEqual("192.0.2.43", forwarded_header.for_list[0])
        self.assertEqual("[2001:db8:cafe::17]", forwarded_header.for_list[1])

    def test_complete(self):
        forwarded_header = ForwardedHeader.from_string("for=192.0.2.60;proto=http;by=203.0.113.43")

        self.assertEqual(["192.0.2.60"], forwarded_header.for_list)
        self.assertEqual("203.0.113.43", forwarded_header.by)
        self.assertEqual("http", forwarded_header.proto)

    def test_complete2(self):
        forwarded_header = ForwardedHeader.from_string(
            "for=12.34.56.78;host=example.com:8080;proto=https, for=23.45.67.89"
        )

        self.assertEqual(["12.34.56.78", "23.45.67.89"], forwarded_header.for_list)
        self.assertEqual("https", forwarded_header.proto)
        self.assertEqual("example.com:8080", forwarded_header.host)

    def test_from_headers(self):
        headers = {
            "X-Forwarded-For": "12.34.56.78, 23.45.67.89",
            "X-Forwarded-Host": "example.com",
            "X-Forwarded-Proto": "https"
        }

        forwarded_header = ForwardedHeader.from_headers(headers)

        self.assertEqual("https", forwarded_header.proto)
        self.assertEqual(['12.34.56.78', '23.45.67.89'], forwarded_header.for_list)
        self.assertEqual('example.com', forwarded_header.host)

    def test_from_headers_forwarded(self):
        headers = {
            "Forwarded": "for=12.34.56.78;host=example.com;proto=https, for=23.45.67.89"
        }
        forwarded_header = ForwardedHeader.from_headers(headers)
        self.assertEqual(["12.34.56.78", "23.45.67.89"], forwarded_header.for_list)
        self.assertEqual("https", forwarded_header.proto)
        self.assertEqual("example.com", forwarded_header.host)
