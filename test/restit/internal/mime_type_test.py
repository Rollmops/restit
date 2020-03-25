import unittest

from restit.internal.mime_type import MIMEType


class MIMETypeTestCase(unittest.TestCase):
    def test_create_from_string(self):
        mime_type_string = "application/signed-exchange+xml;v=b3;q=0.9"
        mime_type = MIMEType.from_string(mime_type_string)

        self.assertEqual("application", mime_type.type)
        self.assertEqual("signed-exchange+xml", mime_type.subtype)
        self.assertEqual(0.9, mime_type.quality)
        self.assertEqual("b3", mime_type.details["v"])

    def test_create_from_string_without_details(self):
        mime_type_string = "text/html"
        mime_type = MIMEType.from_string(mime_type_string)

        self.assertEqual("text", mime_type.type)
        self.assertEqual("html", mime_type.subtype)
        self.assertEqual(1.0, mime_type.quality)
        self.assertEqual({}, mime_type.details)

    def test_parse_wildcard(self):
        mime_type = MIMEType.from_string("*/*;q=0.8")

        self.assertIsNone(mime_type.type)
        self.assertIsNone(mime_type.subtype)
        self.assertEqual(0.8, mime_type.quality)

    def test_incorrect_wildcard_order(self):
        with self.assertRaises(MIMEType.MIMETypeWildcardHierarchyException):
            MIMEType.from_string("*/html")

    def test_parsing_failed(self):
        with self.assertRaises(MIMEType.MIMETypeParsingException):
            MIMEType.from_string("can not parse me")

    def test_parse_with_trailing_whitespaces(self):
        MIMEType.from_string(" image/jpeg")

    def test_mime_type_equal(self):
        mime_type1 = MIMEType("application", "json", 0.9)
        mime_type2 = MIMEType("application", "json", 0.9)

        self.assertEqual(mime_type1, mime_type2)

    def test_quality_compare(self):
        mime_type1 = MIMEType("application", "json")
        mime_type2 = MIMEType("text", "html", 0.9)

        self.assertGreater(mime_type1, mime_type2)
        self.assertLess(mime_type2, mime_type1)

    def test_matches_mime_type_string(self):
        self.assertTrue(MIMEType("text", "html").matches_mime_type_string("text/html"))
        self.assertTrue(MIMEType("text", "*").matches_mime_type_string("text/html"))
        self.assertTrue(MIMEType("text", "html").matches_mime_type_string("text/*"))
        self.assertTrue(MIMEType("*", "*").matches_mime_type_string("text/*"))

        self.assertFalse(MIMEType("text", "*").matches_mime_type_string("application/json"))

    def test_to_string(self):
        mime_type = MIMEType("application", "json", 0.9, {"v": "b3"})

        self.assertEqual("application/json", mime_type.to_string(with_details=False))
        self.assertEqual("application/json;v=b3;q=0.9", mime_type.to_string(with_details=True))

    def test_with_charset(self):
        mime_type = MIMEType.from_string("application/json; charset=utf-8")

        self.assertEqual("utf-8", mime_type.charset)
