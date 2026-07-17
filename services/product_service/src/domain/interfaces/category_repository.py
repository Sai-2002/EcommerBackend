from typing import Optional
import uuid
from abc import ABC, abstractmethod
from ..entities.category import Category


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def find_by_id(self, id: uuid.UUID) -> Optional[Category]:
        pass

    @abstractmethod
    def find_all(self) -> list:
        pass
