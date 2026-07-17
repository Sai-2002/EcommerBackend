import uuid


class Category:
    def __init__(self, name: str, description: str = "", id=None):
        self.id = id if id is not None else uuid.uuid4()
        self.name = name
        self.description = description

        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("Category name cannot be empty")
