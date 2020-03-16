import unittest

from marshmallow import Schema, fields

from restit.open_api.open_api_schema_converter import OpenApiSchemaConverter


class SimpleSchema(Schema):
    """My simple schema."""
    field1 = fields.Integer(required=True)
    field1.__doc__ = "Doc of field1"
    field2 = fields.String()
    field3 = fields.UUID()


class SchemaWithNested(Schema):
    """I have a nested field"""
    nested_field = fields.Nested(SimpleSchema(), required=True)


class SchemaWithIntegerList(Schema):
    int_list = fields.List(fields.Integer())


class SchemaWithNestedList(Schema):
    nested_list = fields.Nested(SchemaWithNested())


class OpenApiSchemaConverterTestCase(unittest.TestCase):
    def test_simple(self):
        open_api_schema = OpenApiSchemaConverter.convert_schema(SimpleSchema())

        self.assertEqual({
            'description': 'My simple schema.',
            'properties': {
                'field1': {
                    'description': 'Doc of field1',
                    'type': 'integer'
                },
                'field2': {
                    'description': 'A string field.',
                    'type': 'string'
                },
                'field3': {
                    'description': 'A UUID field.',
                    'format': 'uuid',
                    'type': 'string'
                }
            },
            'required': ['field1'],
            'type': 'object'
        }, open_api_schema)

    def test_nested(self):
        open_api_schema = OpenApiSchemaConverter.convert_schema(SchemaWithNested())

        self.assertEqual({
            'description': 'I have a nested field',
            'properties': {
                'nested_field': {
                    'description': 'My simple schema.',
                    'properties': {
                        'field1': {
                            'description': 'Doc '
                                           'of '
                                           'field1',
                            'type': 'integer'
                        },
                        'field2': {
                            'description': 'A '
                                           'string '
                                           'field.',
                            'type': 'string'
                        },
                        'field3': {
                            'description': 'A '
                                           'UUID '
                                           'field.',
                            'format': 'uuid',
                            'type': 'string'
                        }
                    },
                    'required': ['field1'],
                    'type': 'object'
                }
            },
            'required': ['nested_field'],
            'type': 'object'
        }, open_api_schema)

    def test_integer_list(self):
        open_api_schema = OpenApiSchemaConverter.convert(SchemaWithIntegerList())
        self.assertEqual({
            'description': None,
            'properties': {
                'int_list': {
                    'items': {
                        'description': 'An integer field.',
                        'type': 'integer'
                    },
                    'type': 'array'
                }
            },
            'required': [],
            'type': 'object'
        }, open_api_schema)

    def test_nested_list(self):
        open_api_schema = OpenApiSchemaConverter.convert(SchemaWithNestedList())

        self.assertEqual({
            'description': None,
            'properties': {
                'nested_list': {
                    'description': 'I have a nested field',
                    'properties': {
                        'nested_field': {
                            'description': 'My '
                                           'simple '
                                           'schema.',
                            'properties': {
                                'field1': {
                                    'description': 'Doc '
                                                   'of '
                                                   'field1',
                                    'type': 'integer'
                                },
                                'field2': {
                                    'description': 'A '
                                                   'string '
                                                   'field.',
                                    'type': 'string'
                                },
                                'field3': {
                                    'description': 'A '
                                                   'UUID '
                                                   'field.',
                                    'format': 'uuid',
                                    'type': 'string'
                                }
                            },
                            'required': ['field1'],
                            'type': 'object'
                        }
                    },
                    'required': ['nested_field'],
                    'type': 'object'
                }
            },
            'required': [],
            'type': 'object'
        }, open_api_schema)
