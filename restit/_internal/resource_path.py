import re
from typing import Tuple, Union, Dict, AnyStr, Match


class ResourcePath:
    _TYPE_MAPPING = {
        "int": (r"\d+", int),
        "integer": (r"\d+", int),
        "string": (r"\S+", str),
        "str": (r"\S+", str),
        None: (r"\S+", str)
    }

    def __init__(self, resource_path: str):
        self._resource_path = resource_path
        self._type_mapping = {}
        self._resource_path_regex = self._transform_to_regex()

    def _transform_to_regex(self):
        path_param_pattern = r"<(\w+)(?:\:(\w+))?>"
        regex_pattern = re.sub(path_param_pattern, self._handle_path_param, self._resource_path)
        regex_pattern = "^" + regex_pattern + "$"
        return re.compile(regex_pattern)

    def _handle_path_param(self, match: Match) -> str:
        self._type_mapping[match.group(1)] = \
            ResourcePath._TYPE_MAPPING.get(match.group(2), ResourcePath._TYPE_MAPPING["str"])[1]
        try:
            return f"(?P<{match.group(1)}>" + ResourcePath._TYPE_MAPPING[match.group(2)][0] + ")"
        except KeyError:
            raise ResourcePath.UnknownPathParamTypeAnnotation(match.group(2))

    def get_match(self, url: str) -> Tuple[bool, Union[None, Dict[str, AnyStr]]]:
        match = self._resource_path_regex.match(url)
        if match:
            match_dict = {param: self._type_mapping[param](value) for param, value in match.groupdict().items()}
            return True, match_dict
        return False, None

    class UnknownPathParamTypeAnnotation(Exception):
        pass
