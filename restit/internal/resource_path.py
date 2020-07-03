import re
from typing import Tuple, Union, Dict, AnyStr, Match


class ResourcePath:
    _STRING_PATTERN = r"[\w\d_\-\s\$]+"
    _TYPE_MAPPING = {
        "int": (r"\d+", int),
        "integer": (r"\d+", int),
        "string": (_STRING_PATTERN, str),
        "str": (_STRING_PATTERN, str),
        None: (_STRING_PATTERN, str)
    }
    _PATH_PARAM_REGEX = re.compile(r":(\w+)(?:<(\w+)>)?")

    def __init__(self, request_mapping: str):
        self._request_mapping = request_mapping
        self._type_mapping = {}
        self._request_mapping_regex = self._transform_to_regex()

    def _transform_to_regex(self):
        regex_pattern = ResourcePath._PATH_PARAM_REGEX.sub(self._handle_path_param, self._request_mapping)
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
        match = self._request_mapping_regex.match(url)
        if match:
            match_dict = {
                param: self._type_mapping.get(param, str)(value)
                for param, value in match.groupdict().items()
            }
            return True, match_dict
        return False, None

    @staticmethod
    def generate_url_with_path_parameter_values(request_mapping: str, path_param: dict) -> str:
        def _replace_with_path_param(match: Match):
            key = match.group(1)
            try:
                value = str(path_param[key])
            except KeyError:
                raise ResourcePath.ExpectedPathParameterForRequestMappingNotFoundException(
                    f"The path parameter {key} in request mapping '{request_mapping}' was not found in the provided "
                    f"path parameters {path_param}"
                )
            return value

        return ResourcePath._PATH_PARAM_REGEX.sub(_replace_with_path_param, request_mapping)

    class UnknownPathParamTypeAnnotation(Exception):
        pass

    class ExpectedPathParameterForRequestMappingNotFoundException(Exception):
        pass
