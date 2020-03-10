from typing import Type


def request_mapping(path: str):
    def wrapper(clazz: Type):
        clazz.__request_mapping__ = path
        return clazz

    return wrapper
