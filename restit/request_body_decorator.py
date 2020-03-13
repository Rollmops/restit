import logging

from marshmallow import Schema
from werkzeug.exceptions import UnprocessableEntity

from restit.internal.request_body_parameter import RequestBodyParameter

LOGGER = logging.getLogger(__name__)


def request_body(schema: Schema, validation_error_class=UnprocessableEntity):
    def decorator(func):
        request_body_parameter = RequestBodyParameter(schema, validation_error_class)
        LOGGER.debug(
            "Registering request body parameter %s for %s", request_body_parameter, func.__name__
        )
        setattr(func, "__request_body_parameter__", request_body_parameter)
        return func

    return decorator
