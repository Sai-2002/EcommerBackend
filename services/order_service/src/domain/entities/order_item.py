import uuid


class OrderItem:
    def __init__(self, order_id: uuid.UUID, product_id: uuid.UUID, quantity: int, unit_price: float):
        self.id = uuid.uuid4()
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

        self.validate()

    def validate(self):
        if self.quantity <= 0:
            raise ValueError("quantity must be greater than 0")
        if self.unit_price < 0:
            raise ValueError("unit_price cannot be negative")
