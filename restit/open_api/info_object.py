from restit.open_api.contact_object import ContactObject
from restit.open_api.license_object import LicenseObject


class InfoObject:
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
