import logging
from typing import List

from marshmallow.fields import Field, String

from restit._path_parameter import PathParameter

LOGGER = logging.getLogger(__name__)


# noinspection PyShadowingNames
def register_path_parameter(path_parameter: PathParameter, clazz):
    registered_path_parameters: List[PathParameter] = getattr(clazz, "__path_parameters__", [])
    LOGGER.debug("Registering path parameter %s for %s", path_parameter, clazz.__name__)
    registered_path_parameters.append(path_parameter)
    setattr(clazz, "__path_parameters__", registered_path_parameters)


# noinspection PyShadowingBuiltins
def path_parameter(name: str, description: str, field_type: Field = String()):
    """Decorator to describe the path parameters.

    Besides describing the path parameters in the :func:`path` decorator function, you can add this
    decorator to your resource class.

    Example:

    .. code-block:: python

        @path("/orders/:year/:month/:id")
        @path_parameter("year", "The year of the order", fields.Integer())
        @path_parameter("month", "The month of the order", fields.Integer())
        @path_parameter("id", "The order id", fields.Integer())
        class OrdersResource(Resource):
            ...

    .. note::

        If you do not describe the path parameters with either :func:`path_parameter` or inside the
        :func:`path` decorator, they won´t show up in the *OpenApi* documentation and the type is
        considered to be string.

    :param name: The path parameter name
    :type name: str
    :param description: The description of the path parameter
    :type description: str
    :param field_type: The type of the path parameter
    :type field_type: marshmallow.fields.Field
    """

    def decorator(clazz):
        _path_parameter = PathParameter(name, description, field_type)
        register_path_parameter(_path_parameter, clazz)
        return clazz

    return decorator
