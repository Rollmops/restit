import json

from werkzeug.datastructures import MIMEAccept

from restit import get_default_encoding
from restit.response_serializer import ResponseSerializer


class DefaultDictTextResponseSerializer(ResponseSerializer):
    def is_responsible_for_media_type(self, media_types: MIMEAccept) -> bool:
        return "text/plain" in media_types

    def is_responsible_for_response_data_type(self, response_data_type: type) -> bool:
        return response_data_type == dict

    def serialize(self, response_input: dict) -> bytes:
        return json.dumps(response_input).encode(encoding=get_default_encoding())

    def get_content_type(self) -> str:
        return "text/plain"
