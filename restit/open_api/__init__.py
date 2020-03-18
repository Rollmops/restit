from .contact_object import ContactObject
from .info_object import InfoObject
from .license_object import LicenseObject
from .open_api_documentation import OpenApiDocumentation


def reusable_schema(clazz):
    setattr(clazz, "__reusable_schema__", True)
    return clazz
