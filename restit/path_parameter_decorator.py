import logging
from collections import namedtuple
from typing import Type, List

LOGGER = logging.getLogger(__name__)

PathParameter = namedtuple("PathParameter", ["name", "description", "type"])


# noinspection PyShadowingBuiltins
def path_parameter(name: str, description: str, type: Type = str):
    def decorator(clazz):
        _path_parameter = PathParameter(name, description, type)

        registered_path_parameters: List[PathParameter] = getattr(clazz, "__path_parameters__", [])
        LOGGER.debug("Registering path parameter %s for %s", _path_parameter, clazz.__name__)
        registered_path_parameters.append(_path_parameter)
        setattr(clazz, "__path_parameters__", registered_path_parameters)
        return clazz

    return decorator
