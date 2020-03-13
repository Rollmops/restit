import logging
from typing import Type, List

from restit.path_parameter import PathParameter
from restit.path_parameter_decorator import register_path_parameter
from restit.resource import Resource

LOGGER = logging.getLogger(__name__)


def request_mapping(path: str, path_parameters: List[PathParameter] = None):
    path_parameters = path_parameters or []

    def wrapper(clazz: Type[Resource]):

        if not path.startswith("/"):
            raise PathIsNotStartingWithSlashException(path)
        LOGGER.debug("Registering path %s for swagger %s", path, clazz.__name__)
        clazz.__request_mapping__ = path
        for path_parameter in path_parameters:
            register_path_parameter(path_parameter, clazz)
        return clazz

    return wrapper


class PathIsNotStartingWithSlashException(Exception):
    pass
