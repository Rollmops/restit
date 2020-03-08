import json
from json import JSONDecodeError

from restit import DEFAULT_ENCODING
from restit._internal.common import create_dict_from_query_parameter_syntax


class Request:
    def __init__(self, query_parameters: dict, wsgi_environment: dict = None, body: bytes = None):
        self.query_parameters = query_parameters
        self.wsgi_environment = wsgi_environment
        self.body: bytes = body or b""
        self.body_as_json: dict = {}
        self.__set_body_as_json()

    def __set_body_as_json(self):
        body_as_string = self.body.decode(encoding=DEFAULT_ENCODING)
        try:
            self.body_as_json = json.loads(body_as_string)
        except JSONDecodeError:
            self.body_as_json = create_dict_from_query_parameter_syntax(body_as_string)
