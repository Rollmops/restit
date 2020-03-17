from restit.internal.mime_type import MIMEType
from restit.internal.request_deserializer_service import RequestDeserializerService


class TypedBody:
    def __init__(self, body: bytes, content_type: MIMEType):
        self.body = body
        self.content_type = content_type
        self.cache = {}

    def __getitem__(self, python_type: type):
        value = self.cache.get(
            python_type,
            RequestDeserializerService.deserialize_request_body(self.body, self.content_type, python_type)
        )
        self.cache[python_type] = value
        return value
