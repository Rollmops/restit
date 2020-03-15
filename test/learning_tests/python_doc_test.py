import unittest

from marshmallow import Schema, fields


class PythonDocTestCase(unittest.TestCase):
    def test_attribute_doc_test(self):
        class MySchema(Schema):
            "Can you access me?"
            field1 = fields.Integer()

            """And me?

            I have a bigger docstring!
            """
            field2 = fields.String()

        my_schema = MySchema()

        self.assertEqual("Can you access me?", my_schema.fields["field1"].parent.__doc__)
        # no ... parent is the class itself ... so no chance to access attribute docs :-(
        self.assertEqual("Can you access me?", my_schema.fields["field2"].parent.__doc__)
