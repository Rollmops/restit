from typing import Union, Type
from uuid import UUID

from marshmallow import Schema, fields


class OpenApiSchemaConverter:
    _TYPE_MAP = {
        fields.Integer: "integer"
    }
    _PYTHON_TYPE_SCHEMA_MAPPING = {
        int: {"type": "integer", "default": None},
        str: {"type": "string"},
        UUID: {"type": "string", "format": "uuid"},
        bytes: {"type": "string", "format": "binary"}
    }

    @staticmethod
    def convert(schema: Union[Schema, Type], spec_structure: dict = None) -> dict:
        if isinstance(schema, Schema):
            schema_definition = OpenApiSchemaConverter._create_open_api_schema_from_marshmallow(schema, spec_structure)
        else:
            try:
                schema_definition = OpenApiSchemaConverter._PYTHON_TYPE_SCHEMA_MAPPING[schema]
            except KeyError:
                raise Exception(f"Type {schema} is not supported as request body type")
        return schema_definition

    @staticmethod
    def _create_open_api_schema_from_marshmallow(schema: Schema, spec_structure: dict):
        schema_component_definition = {
            "description": schema.__doc__,
            "type": "object",
            "properties": {
                name: {
                    "type": OpenApiSchemaConverter._TYPE_MAP.get(field.__class__, "string"),
                    "description": field.__doc__.split("\n")[0]
                }
                for name, field in schema.fields.items()
            },
            "required": [name for name, field in schema.fields.items() if field.required]
        }

        if getattr(schema, "__reusable_open_api_component__", False):
            schema_definition = {
                "$ref": f"#/components/schemas/{schema.__class__.__name__}"
            }
            spec_structure["components"]["schemas"][schema.__class__.__name__] = schema_component_definition
            return schema_definition

        return schema_component_definition
