import os
from pathlib import Path
from typing import Union

from restit._response import Response
from restit.internal.suffix_media_type_mapping import SUFFIX_MEDIA_TYPE_MAPPING
from restit.request import Request
from restit.resource import Resource


class StaticDirectoryResource(Resource):
    def __init__(self, path: str, static_directory_path: Union[str, Path], entry_file: str = None):
        super().__init__()
        self.__request_mapping__ = path.rstrip("/") + r"/?(?P<file_name>\S*)"
        self.static_directory_path = static_directory_path
        self.entry_file = entry_file or "index.html"

    def get(self, request: Request) -> Response:
        file_name = request.path_parameters["file_name"] or self.entry_file

        file_path = os.path.join(self.static_directory_path, file_name)
        with open(file_path, "rb") as fp:
            file_content = fp.read()

        _, suffix = os.path.splitext(file_name)
        content_type = SUFFIX_MEDIA_TYPE_MAPPING.get(suffix, )

        return Response(file_content, headers={"Content-Type": content_type})
