from marshmallow import ValidationError
from marshmallow.fields import Field

from restit.internal.request_body_properties import RequestBodyProperties
from restit.internal.schema_or_field_deserializer import SchemaOrFieldDeserializer
from restit.request import Request


class RequestBodySchemaDeserializer:
    @staticmethod
    def deserialize(request: Request, request_body_properties: RequestBodyProperties):
        schema_or_field = request_body_properties.get_schema_for_content_type(request.content_type)
        _type = str if isinstance(schema_or_field, Field) else dict
        body = request.typed_body[_type]
        try:
            request.deserialized_body = SchemaOrFieldDeserializer.deserialize(body, schema_or_field)
        except (ValidationError, ValueError) as error:
            raise request_body_properties.validation_error_class(
                f"Request body schema deserialization failed ({str(error)})"
            )

