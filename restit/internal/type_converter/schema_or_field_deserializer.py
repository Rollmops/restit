from typing import Union, Type, Any

from marshmallow import Schema
from marshmallow.fields import Field


class SchemaOrFieldDeserializer:
    @staticmethod
    def convert(value, type_or_schema: Union[Type, Schema, Field]) -> Any:
        if isinstance(type_or_schema, Schema):
            return type_or_schema.dump(value)
        if isinstance(type_or_schema, Field):

            return type_or_schema.deserialize(value)
        else:
            raise SchemaOrFieldDeserializer.OnlySchemaOrFieldTypeSupportedException()

    class OnlySchemaOrFieldTypeSupportedException(Exception):
        pass
