from typing import Type

from restit.resource import Resource, PathParameter


# noinspection PyShadowingBuiltins
def path_parameter(name: str, type=str, doc: str = None):
    def decorator(clazz: Type[Resource]):
        clazz.add_path_parameter(PathParameter(name, type, doc))
        return clazz

    return decorator
