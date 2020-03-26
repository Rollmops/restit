from restit.open_api.contact_object import ContactObject
from restit.open_api.license_object import LicenseObject


class InfoObject:
    """Holds the `OpenApi`_ documentation `InfoObject <https://swagger.io/specification/#infoObject>`_.

    The object provides metadata about the API. The metadata MAY be used by the clients if needed, and MAY be
    presented in editing or documentation generation tools for convenience.

    :param title: The title of the API
    :type title: str
    :param version: The version of the OpenAPI document
    :type version: str
    :param description: A short description of the API. `CommonMark <https://spec.commonmark.org/>`_ syntax MAY be
        used for rich text representation
    :type description: str
    :param terms_of_service: A URL to the Terms of Service for the API. MUST be in the format of a URL
    :type terms_of_service: str
    :param contact: The contact information for the exposed API
    :type contact: ContactObject
    :param license: The license information for the exposed API
    :type license: LicenseObject
    """

    def __init__(
            self,
            title: str,
            version: str,
            description: str = None,
            terms_of_service: str = None, contact: ContactObject = None, license: LicenseObject = None):
        self.title = title
        self.version = version
        self.description = description
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license = license

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "version": self.version,
            "description": self.description,
            "termsOfService": self.terms_of_service,
            "contact": self.contact.to_dict() if self.contact else None,
            "license": self.license.to_dict() if self.license else None
        }
