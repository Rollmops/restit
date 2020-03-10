from werkzeug.datastructures import MIMEAccept

from restit import get_default_encoding
from restit.response_serializer import ResponseSerializer


class DefaultStrTextResponseSerializer(ResponseSerializer):
    def is_responsible_for_media_type(self, media_type: MIMEAccept) -> bool:
        return "text/plain" in media_type

    def is_responsible_for_response_data_type(self, response_data_type: type) -> bool:
        return response_data_type == str

    def serialize(self, response_input: str) -> bytes:
        return response_input.encode(encoding=get_default_encoding())

    def get_content_type(self) -> str:
        return "text/plain"
