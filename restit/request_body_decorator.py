import logging
from typing import Dict, Union, Type

from marshmallow import Schema
from werkzeug.exceptions import UnprocessableEntity

from restit.internal.request_body_parameter import RequestBodyParameter

LOGGER = logging.getLogger(__name__)


def request_body(
        content_type_schemas: Dict[str, Union[Schema, Type]],
        description: str,
        required: bool = True,
        validation_error_class=UnprocessableEntity
):
    def decorator(func):
        request_body_parameter = RequestBodyParameter(
            content_type_schemas, description, required, validation_error_class
        )
        LOGGER.debug(
            "Registering request body parameter %s for %s", request_body_parameter, func.__name__
        )
        setattr(func, "__request_body_parameter__", request_body_parameter)
        return func

    return decorator
