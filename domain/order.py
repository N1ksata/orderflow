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

        if not isinstance(self.creation_time , datetime ) or self.creation_time.utcoffset() is None:
            raise ValueError("Creation time must be a datetime with timezone information.")

        if self.status != OrderStatus.PENDING:
            raise ValueError("We need the status to be pending")

        if self.rejection_reason is not None:
            raise ValueError("A new order must not have a rejection reason.")

        seen_product_ids = set()
        for x in self.items:
            if x.product_id  in seen_product_ids:
                raise ValueError("Duplicate products are not allowed.")
            seen_product_ids.add(x.product_id)