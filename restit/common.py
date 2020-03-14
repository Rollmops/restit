import os
import sys
from html import escape

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
            pair.split("=") for pair in request_input_string.strip(group_delimiter).split(group_delimiter)
        ]
    }
