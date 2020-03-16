from typing import Union, Type

from marshmallow import Schema, fields
from marshmallow.fields import Field

from restit.bytes_field import BytesField


class OpenApiSchemaConverter:
    _PYTHON_TYPE_SCHEMA_MAPPING = {
        fields.Integer: {"type": "integer", "default": None},
        fields.String: {"type": "string"},
        fields.UUID: {"type": "string", "format": "uuid"},
        BytesField: {"type": "string", "format": "binary"}
    }

    @staticmethod
    def convert(schema_or_field: Union[Schema, Field], spec_structure: dict = None) -> dict:
        if isinstance(schema_or_field, Schema):
            schema_definition = OpenApiSchemaConverter._create_open_api_schema_from_marshmallow(
                schema_or_field, spec_structure
            )
        elif isinstance(schema_or_field, Field):
            schema_definition = OpenApiSchemaConverter._PYTHON_TYPE_SCHEMA_MAPPING[schema_or_field.__class__]
        else:
            raise Exception(f"Type {schema_or_field} is not supported as request body type")
        return schema_definition

    @staticmethod
    def _create_open_api_schema_from_marshmallow(schema: Schema, spec_structure: dict):
        schema_component_definition = {
            "description": schema.__doc__,
            "type": "object",
            "properties": {
                name: OpenApiSchemaConverter._create_property_item(field.__class__, field.__doc__)
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

    @staticmethod
    def _create_property_item(field_type: Type, description: str) -> dict:
        property_item = OpenApiSchemaConverter._PYTHON_TYPE_SCHEMA_MAPPING[field_type]
        property_item["description"] = description
        return property_item
