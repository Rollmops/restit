from marshmallow import fields
from marshmallow.fields import Field


class PathParameter:
    """Class that holds the path parameter properties and is used in
    the :func:`~restit.decorator.path` decorator.

    :param name: The path parameter name
    :type name: str
    :param description: The description of the path parameter
    :type description: str
    :param field_type: The type of the path parameter
    :type field_type: marshmallow.fields.Field
    """

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
