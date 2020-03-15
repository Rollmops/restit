from marshmallow import Schema, ValidationError

from restit.internal.request_body_properties import RequestBodyProperties
from restit.request import Request


class RequestBodySchemaDeserializer:
    @staticmethod
    def deserialize(request: Request, request_body_properties: RequestBodyProperties):
        schema_or_type = request_body_properties.get_schema_for_content_type(request.get_content_type())
        if isinstance(schema_or_type, Schema):
            body_as_dict = request.get_request_body_as_type(dict)

            try:
                request._body_type_cache[dict] = schema_or_type.load(body_as_dict)
            except (ValidationError, ValueError) as error:
                raise request_body_properties.validation_error_class(
                    f"Request body schema deserialization failed ({str(error)})"
                )
        else:
            body_as_string = request.get_request_body_as_type(str)
            try:
                request._body_type_cache[schema_or_type] = schema_or_type(body_as_string)
            except Exception as error:
                raise request_body_properties.validation_error_class(
                    f"Request body schema deserialization failed ({str(error)})"
                )
        request.get_request_body_as_type.cache_clear()
