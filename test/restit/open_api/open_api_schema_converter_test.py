import json
import unittest
from enum import Enum

from marshmallow import Schema, fields, validate
from marshmallow.validate import Range, Regexp, Length

from restit.open_api.open_api_schema_converter import OpenApiSchemaConverter


class SimpleSchema(Schema):
    """My simple schema."""

    field1 = fields.Integer(required=True, default=1, validate=[Range(min=1, max=10)])
    field1.__doc__ = "Doc of field1"
    field2 = fields.String(validate=[Regexp(r"\w+"), Length(min=1, max=100)])
    field3 = fields.UUID()


class SchemaWithNested(Schema):
    """I have a nested field"""

    nested_field = fields.Nested(SimpleSchema(), required=True)


class SchemaWithIntegerList(Schema):
    int_list = fields.List(fields.Integer())


class SchemaWithNestedList(Schema):
    nested_list = fields.Nested(SchemaWithNested())


class SchemaWithMapping(Schema):
    mapping = fields.Mapping(keys=fields.String(), values=fields.Integer())


class OpenApiSchemaConverterTestCase(unittest.TestCase):
    def test_simple(self):
        open_api_schema = OpenApiSchemaConverter().convert_schema(SimpleSchema(), {})

        self.assertEqual(
            {
                "description": "My simple schema.",
                "properties": {
                    "field1": {
                        "default": 1,
                        "description": "Doc of field1",
                        "exclusiveMaximum": False,
                        "exclusiveMinimum": False,
                        "maximum": 10,
                        "minimum": 1,
                        "type": "integer",
                    },
                    "field2": {
                        "description": "A string field.",
                        "maxLength": 100,
                        "minLength": 1,
                        "pattern": "\\w+",
                        "type": "string",
                    },
                    "field3": {
                        "description": "A UUID field.",
                        "format": "uuid",
                        "type": "string",
                    },
                },
                "required": ["field1"],
                "type": "object",
            },
            open_api_schema,
        )

    def test_nested(self):
        open_api_schema = OpenApiSchemaConverter().convert_schema(SchemaWithNested(), {})

        self.assertEqual(
            {
                "description": "I have a nested field",
                "properties": {
                    "nested_field": {
                        "description": "My simple schema.",
                        "properties": {
                            "field1": {
                                "default": 1,
                                "description": "Doc " "of " "field1",
                                "exclusiveMaximum": False,
                                "exclusiveMinimum": False,
                                "maximum": 10,
                                "minimum": 1,
                                "type": "integer",
                            },
                            "field2": {
                                "description": "A " "string " "field.",
                                "maxLength": 100,
                                "minLength": 1,
                                "pattern": "\\w+",
                                "type": "string",
                            },
                            "field3": {
                                "description": "A " "UUID " "field.",
                                "format": "uuid",
                                "type": "string",
                            },
                        },
                        "required": ["field1"],
                        "type": "object",
                    }
                },
                "required": ["nested_field"],
                "type": "object",
            },
            open_api_schema,
        )

    def test_integer_list(self):
        open_api_schema = OpenApiSchemaConverter().convert(SchemaWithIntegerList(), {})
        self.assertEqual(
            {
                "description": None,
                "properties": {
                    "int_list": {
                        "items": {
                            "description": "An integer field.",
                            "type": "integer",
                        },
                        "type": "array",
                    }
                },
                "required": [],
                "type": "object",
            },
            open_api_schema,
        )

    def test_nested_list(self):
        open_api_schema = OpenApiSchemaConverter().convert(SchemaWithNestedList(), {})

        self.assertEqual(
            {
                "description": None,
                "properties": {
                    "nested_list": {
                        "description": "I have a nested field",
                        "properties": {
                            "nested_field": {
                                "description": "My " "simple " "schema.",
                                "properties": {
                                    "field1": {
                                        "default": 1,
                                        "description": "Doc " "of " "field1",
                                        "exclusiveMaximum": False,
                                        "exclusiveMinimum": False,
                                        "maximum": 10,
                                        "minimum": 1,
                                        "type": "integer",
                                    },
                                    "field2": {
                                        "description": "A " "string " "field.",
                                        "maxLength": 100,
                                        "minLength": 1,
                                        "pattern": "\\w+",
                                        "type": "string",
                                    },
                                    "field3": {
                                        "description": "A " "UUID " "field.",
                                        "format": "uuid",
                                        "type": "string",
                                    },
                                },
                                "required": ["field1"],
                                "type": "object",
                            }
                        },
                        "required": ["nested_field"],
                        "type": "object",
                    }
                },
                "required": [],
                "type": "object",
            },
            open_api_schema,
        )

    def test_mapping(self):
        open_api_schema = OpenApiSchemaConverter().convert(SchemaWithMapping(), {})

        self.assertEqual(
            {
                "description": None,
                "properties": {
                    "mapping": {
                        "additionalProperties": {"type": "integer"},
                        "description": "An abstract class for objects with " "key-value pairs.",
                        "type": "object",
                    }
                },
                "required": [],
                "type": "object",
            },
            open_api_schema,
        )

    def test_recursive_schema(self):
        class MyRecursiveSchema(Schema):
            _fields1 = fields.List(fields.Nested(lambda: MyRecursiveSchema()))
            _fields2 = fields.List(fields.Nested("self"))

        open_api_schema = OpenApiSchemaConverter().convert(MyRecursiveSchema(), {})

        self.assertEqual(
            {
                "description": None,
                "properties": {
                    "_fields1": {"items": {"description": "MyRecursiveSchema", "type": "object"}, "type": "array"},
                    "_fields2": {"items": {"description": "MyRecursiveSchema", "type": "object"}, "type": "array"},
                },
                "required": [],
                "type": "object",
            },
            open_api_schema,
        )

    def test_enum_schema_json_serializable(self):
        class MyEnum(Enum):
            FIRST = "FIRST"
            SECOND = "SECOND"

        class MyEnumSchema(Schema):
            my_enum = fields.String(
                required=False, default=MyEnum.FIRST, validate=validate.OneOf([e.value for e in MyEnum])
            )

        open_api_schema = OpenApiSchemaConverter().convert(MyEnumSchema(), {})
        self.assertEqual(
            {
                "description": None,
                "properties": {
                    "my_enum": {
                        "default": "FIRST",
                        "description": "A string field.",
                        "enum": ["FIRST", "SECOND"],
                        "type": "string",
                    }
                },
                "required": [],
                "type": "object",
            },
            open_api_schema,
        )

        open_api_schema_json = json.dumps(open_api_schema)

        self.assertEqual(
            (
                '{"required": [], "type": "object", "description": null, "properties": '
                '{"my_enum": {"type": "string", "description": "A string field.", "enum": '
                '["FIRST", "SECOND"], "default": "FIRST"}}}'
            ),
            open_api_schema_json,
        )
