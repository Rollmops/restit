import logging
from typing import Type, List

from restit.path_parameter import PathParameter

LOGGER = logging.getLogger(__name__)


# noinspection PyShadowingNames
def register_path_parameter(path_parameter: PathParameter, clazz):
    registered_path_parameters: List[PathParameter] = getattr(clazz, "__path_parameters__", [])
    LOGGER.debug("Registering path parameter %s for %s", path_parameter, clazz.__name__)
    registered_path_parameters.append(path_parameter)
    setattr(clazz, "__path_parameters__", registered_path_parameters)


# noinspection PyShadowingBuiltins
def path_parameter(name: str, description: str, type: Type = str):
    def decorator(clazz):
        _path_parameter = PathParameter(name, description, type)
        register_path_parameter(_path_parameter, clazz)
        return clazz

    return decorator
