from typing import Union, Type, Any

from marshmallow import Schema

from restit.internal.type_converter.string_type_converter import StringTypeConverter


class SchemaOrTypeConverter:
    @staticmethod
    def convert(value, type_or_schema: Union[Type, Schema]) -> Any:
        if isinstance(type_or_schema, Schema):
            return type_or_schema.dump(value)
        elif isinstance(value, (str, bytes)):
            return StringTypeConverter.convert(value, type_or_schema)
        else:
            return type_or_schema(value)
