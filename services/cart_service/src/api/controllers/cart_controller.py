import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from ...infrastructure.session import get_db
from ...infrastructure.repository.cart_repository import CartRepository
from ...application.use_cases.add_to_cart import AddToCartUseCase
from ...application.use_cases.get_cart import GetCartUseCase
from ...application.use_cases.update_cart_item import UpdateCartItemUseCase
from ...application.use_cases.remove_from_cart import RemoveFromCartUseCase
from ...application.use_cases.clear_cart import ClearCartUseCase
from ..validators.cart_validator import AddToCartRequest, UpdateCartItemRequest


class CartController:

    def add_to_cart(self, request: AddToCartRequest, db: Session = Depends(get_db)):
        repository = CartRepository(db)
        use_case = AddToCartUseCase(repository)
        return use_case.execute(
            user_id=str(request.user_id),
            product_id=str(request.product_id),
            quantity=request.quantity,
        )

    def get_cart(self, user_id: uuid.UUID, db: Session = Depends(get_db)):
        repository = CartRepository(db)
        use_case = GetCartUseCase(repository)
        return use_case.execute(user_id=str(user_id))

    def update_cart_item(self, item_id: uuid.UUID, request: UpdateCartItemRequest, db: Session = Depends(get_db)):
        repository = CartRepository(db)
        use_case = UpdateCartItemUseCase(repository)
        return use_case.execute(item_id=str(item_id), quantity=request.quantity)

    def remove_from_cart(self, item_id: uuid.UUID, db: Session = Depends(get_db)):
        repository = CartRepository(db)
        use_case = RemoveFromCartUseCase(repository)
        use_case.execute(item_id=str(item_id))
        return {"message": "Item removed from cart"}

    def clear_cart(self, user_id: uuid.UUID, db: Session = Depends(get_db)):
        repository = CartRepository(db)
        use_case = ClearCartUseCase(repository)
        use_case.execute(user_id=str(user_id))
        return {"message": "Cart cleared"}
