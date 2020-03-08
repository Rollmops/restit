from functools import lru_cache
from html import escape


@lru_cache()
def create_dict_from_query_parameter_syntax(query_string: str) -> dict:
    query_parameters = {}
    if query_string is None or "=" not in query_string:
        return query_parameters
    for query_string_pair in query_string.split("&"):
        try:
            key, value = query_string_pair.split("=")
            query_parameters[key] = escape(value)
        except ValueError:
            pass

    return query_parameters
