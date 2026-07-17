from typing import Optional
import uuid
from abc import ABC, abstractmethod
from ..entities.product import Product


class ProductRepositoryInterface(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product:
        pass

    @abstractmethod
    def find_by_id(self, id: uuid.UUID) -> Optional[Product]:
        pass

    @abstractmethod
    def find_all(self) -> list:
        pass

    @abstractmethod
    def find_by_category(self, category_id: uuid.UUID) -> list:
        pass

    @abstractmethod
    def update(self, product: Product) -> Product:
        pass

    @abstractmethod
    def delete(self, id: uuid.UUID) -> None:
        pass
