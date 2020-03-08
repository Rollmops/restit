from typing import Type


def request_mapping(url: str):
    def wrapper(clazz: Type):
        clazz.__url__ = url
        return clazz

    return wrapper
