from marshmallow import fields
from marshmallow.fields import Field


class PathParameter:
    _PYTHON_TYPE_FIELD_MAPPING = {
        int: fields.Integer(),
        str: fields.String()
    }

    def __init__(self, name: str, description: str, field_type: Field):
        self.name = name
        self.description = description
        self.field_type = \
            field_type if isinstance(field_type, Field) else PathParameter._PYTHON_TYPE_FIELD_MAPPING[field_type]

    def __str__(self):
        return f"PathParameter(name='{self.name}', description='{self.description}', field_type={self.field_type})"
