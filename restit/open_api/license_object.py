class LicenseObject:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "url": self.url
        }
