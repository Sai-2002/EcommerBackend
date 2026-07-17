import uuid
from abc import ABC, abstractmethod
from typing import Optional

from ..entities.payment import Payment


class PaymentRepositoryInterface(ABC):
    @abstractmethod
    def save(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def find_by_id(self, id: uuid.UUID) -> Optional[Payment]:
        pass

    @abstractmethod
    def find_by_order_id(self, order_id: uuid.UUID) -> Optional[Payment]:
        pass
