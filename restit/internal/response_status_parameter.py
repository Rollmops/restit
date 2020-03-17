from http import HTTPStatus
from typing import Union, Dict

from marshmallow import Schema
from marshmallow.fields import Field


class ResponseStatusParameter:
    def __init__(
            self, status: Union[int, HTTPStatus, None], description: str, content_types: Dict[str, Union[Schema, Field]]
    ):
        self.status: int = status if isinstance(status, int) or status is None else status.value
        self.description = description
        self.content_types = content_types
        self._check_request_properties_schema_type()

    def _check_request_properties_schema_type(self):
        for schema_or_field in self.content_types.values():
            if not isinstance(schema_or_field, (Field, Schema)):
                raise ResponseStatusParameter.UnsupportedSchemaTypeException(type(schema_or_field))

    class UnsupportedSchemaTypeException(Exception):
        pass
