from typing import Union, Type, Any

from marshmallow import Schema
from marshmallow.fields import Field


class SchemaOrFieldDeserializer:
    @staticmethod
    def deserialize(value, field_or_schema: Union[Type, Schema, Field]) -> Any:
        if isinstance(field_or_schema, Schema):
            return field_or_schema.load(value)
        if isinstance(field_or_schema, Field):
            return SchemaOrFieldDeserializer._deserialize_field(value, field_or_schema)
        else:
            raise SchemaOrFieldDeserializer.OnlySchemaOrFieldTypeSupportedException()

    @staticmethod
    def _deserialize_field(value, field: Field):
        if value is None:
            if field.default:
                return field.default
            if field.required:
                raise SchemaOrFieldDeserializer.RequiredFieldNotSetException()
        else:
            return field.deserialize(value)

    class OnlySchemaOrFieldTypeSupportedException(Exception):
        pass

    class RequiredFieldNotSetException(Exception):
        pass
