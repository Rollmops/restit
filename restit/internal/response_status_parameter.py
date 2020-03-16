from http import HTTPStatus
from typing import Union, Dict, Type

from marshmallow import Schema


class ResponseStatusParameter:
    def __init__(
            self, status: Union[int, HTTPStatus, None], description: str, content_types: Dict[str, Union[Schema, Type]]
    ):
        self.status: int = status if isinstance(status, int) or status is None else status.value
        self.description = description
        self.content_types = content_types
