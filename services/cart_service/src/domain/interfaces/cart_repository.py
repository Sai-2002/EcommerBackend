import uuid
from abc import ABC, abstractmethod
from typing import Optional

from ..entities.cart_item import CartItem


class CartRepositoryInterface(ABC):

    @abstractmethod
    def save(self, item: CartItem) -> CartItem:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: uuid.UUID) -> list[CartItem]:
        pass

    @abstractmethod
    def find_by_user_and_product(self, user_id: uuid.UUID, product_id: uuid.UUID) -> Optional[CartItem]:
        pass

    @abstractmethod
    def update_quantity(self, item_id: uuid.UUID, quantity: int) -> CartItem:
        pass

    @abstractmethod
    def delete(self, item_id: uuid.UUID) -> None:
        pass

    @abstractmethod
    def clear(self, user_id: uuid.UUID) -> None:
        pass
