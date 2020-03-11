from typing import Type


def request_mapping(path: str):
    def wrapper(clazz: Type):
        if not path.startswith("/"):
            raise PathIsNotStartingWithSlashException(path)
        clazz.__request_mapping__ = path
        return clazz

    return wrapper


class PathIsNotStartingWithSlashException(Exception):
    pass
