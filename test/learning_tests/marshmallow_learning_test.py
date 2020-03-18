import unittest

from marshmallow import Schema, fields, ValidationError


class MarshmallowLearningTestCase(unittest.TestCase):
    def test_dump(self):
        class MySchema(Schema):
            f1 = fields.Integer()
            f2 = fields.String()

        my_schema = MySchema()

        self.assertEqual({'f1': 2, 'f2': '3'}, my_schema.dump({"f1": "2", "f2": "3"}))
        self.assertEqual('{"f1": 2}', my_schema.dumps({"f1": "2"}))

        self.assertEqual({}, my_schema.dump('{"f1": 2, "f2": "3"}'))

    def test_load(self):
        class MySchema(Schema):
            f1 = fields.Integer()
            f2 = fields.String()

        my_schema = MySchema()

        self.assertEqual({'f1': 2, 'f2': '3'}, my_schema.load({"f1": "2", "f2": "3"}))
        self.assertEqual({'f1': 2, "f2": "3"}, my_schema.loads('{"f1": "2", "f2": "3"}'))

    def test_validate(self):
        class MySchema(Schema):
            f1 = fields.Integer()
            f2 = fields.String()

        my_schema = MySchema()
        self.assertEqual({}, my_schema.validate({'f1': 2, 'f2': '3'}))
        self.assertEqual({}, my_schema.validate({'f1': '2', 'f2': '3'}))
        self.assertEqual({'f1': ['Not a valid integer.']}, my_schema.validate({'f1': 'asd', 'f2': '3'}))

    def test_single_field(self):
        field = fields.Integer()

        self.assertEqual(2, field.serialize("", None, lambda *args: "2"))
        self.assertEqual(2, field.serialize("", None, lambda *args: 2))

        fields.Email().serialize("", None, lambda *args: "1234")
        with self.assertRaises(ValidationError):
            fields.Email().deserialize("1234")

        self.assertEqual(2, field.deserialize("2"))
        self.assertEqual(2, field.deserialize(2))

        with self.assertRaises(ValidationError):
            field.deserialize("21321dsadsad31")

        with self.assertRaises(ValueError):
            field.serialize("", None, lambda *args: "31sadsad")

