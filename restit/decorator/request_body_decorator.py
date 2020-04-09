import logging
from typing import Dict, Union

from marshmallow import Schema
from marshmallow.fields import Field

from restit.exception import UnprocessableEntity
from restit.internal.request_body_properties import RequestBodyProperties

LOGGER = logging.getLogger(__name__)


def request_body(
        content_types: Dict[str, Union[Schema, Field]],
        description: str,
        required: bool = True,
        validation_error_class=UnprocessableEntity
):
    """Describe an expected request body for a method


    :param content_types: A dictionary that maps a *Content-Type* with a *marshmallow* schema or a field.
    :type content_types: Dict[str, Union[marshmallow.Schema, marshmallow.fields.Field]
    :param description: The description of the request body
    :type description: str
    :param required: Is the request body required?
    :type required: bool
    :param validation_error_class: An error class either that should be raised if either the schema validation
        fails or the request body is missing.
    :type validation_error_class: An instance of type Exception
    """

    def decorator(func):
        request_body_properties = RequestBodyProperties(
            content_types, description, required, validation_error_class
        )
        LOGGER.debug(
            "Registering request body parameter %s for resource %s", request_body_properties, func.__name__
        )
        setattr(func, "__request_body_properties__", request_body_properties)
        return func

    return decorator
