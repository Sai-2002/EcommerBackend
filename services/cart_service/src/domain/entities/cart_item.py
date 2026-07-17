import uuid


class CartItem:
    def __init__(self, user_id: uuid.UUID, product_id: uuid.UUID, quantity: int = 1, id=None):
        self.id = id if id is not None else uuid.uuid4()
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

        self.validate()

    def validate(self):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
