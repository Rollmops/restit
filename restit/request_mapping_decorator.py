import logging
from typing import Type, List

from restit.exception import PathIsNotStartingWithSlashException
from restit.path_parameter import PathParameter
from restit.path_parameter_decorator import register_path_parameter
from restit.resource import Resource

LOGGER = logging.getLogger(__name__)


def request_mapping(path: str, path_parameters: List[PathParameter] = None):
    """Maps a resource *URI* path to your resource.

    The path can contain multiple path parameters.

    Example:

    .. code-block:: python

        @request_mapping("/users/:id")
        class UserResource(Resource):
            ...

    Or:

    .. code-block:: python

        @request_mapping("/orders/:year/:month/:id")
        class OrdersResource(Resource):
            ...

    .. note::

        A specific request mapping paths will always win. So given the following two request mapping paths:

            - ``/orders/api``
            - ``/orders/:id``

        The incoming path ``/orders/api`` will always map to the resource with the ``/orders/api`` request mapping path.

    **Setting** `OpenApi <https://swagger.io/docs/specification/about/>`_ **properties**

    There are two ways of setting the path parameter properties for the *OpenApi* documentation.

        1. Using the :func:`~restit.path_parameter_decorator.path_parameter` decorator

        2. Passing a list of :class:`~restit.PathParameter` instances to the ``path_parameter`` parameter of the :func:`request_mapping` decorator


    Example for 2.:

    .. code-block:: python

        from marshmallow import fields

        ...

        @request_mapping(
            "/users/:id",
            [
                PathParameter("id", "The user id", fields.Integer())
            ]
        )
        class UserResource(Resource):
            ...


    As you can see, we are using the `marshmallow <https://marshmallow.readthedocs.io/en/stable/#>`_ library here.

    :param path: The *URI* path to the resource
    :type path: str
    :param path_parameters: Optional list of path parameter properties used to generate the
        `OpenApi <https://swagger.io/docs/specification/about/>`_ documentation.
        Can also be set using the :func:`~restit.path_parameter_decorator.path_parameter` decorator.
    :type path_parameters: List[PathParameter]
    """
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

