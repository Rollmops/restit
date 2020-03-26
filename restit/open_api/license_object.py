class LicenseObject:
    """`License <https://swagger.io/specification/#licenseObject>`_ information for the exposed API.

    :param name: The license name used for the API
    :type name: str
    :param url: A URL to the license used for the API. MUST be in the format of a URL
    :type url: str
    """

    def __init__(self, name: str, url: str = None):
        self.name = name
        self.url = url

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "url": self.url
        }
