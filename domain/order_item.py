import decimal
from dataclasses import dataclass 

@dataclass(frozen=True)
class OrderItem:

    product_id: int
    quantity: int
    unit_price: decimal.Decimal

    def __post_init__(self):

        if type(self.quantity) is not int or self.quantity <= 0:  #we need quantity -> int  and positive number
            raise ValueError("Quantity must be a positive integer.")
            
        if type(self.unit_price) is not decimal.Decimal or not self.unit_price.is_finite() or self.unit_price <= 0:
            raise ValueError("Unit price must be a finite, positive Decimal.")
        
        if type(self.product_id) is not int or self.product_id <= 0:
            raise ValueError("Product ID must be a positive integer.")

