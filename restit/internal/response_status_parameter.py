import json
from http import HTTPStatus
from typing import Union, Dict, Type

from marshmallow import Schema

from restit.response import Response


class ResponseStatusParameter:
    def __init__(self, status: Union[int, HTTPStatus], description: str, content_types: Dict[str, Union[Schema, Type]]):
        self.status = status if isinstance(status, int) else status.value
        self.description = description
        self.content_types = content_types

    def validate(self, response: Response) -> Response:
        schema_or_type = self._find_schema_for_content_type(response)
        if isinstance(schema_or_type, Schema):
            response.text = json.dumps(schema_or_type.dumps())

        return response

    def _find_schema_for_content_type(self, response: Response) -> Union[Schema, Type]:
        try:
            return self.content_types[response.get_content_type()]
        except KeyError:
            raise Exception(
                f"Response content type {response.get_content_type()} is not supported, "
                f"supported are: {self.content_types.keys()} "
            )
