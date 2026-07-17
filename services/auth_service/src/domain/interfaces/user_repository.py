from typing import Optional
import uuid
from abc import ABC, abstractmethod
from ..entities.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self, user:User) -> User:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_id(self, id: uuid.UUID) -> Optional[User]:
        pass