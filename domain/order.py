from domain.order_item import OrderItem
from domain.order_status import OrderStatus
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Order():
    order_id : int
    user_id : int
    items : tuple[OrderItem, ...]
    creation_time : datetime 
    status : OrderStatus = OrderStatus.PENDING
    rejection_reason : str | None = None


    def __post_init__(self):
    
        if type(self.order_id) is not int or self.order_id <= 0:
            raise ValueError("Order ID must be a positive integer.")
        if type(self.user_id) is not int or self.user_id <= 0:
            raise ValueError("User ID must be a positive integer.")
        if type(self.items) is not tuple or not self.items:
            raise ValueError("Items must be a non-empty tuple.")
        for x in self.items:
            if not isinstance(x, OrderItem):
                raise ValueError("Each item must be an OrderItem.")