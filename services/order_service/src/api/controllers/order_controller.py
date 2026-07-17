from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session

from ...infrastructure.session import get_db
from ...infrastructure.repository.order_repository import OrderRepository
from ...application.use_cases.create_order import CreateOrderUseCase
from ...application.use_cases.get_order import GetOrderUseCase
from ...application.use_cases.list_user_orders import ListUserOrdersUseCase
from ...application.use_cases.update_order_status import UpdateOrderStatusUseCase
from ..validators.order_validator import CreateOrderRequest, UpdateOrderStatusRequest


class OrderController:

    def create_order(self, request: CreateOrderRequest, db: Session = Depends(get_db)):
        repo = OrderRepository(db)
        use_case = CreateOrderUseCase(repo)
        items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
            }
            for item in request.items
        ]
        result = use_case.execute(user_id=str(request.user_id), items=items)
        return result

    def get_order(self, order_id: UUID, db: Session = Depends(get_db)):
        repo = OrderRepository(db)
        use_case = GetOrderUseCase(repo)
        result = use_case.execute(order_id=order_id)
        return result

    def list_user_orders(self, user_id: UUID, db: Session = Depends(get_db)):
        repo = OrderRepository(db)
        use_case = ListUserOrdersUseCase(repo)
        result = use_case.execute(user_id=user_id)
        return result

    def update_order_status(self, order_id: UUID, request: UpdateOrderStatusRequest, db: Session = Depends(get_db)):
        repo = OrderRepository(db)
        use_case = UpdateOrderStatusUseCase(repo)
        result = use_case.execute(order_id=order_id, status=request.status)
        return result
