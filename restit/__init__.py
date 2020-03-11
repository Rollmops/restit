__version__ = "0.1.0"

import sys

_DEFAULT_ENCODING = sys.getdefaultencoding()


def set_default_encoding(default_encoding: str):
    global _DEFAULT_ENCODING
    _DEFAULT_ENCODING = default_encoding


def get_default_encoding() -> str:
    global _DEFAULT_ENCODING
    return _DEFAULT_ENCODING
