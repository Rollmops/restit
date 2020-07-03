import unittest

from restit.internal.resource_path import ResourcePath


class ResourcePathTestCase(unittest.TestCase):
    def test_match_no_path_param(self):
        resource_path = ResourcePath("/hello")

        self.assertEqual((True, {}), resource_path.get_match("/hello"))
        self.assertEqual((False, None), resource_path.get_match("/hello/"))
        self.assertEqual((False, None), resource_path.get_match("hello"))
        self.assertEqual((False, None), resource_path.get_match("/miau/hello"))

    def test_match_no_type(self):
        resource_path = ResourcePath("/hello/:id")

        self.assertEqual((True, {"id": "21"}), resource_path.get_match("/hello/21"))
        self.assertEqual((False, None), resource_path.get_match("/hello/"))
        self.assertEqual((False, None), resource_path.get_match("/hans/hello/21"))
        self.assertEqual((False, None), resource_path.get_match("/hello"))

    def test_match_multiple_path_params(self):
        resource_path = ResourcePath("/hello/:id/wuff/:miau")
        self.assertEqual(
            (True, {'id': '21', 'miau': 'dog'}), resource_path.get_match("/hello/21/wuff/dog")
        )

    def test_match_path_param_type_int(self):
        resource_path = ResourcePath("/hello/:id<int>")
        self.assertEqual((True, {"id": 21}), resource_path.get_match("/hello/21"))
        self.assertEqual((False, None), resource_path.get_match("/hello/hans"))

        resource_path = ResourcePath("/hello/:id<integer>")
        self.assertEqual((True, {"id": 21}), resource_path.get_match("/hello/21"))
        self.assertEqual((False, None), resource_path.get_match("/hello/hans"))

    def test_match_path_param_type_string(self):
        resource_path = ResourcePath("/hello/:id<str>")
        self.assertEqual((True, {"id": "21"}), resource_path.get_match("/hello/21"))
        self.assertEqual((True, {"id": "hans"}), resource_path.get_match("/hello/hans"))

        resource_path = ResourcePath("/hello/:id<string>")
        self.assertEqual((True, {"id": "21"}), resource_path.get_match("/hello/21"))
        self.assertEqual((True, {"id": "hans"}), resource_path.get_match("/hello/hans"))

    def test_match_path_param_with_special_chars(self):
        resource_path = ResourcePath("/hello/:id_1<str>")
        self.assertEqual((True, {"id_1": "21"}), resource_path.get_match("/hello/21"))
        self.assertEqual((True, {"id_1": "hans"}), resource_path.get_match("/hello/hans"))

    def test_do_not_allow_path_params_with_slash(self):
        resource_path = ResourcePath("/hello/:id")

        self.assertEqual((False, None), resource_path.get_match("/hello/you/whats/up"))

    def test_match_special_characters(self):
        resource_path = ResourcePath("/hello/:id")

        self.assertEqual((True, {"id": "a_b- $"}), resource_path.get_match("/hello/a_b- $"))

    def test_invalid_type_annotation(self):
        with self.assertRaises(ResourcePath.UnknownPathParamTypeAnnotation):
            ResourcePath("/hello/:id<invalid>")
