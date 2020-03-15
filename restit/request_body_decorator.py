import logging
from typing import Dict, Union, Type

from marshmallow import Schema
from werkzeug.exceptions import UnprocessableEntity

from restit.internal.request_body_properties import RequestBodyProperties

LOGGER = logging.getLogger(__name__)


def request_body(
        content_types: Dict[str, Union[Schema, Type]],
        description: str,
        required: bool = True,
        validation_error_class=UnprocessableEntity
):
    def decorator(func):
        request_body_properties = RequestBodyProperties(
            content_types, description, required, validation_error_class
        )
        LOGGER.debug(
            "Registering request body parameter %s for %s", request_body_properties, func.__name__
        )
        setattr(func, "__request_body_properties__", request_body_properties)
        return func

    return decorator
