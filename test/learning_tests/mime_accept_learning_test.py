import unittest

from werkzeug.datastructures import MIMEAccept


class MimeAcceptLearningTestCase(unittest.TestCase):
    def test_something(self):
        mime_accept = MIMEAccept([("application/json", 1)])
        mime_accept2 = MIMEAccept([("application/json", 1), ("text/plain", 0.6)])

        self.assertTrue(mime_accept.accept_json)
        self.assertIn("application/json", mime_accept)

        self.assertEqual(['application/json'], list(set(mime_accept2.values()) & set(mime_accept.values())))

        self.assertEqual(["application/json"], list(set(mime_accept.values()).intersection({"application/json"})))
        self.assertEqual([], list(set(mime_accept.values()).intersection({"my/type"})))
        self.assertEqual([], list(set(mime_accept2.values()).intersection({"my/type"})))
        self.assertEqual(["application/json"], list(set(mime_accept2.values()).intersection({"application/json"})))
        self.assertEqual(["application/json"], list(set(mime_accept2.values()).intersection({"application/json"})))

        self.assertEqual("application/json", mime_accept2.best_match(["application/json", "text/plain"]))

        self.assertEqual(0.6, mime_accept2[mime_accept2.find("text/plain")][1])

        self.assertEqual("application/json", MIMEAccept([("*/*", 1)]).best_match(["application/json"]))
        self.assertIsNone(MIMEAccept([("application/json", 1)]).best_match(["text/plain"]))
