class ContactObject:
    """`Contact <https://swagger.io/specification/#contactObject>`_ information for the exposed API.

    :param name: The identifying name of the contact person/organization
    :type name: str
    :param url: The URL pointing to the contact information. MUST be in the format of a URL
    :type url: str
    :param email: The email address of the contact person/organization. MUST be in the format of an email address
    :type email: str
    """

    def __init__(self, name: str, url: str, email: str):
        self.name = name
        self.url = url
        self.email = email

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "url": self.url,
            "email": self.email
        }
