from typing import Union, List, Pattern

import marshmallow
from marshmallow import Schema, fields
from marshmallow.fields import Field, Nested
from marshmallow.validate import Validator, Range, Length, Regexp


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
        OpenApiSchemaConverter._process_validators(field.validators, field_schema)
        if field.default != marshmallow.missing:
            field_schema["default"] = field.default
        return field_schema

    @staticmethod
    def _process_validators(validators: List[Validator], field_schema: dict):
        for validator in validators:
            if isinstance(validator, Range):
                field_schema["minimum"] = validator.min
                field_schema["maximum"] = validator.max
                field_schema["exclusiveMinimum"] = not validator.min_inclusive
                field_schema["exclusiveMaximum"] = not validator.max_inclusive
            elif isinstance(validator, Length):
                field_schema["minLength"] = validator.min
                field_schema["maxLength"] = validator.max
            elif isinstance(validator, Regexp):
                field_schema["pattern"] = \
                    validator.regex.pattern if isinstance(validator.regex, Pattern) else str(validator.regex)

    @staticmethod
    def _get_first_doc_line(doc: str) -> str:
        lines = doc.split("\n")
        if lines:
            return lines[0].strip("\n")
