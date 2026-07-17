import uuid
from typing import Optional
from sqlalchemy.orm import Session

from ..model.order import Order as OrderModel
from ..model.order_item import OrderItem as OrderItemModel
from ...domain.interfaces.order_repository import OrderRepositoryInterface
from ...domain.entities.order import Order as DomainOrder


class OrderRepository(OrderRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, order: DomainOrder) -> OrderModel:
        db_order = OrderModel()
        db_order.id = order.id
        db_order.user_id = order.user_id
        db_order.status = order.status
        db_order.total_amount = order.total_amount
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def find_by_id(self, id: uuid.UUID) -> Optional[OrderModel]:
        return self.db.query(OrderModel).filter(OrderModel.id == id).first()

    def find_by_user_id(self, user_id: uuid.UUID) -> list[OrderModel]:
        return self.db.query(OrderModel).filter(OrderModel.user_id == user_id).all()

    def update_status(self, id: uuid.UUID, status: str) -> OrderModel:
        db_order = self.db.query(OrderModel).filter(OrderModel.id == id).first()
        db_order.status = status
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def save_items(self, order_id: uuid.UUID, items: list[dict]) -> None:
        for item in items:
            db_item = OrderItemModel()
            db_item.id = uuid.uuid4()
            db_item.order_id = order_id
            db_item.product_id = uuid.UUID(str(item["product_id"]))
            db_item.quantity = item["quantity"]
            db_item.unit_price = item["unit_price"]
            self.db.add(db_item)
        self.db.commit()
