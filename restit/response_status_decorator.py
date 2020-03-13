import logging
from http import HTTPStatus
from typing import Dict, Union, List, Type

from marshmallow import Schema

from restit.internal.response_status_parameter import ResponseStatusParameter

LOGGER = logging.getLogger(__name__)


# noinspection PyShadowingBuiltins
def response_status(status: Union[int, HTTPStatus], description: str, content_types: Dict[str, Union[Schema, Type]]):
    def decorator(func):
        http_status_code = status if isinstance(status, int) else status.value
        response_status_parameter = ResponseStatusParameter(http_status_code, description, content_types)

        registered_response_status_parameters: List[ResponseStatusParameter] = \
            getattr(func, "__response_status_parameters__", [])
        LOGGER.debug(
            "Registering response status parameter %s for %s", response_status_parameter, func.__name__
        )
        registered_response_status_parameters.append(response_status_parameter)
        setattr(func, "__response_status_parameters__", registered_response_status_parameters)
        return func

    return decorator
