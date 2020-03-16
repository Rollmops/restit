import logging
import warnings
from collections import namedtuple
from typing import Any, List

from marshmallow.fields import Field, String

LOGGER = logging.getLogger(__name__)

QueryParameter = namedtuple("QueryParameter", ["name", "description", "field_type", "required", "default"])


# noinspection PyShadowingBuiltins
def query_parameter(
        name: str, description: str, field_type: Field = String, required: bool = True, default: Any = None
):
    def decorator(func):
        _query_parameter = QueryParameter(name, description, field_type, required, default)
        if required and default is not None:
            warnings.warn(f"Specified default value '{default}' for required query parameter {name}")
        registered_query_parameters: List[QueryParameter] = getattr(func, "__query_parameters__", [])
        LOGGER.debug(
            "Registering query parameter %s for %s", _query_parameter, func.__name__
        )
        registered_query_parameters.append(_query_parameter)
        setattr(func, "__query_parameters__", registered_query_parameters)
        return func

    return decorator
