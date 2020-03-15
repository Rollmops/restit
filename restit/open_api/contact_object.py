class ContactObject:
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
