import uuid
from typing import Optional
from abc import ABC, abstractmethod
from ..entities.order import Order


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_by_id(self, id: uuid.UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: uuid.UUID) -> list[Order]:
        pass

    @abstractmethod
    def update_status(self, id: uuid.UUID, status: str) -> Order:
        pass
