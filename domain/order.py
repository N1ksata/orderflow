from domain.order_item import OrderItem
from domain.order_status import OrderStatus
from datetime import datetime
from decimal import Decimal


class Order():
    _order_id : int
    _user_id : int
    _items : tuple[OrderItem, ...]
    _creation_time : datetime 
    _status : OrderStatus 
    _rejection_reason : str | None


    def __init__(self , order_id , user_id , items , creation_time):
        self._order_id = order_id
        self._user_id = user_id
        self._items = items
        self._creation_time = creation_time
        self._status = OrderStatus.PENDING
        self._rejection_reason = None
        self.__post_init__()

    def confirm(self):
        if self._status == OrderStatus.REJECTED:
            raise ValueError("The status is rejected!")

        if self._status == OrderStatus.PENDING:
            self._status = OrderStatus.CONFIRMED


    def reject(self , reason : str):

        if not isinstance(reason , str) or reason.strip() == "" :
            raise ValueError("The reason is either not string or its empty")

        if self._status == OrderStatus.CONFIRMED:
            raise ValueError("A confirmed order cannot be rejected.")

        if self._status == OrderStatus.REJECTED:
            if reason != self._rejection_reason:
                raise ValueError("You cannot change the reason")
            return 


        if self._status == OrderStatus.PENDING:
            self._rejection_reason = reason
            self._status = OrderStatus.REJECTED

    @property
    def order_id(self):
        return self._order_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def creation_time(self):
        return self._creation_time

    @property
    def status(self):
        return self._status
    
    @property 
    def rejection_reason(self):
        return self._rejection_reason

    @property
    def total(self):
        total_amount = Decimal("0.0")
        for item in self.items:
            total_amount += item.unit_price * item.quantity
        return total_amount

    @property 
    def items(self):
        return self._items

    
    
        

    def __post_init__(self):
    
        if type(self._order_id) is not int or self._order_id <= 0:
            raise ValueError("Order ID must be a positive integer.")
        if type(self._user_id) is not int or self._user_id <= 0:
            raise ValueError("User ID must be a positive integer.")
        if type(self._items) is not tuple or not self._items:
            raise ValueError("Items must be a non-empty tuple.")
        for x in self._items:
            if not isinstance(x, OrderItem):
                raise ValueError("Each item must be an OrderItem.")

        if not isinstance(self._creation_time , datetime ) or self._creation_time.utcoffset() is None:
            raise ValueError("Creation time must be a datetime with timezone information.")

        if self._status != OrderStatus.PENDING:
            raise ValueError("We need the status to be pending")

        if self._rejection_reason is not None:
            raise ValueError("A new order must not have a rejection reason.")

        seen_product_ids = set()
        for x in self._items:
            if x.product_id  in seen_product_ids:
                raise ValueError("Duplicate products are not allowed.")
            seen_product_ids.add(x.product_id)