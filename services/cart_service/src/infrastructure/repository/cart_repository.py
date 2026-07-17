import uuid
from typing import Optional

from sqlalchemy.orm import Session

from ..model.cart_item import CartItem as CartItemModel
from ...domain.interfaces.cart_repository import CartRepositoryInterface
from ...domain.entities.cart_item import CartItem as DomainCartItem


class CartRepository(CartRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, item: DomainCartItem) -> CartItemModel:
        db_item = CartItemModel()
        db_item.id = item.id
        db_item.user_id = item.user_id
        db_item.product_id = item.product_id
        db_item.quantity = item.quantity
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def find_by_user_id(self, user_id: uuid.UUID) -> list[CartItemModel]:
        return self.db.query(CartItemModel).filter(CartItemModel.user_id == user_id).all()

    def find_by_user_and_product(self, user_id: uuid.UUID, product_id: uuid.UUID) -> Optional[CartItemModel]:
        return (
            self.db.query(CartItemModel)
            .filter(CartItemModel.user_id == user_id, CartItemModel.product_id == product_id)
            .first()
        )

    def update_quantity(self, item_id: uuid.UUID, quantity: int) -> CartItemModel:
        db_item = self.db.query(CartItemModel).filter(CartItemModel.id == item_id).first()
        db_item.quantity = quantity
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, item_id: uuid.UUID) -> None:
        self.db.query(CartItemModel).filter(CartItemModel.id == item_id).delete()
        self.db.commit()

    def clear(self, user_id: uuid.UUID) -> None:
        self.db.query(CartItemModel).filter(CartItemModel.user_id == user_id).delete()
        self.db.commit()
