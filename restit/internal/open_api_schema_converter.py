from typing import Union, Type
from uuid import UUID

from marshmallow import Schema, fields


class OpenApiSchemaConverter:
    _TYPE_MAP = {
        fields.Integer: "integer"
    }
    _PYTHON_TYPE_SCHEMA_MAPPING = {
        int: {"type": "integer"},
        str: {"type": "string"},
        UUID: {"type": "string", "format": "uuid"},
        bytes: {"type": "string", "format": "binary"}
    }

    @staticmethod
    def convert(schema: Union[Schema, Type]) -> dict:
        if isinstance(schema, Schema):
            schema_definition = OpenApiSchemaConverter._create_open_api_schema_from_marshmallow(schema)
        else:
            try:
                schema_definition = OpenApiSchemaConverter._PYTHON_TYPE_SCHEMA_MAPPING[schema]
            except KeyError:
                raise Exception(f"Type {schema} is not supported as request body type")
        return schema_definition

    @staticmethod
    def _create_open_api_schema_from_marshmallow(schema):
        schema_definition = {
            "title": schema.__doc__,
            "type": "object",
            "properties": {
                name: {
                    "type": OpenApiSchemaConverter._TYPE_MAP.get(field.__class__, "string")
                }
                for name, field in schema.fields.items()
            },
            "required": [name for name, field in schema.fields.items() if field.required]
        }
        return schema_definition
