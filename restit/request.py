import json
from functools import lru_cache

import werkzeug.wrappers
from werkzeug.utils import escape

from restit import _DEFAULT_ENCODING


class Request(werkzeug.wrappers.Request):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query_parameters = {}
        self.body_as_dict = {}
        self._init()

    def _init(self):
        self.query_parameters = \
            self._create_dict_from_assignment_syntax(self.query_string.decode(encoding=_DEFAULT_ENCODING))
        if self.is_json():
            self.body_as_dict.update(json.loads(self.data.decode(encoding=_DEFAULT_ENCODING)))
        else:
            self.body_as_dict.update(dict(self.form))

    def is_json(self) -> bool:
        return self.content_type.lower() == "application/json"

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
