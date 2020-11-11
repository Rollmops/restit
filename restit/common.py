import os
import sys
from copy import deepcopy
from functools import lru_cache
from html import escape
from typing import List

from restit.internal.response_status_parameter import ResponseStatusParameter

_DEFAULT_ENCODING = sys.getdefaultencoding()


def set_default_encoding(default_encoding: str):
    global _DEFAULT_ENCODING
    _DEFAULT_ENCODING = default_encoding


def get_default_encoding() -> str:
    global _DEFAULT_ENCODING
    return _DEFAULT_ENCODING


def get_open_api_resource_path() -> str:
    import restit
    path = os.path.join(restit.__path__[0], "resource", "swagger")
    assert os.path.isdir(path)
    return path


def create_dict_from_assignment_syntax(request_input_string: str, group_delimiter: str = "&") -> dict:
    if request_input_string is None or "=" not in request_input_string:
        return {}

    return {
        key: escape(value) for key, value in [
            pair.split("=") for pair in request_input_string.strip(group_delimiter + " ").split(group_delimiter)
        ]
    }


def guess_text_content_subtype_bytes(content: bytes) -> str:
    if b"<html>" in content or b"<title>" in content or b"<body>" in content:
        return "text/html"

    return "text/plain"


def guess_text_content_subtype_string(content: str) -> str:
    if "<html>" in content or "<title>" in content or "<body>" in content:
        return "text/html"

    return "text/plain"


@lru_cache()
def get_response_status_parameters_for_method(method_object: object) -> List[ResponseStatusParameter]:
    response_status_parameters = deepcopy(getattr(method_object.__self__, "__response_status_parameters__", []))
    response_status_parameters.extend(getattr(method_object, "__response_status_parameters__", []))
    return response_status_parameters


@lru_cache()
def get_exception_mapping_for_method(method_object: object) -> dict:
    exception_mapping: dict = deepcopy(getattr(method_object.__self__, "__exception_mapping__", {}))
    exception_mapping.update(getattr(method_object, "__exception_mapping__", {}))
    return exception_mapping
