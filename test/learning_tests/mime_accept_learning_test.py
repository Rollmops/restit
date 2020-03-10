import unittest

from werkzeug.datastructures import MIMEAccept


class MimeAcceptLearningTestCase(unittest.TestCase):
    def test_something(self):
        mime_accept = MIMEAccept([("application/json", 1)])
        self.assertTrue(mime_accept.accept_json)

        self.assertIn("application/json", mime_accept)
