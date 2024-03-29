from enum import Enum
from typing import Union, List, Pattern

import marshmallow
from marshmallow import Schema, fields
from marshmallow.fields import Field, Nested
from marshmallow.validate import Validator, Range, Length, Regexp, OneOf


# https://swagger.io/docs/specification/data-models/dictionaries/
def get_mapping_field_schema(field: fields.Mapping):
    return {
        "type": "object",
        "additionalProperties": _OPEN_API_SCHEMA_TYPE_MAPPING[field.value_field.__class__](field.value_field),
    }


_OPEN_API_SCHEMA_TYPE_MAPPING = {
    fields.Integer: lambda _: {"type": "integer"},
    fields.Float: lambda _: {"type": "number", "format": "float"},
    fields.String: lambda _: {"type": "string"},
    fields.UUID: lambda _: {"type": "string", "format": "uuid"},
    fields.Boolean: lambda _: {"type": "boolean"},
    fields.Email: lambda _: {"type": "string", "format": "email"},
    fields.Url: lambda _: {"type": "string", "format": "uri"},
    fields.DateTime: lambda _: {"type": "string", "format": "date-time"},
    fields.Date: lambda _: {"type": "string", "format": "date"},
    fields.Number: lambda _: {"type": "number"},
    fields.Mapping: get_mapping_field_schema,
}


class OpenApiSchemaConverter:
    def __init__(self):
        self._handled_schemas = []

    def convert(self, schema_or_field: Union[Field, Schema], root_spec: dict):
        if isinstance(schema_or_field, Schema):
            return self.convert_schema(schema_or_field, root_spec)
        if isinstance(schema_or_field, Nested):
            return self.convert_schema(schema_or_field.schema, root_spec)

        return self.convert_field(schema_or_field)

    def convert_schema(self, schema: Schema, root_spec: dict):
        if schema.__class__ in self._handled_schemas:
            return {"description": schema.__class__.__name__, "type": "object"}
        self._handled_schemas.append(schema.__class__)
        open_api_schema = {
            "required": [],
            "type": "object",
            "description": schema.__doc__,
            "properties": {},
        }

        for name, field in schema.fields.items():
            if isinstance(field, Nested):
                open_api_schema["properties"][name] = self.convert_schema(field.schema, root_spec)
            elif isinstance(field, fields.List):
                open_api_schema["properties"][name] = self.convert_array(field, root_spec)
            else:
                open_api_schema["properties"][name] = self.convert_field(field)
            if field.required:
                open_api_schema["required"].append(name)

        if getattr(schema, "__reusable_schema__", False):
            root_spec["components"]["schemas"][schema.__class__.__name__] = open_api_schema
            return {"$ref": f"#/components/schemas/{schema.__class__.__name__}"}

        return open_api_schema

    def convert_array(self, array: fields.List, root_spec: dict) -> dict:
        list_schema = {
            "type": "array",
            "items": self.convert(array.inner, root_spec),
        }
        return list_schema

    def convert_field(self, field: Field) -> dict:
        field_schema = _OPEN_API_SCHEMA_TYPE_MAPPING[field.__class__](field).copy()
        field_schema["description"] = self._get_first_doc_line(str(field.__doc__))
        field_schema = self._process_validators(field.validators, field_schema)
        if field.default != marshmallow.missing:
            field_schema["default"] = field.default.value if isinstance(field.default, Enum) else field.default

        return field_schema

    @staticmethod
    def _process_validators(validators: List[Validator], field_schema: dict) -> dict:
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
                field_schema["pattern"] = (
                    validator.regex.pattern if isinstance(validator.regex, Pattern) else str(validator.regex)
                )
            elif isinstance(validator, OneOf):
                field_schema["enum"] = validator.choices

        return field_schema

    @staticmethod
    def _get_first_doc_line(doc: str) -> str:
        lines = doc.split("\n")
        if lines:
            return lines[0].strip("\n")
