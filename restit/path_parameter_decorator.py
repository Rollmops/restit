from typing import Type

from restit.resource import Resource, PathParameter


# noinspection PyShadowingBuiltins
def path_parameter(name: str, type=str, description: str = None, format: str = None):
    def decorator(clazz: Type[Resource]):
        clazz.add_path_parameter(PathParameter(name, type, description, format))
        return clazz

    return decorator
