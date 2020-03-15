import unittest

from marshmallow import Schema, fields


class MarshmallowLearningTestCase(unittest.TestCase):
    def test_dump(self):
        class MySchema(Schema):
            f1 = fields.Integer()
            f2 = fields.String()

        my_schema = MySchema()

        self.assertEqual({'f1': 2, 'f2': '3'}, my_schema.dump({"f1": "2", "f2": "3"}))
        self.assertEqual('{"f1": 2}', my_schema.dumps({"f1": "2"}))

    def test_load(self):
        class MySchema(Schema):
            f1 = fields.Integer()
            f2 = fields.String()

        my_schema = MySchema()

        self.assertEqual({'f1': 2, 'f2': '3'}, my_schema.load({"f1": "2", "f2": "3"}))
        self.assertEqual({'f1': 2, "f2": "3"}, my_schema.loads('{"f1": "2", "f2": "3"}'))
