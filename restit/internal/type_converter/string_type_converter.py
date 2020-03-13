from typing import Type, List, Union

from restit.common import get_default_encoding


class StringTypeConverter:
    @staticmethod
    def convert(string_or_bytes: Union[str, bytes], into_type: Type):
        if isinstance(string_or_bytes, bytes):
            string_or_bytes = string_or_bytes.decode(get_default_encoding())
        if into_type == list:
            return StringTypeConverter._convert_iterable(string_or_bytes, str, "[]", list)
        try:
            return into_type(string_or_bytes)
        except TypeError:
            return StringTypeConverter._convert_advanced_types(string_or_bytes, into_type)

    @staticmethod
    def _convert_advanced_types(string: str, into_type: Type):
        if getattr(into_type, "_name", None) == "List" or getattr(into_type, "_gorg", None) == List:
            # noinspection PyUnresolvedReferences
            return StringTypeConverter._convert_iterable(string, into_type.__args__[0], "[]", list)

    @staticmethod
    def _convert_iterable(string: str, list_type, to_strip: str, result_type):
        return result_type([list_type(elem) for elem in string.strip(f" {to_strip}").split(",")])
