import json
from functools import lru_cache

import werkzeug.wrappers
from werkzeug.datastructures import MIMEAccept
from werkzeug.utils import escape

from restit import _DEFAULT_ENCODING


class Request:
    def __init__(self, wsgi_environment: dict):
        self._extended_request_info = werkzeug.wrappers.Request(wsgi_environment)
        self.query_parameters = {}
        self._body_as_dict = {}
        self._init()

    def _init(self):
        self.query_parameters = \
            self._create_dict_from_assignment_syntax(
                self._extended_request_info.query_string.decode(encoding=_DEFAULT_ENCODING)
            )
        if self.is_json():
            self._body_as_dict.update(json.loads(self._extended_request_info.data.decode(encoding=_DEFAULT_ENCODING)))
        else:
            self._body_as_dict.update(dict(self._extended_request_info.form))

    def is_json(self) -> bool:
        return self._extended_request_info.content_type.lower() == "application/json"

    def get_extended_request_info(self) -> werkzeug.wrappers.Request:
        return self._extended_request_info

    def get_path(self) -> str:
        return self._extended_request_info.path

    def get_accepted_media_types(self) -> MIMEAccept:
        return self._extended_request_info.accept_mimetypes

    def get_request_method_name(self) -> str:
        return self._extended_request_info.method

    def get_body_as_dict(self) -> dict:
        return self._body_as_dict

    @staticmethod
    @lru_cache()
    def _create_dict_from_assignment_syntax(assignment_syntax_data: str) -> dict:
        return_dict = {}
        if assignment_syntax_data is None or "=" not in assignment_syntax_data:
            return return_dict
        for query_string_pair in assignment_syntax_data.split("&"):
            try:
                key, value = query_string_pair.split("=")
                return_dict[key] = escape(value)
            except ValueError:
                pass

        return return_dict
