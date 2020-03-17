from marshmallow.fields import Field


class QueryParameter:
    def __init__(self, name: str, description: str, field_type: Field):
        if not isinstance(field_type, Field):
            raise QueryParameter.UnsupportedQueryFieldTypeException(type(field_type))

        self.name = name
        self.description = description
        self.field_type = field_type

    class UnsupportedQueryFieldTypeException(Exception):
        pass
