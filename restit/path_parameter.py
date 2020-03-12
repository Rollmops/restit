from typing import Type


class PathParameter:
    def __init__(self, name: str, description: str, type: Type):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return f"PathParameter(name='{self.name}', description='{self.description}', type={self.type})"
