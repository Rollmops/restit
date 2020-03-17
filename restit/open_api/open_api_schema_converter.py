from typing import Union

import marshmallow
from marshmallow import Schema, fields
from marshmallow.fields import Field, Nested


class OpenApiSchemaConverter:
    _SCHEMA_TYPE_MAPPING = {
        fields.Integer: {"type": "integer"},
        fields.Float: {"type": "number", "format": "float"},
        fields.String: {"type": "string"},
        fields.UUID: {"type": "string", "format": "uuid"},
        fields.Boolean: {"type": "boolean"},
        fields.Email: {"type": "string", "format": "email"},
        fields.Url: {"type": "string", "format": "uri"},
        fields.DateTime: {"type": "string", "format": "date-time"},
        fields.Date: {"type": "string", "format": "date"},
        fields.Number: {"type": "number"}
    }

    @staticmethod
    def convert(schema_or_field: Union[Field, Schema]):
        if isinstance(schema_or_field, Schema):
            return OpenApiSchemaConverter.convert_schema(schema_or_field)
        elif isinstance(schema_or_field, Nested):
            return OpenApiSchemaConverter.convert_schema(schema_or_field.schema)
        else:
            return OpenApiSchemaConverter.convert_field(schema_or_field)

    @staticmethod
    def convert_schema(schema: Schema):
        open_api_schema = {
            "required": [],
            "type": "object",
            "description": schema.__doc__,
            "properties": {
            }
        }
        for name, field in schema.fields.items():
            if isinstance(field, Nested):
                open_api_schema["properties"][name] = OpenApiSchemaConverter.convert_schema(field.schema)
            elif isinstance(field, fields.List):
                open_api_schema["properties"][name] = OpenApiSchemaConverter.convert_array(field)
            else:
                open_api_schema["properties"][name] = OpenApiSchemaConverter.convert_field(field)
            if field.required:
                open_api_schema["required"].append(name)

        return open_api_schema

    @staticmethod
    def convert_array(array: fields.List) -> dict:
        list_schema = {
            "type": "array",
            "items": OpenApiSchemaConverter.convert(array.inner)
        }
        return list_schema

    @staticmethod
    def convert_field(field: Field) -> dict:
        field_schema = OpenApiSchemaConverter._SCHEMA_TYPE_MAPPING[field.__class__]
        field_schema["description"] = OpenApiSchemaConverter._get_first_doc_line(str(field.__doc__))
        if field.default != marshmallow.missing:
            field_schema["default"] = field.default
        return field_schema

    @staticmethod
    def _get_first_doc_line(doc: str) -> str:
        lines = doc.split("\n")
        if lines:
            return lines[0].strip("\n")
