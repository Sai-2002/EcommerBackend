import uuid


class Product:
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        stock_quantity: int,
        category_id=None,
        is_active: bool = True,
        id=None,
    ):
        self.id = id if id is not None else uuid.uuid4()
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity
        self.category_id = category_id
        self.is_active = is_active

        self.validate()

    def validate(self):
        if not self.name:
            raise ValueError("Product name cannot be empty")
        if self.price < 0:
            raise ValueError("Product price cannot be negative")
        if self.stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
