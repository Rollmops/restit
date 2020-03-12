import os
import sys

_DEFAULT_ENCODING = sys.getdefaultencoding()


def set_default_encoding(default_encoding: str):
    global _DEFAULT_ENCODING
    _DEFAULT_ENCODING = default_encoding


def get_default_encoding() -> str:
    global _DEFAULT_ENCODING
    return _DEFAULT_ENCODING


def get_open_api_resource_path() -> str:
    import restit
    path = os.path.join(restit.__path__[0], "open_api")
    assert os.path.isdir(path)
    return path
