import os
from http import HTTPStatus
from pathlib import Path
from typing import Union

from restit._response import Response
from restit.internal.suffix_media_type_mapping import SUFFIX_MEDIA_TYPE_MAPPING


class StaticFileResponse(Response):
    def __init__(
            self, file_path: Union[str, Path],
            status_code: Union[int, HTTPStatus] = HTTPStatus.OK,
            headers: dict = None,
            suffix: str = None
    ):
        headers = headers or {}
        suffix = suffix or StaticFileResponse._get_suffix_from_file_path(file_path)
        content_type = SUFFIX_MEDIA_TYPE_MAPPING.get(suffix, )
        headers.setdefault("Content-Type", content_type)

        with open(file_path, "rb") as fp:
            file_content = fp.read()

        super().__init__(file_content, status_code, headers)

    @staticmethod
    def _get_suffix_from_file_path(file_path: str) -> str:
        _, suffix = os.path.splitext(file_path)
        return suffix
