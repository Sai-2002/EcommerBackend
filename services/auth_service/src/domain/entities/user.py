import uuid
import re

class User:
    def __init__(self, email:str, password:str, id=None, isActive=True):
        self.id = uuid.uuid4()
        self.email = email
        self.password = password
        self.isActive = isActive

        self.validate()

    def validate(self):
        if not self.email or not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format")
        
        if not self.password or len(self.password) < 8:
            raise ValueError("Password must at least be 8 characters")
