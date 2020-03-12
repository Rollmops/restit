import logging
import warnings
from collections import namedtuple
from typing import Type, Any, List

LOGGER = logging.getLogger(__name__)

QueryParameter = namedtuple("QueryParameter", ["name", "description", "type", "required", "default"])


def query_parameter(name: str, description: str, type: Type = str, required: bool = True, default: Any = None):
    def decorator(func):
        _query_parameter = QueryParameter(name, description, type, required, default)
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
