import logging
from typing import Type

LOGGER = logging.getLogger(__name__)


def request_mapping(path: str):
    def wrapper(clazz: Type):
        if not path.startswith("/"):
            raise PathIsNotStartingWithSlashException(path)
        LOGGER.debug("Registering path %s for resource %s", path, clazz.__name__)
        clazz.__request_mapping__ = path
        return clazz

    return wrapper


class PathIsNotStartingWithSlashException(Exception):
    pass
