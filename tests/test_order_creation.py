from domain.order import Order
from domain.order_item import OrderItem
from domain.order_status import OrderStatus
from datetime import timezone,datetime 
from decimal import Decimal
import pytest



def test_order_creation():
    item = OrderItem(1 , 2 , Decimal("50.00"))

    order = Order( 1 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc) )

    assert order.order_id == 1
    assert order.user_id == 5
    assert order.items == (item,)
    assert order.creation_time == datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc)
    assert order.status is OrderStatus.PENDING
    assert order.rejection_reason is None


def test_order_rejects_empty_items():
    with pytest.raises(ValueError):
        Order(1 , 2 ,(),datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))


def test_order_rejects_invalid_item():
    with pytest.raises(ValueError):
        Order(1 , 2 ,(1 , ),datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))


def test_order_rejects_naive_creation_time():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    
    with pytest.raises(ValueError):
        Order(1 , 2 ,(item , ),datetime(2026, 10, 24, 15, 30))


def test_order_rejects_string_creation_time():
    item = OrderItem(1 , 2 , Decimal("50.00"))

    with pytest.raises(ValueError):
        Order(1 , 2 ,(item , ),"Hello") #datetime is string 


def test_order_rejects_confirmed_status():
    with pytest.raises(ValueError):
        item = OrderItem(1 , 2 , Decimal("50.00"))

        Order(1 , 2 ,(item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc) , status=OrderStatus.CONFIRMED)


def test_order_rejects_pending_order_with_rejection_reason():
    item = OrderItem(1 , 2 , Decimal("50.00"))

    with pytest.raises(ValueError):
        Order(1 , 2 ,(item , ), datetime(2026, 10, 24, 15, 30, tzinfo=timezone.utc) ,rejection_reason = "out of stock")


def test_order_rejects_zero_order_id():
    item = OrderItem(1 , 2 , Decimal("50.00"))

    with pytest.raises(ValueError):
        Order( 0 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc) )
    


def test_order_rejects_zero_user_id():
    item = OrderItem(1 , 2 , Decimal("50.00"))

    with pytest.raises(ValueError):
        Order( 1 , 0 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc) )


def test_order_rejects_duplicate_products():
    item1= OrderItem(1 , 2 , Decimal("50.00"))
    item2 = OrderItem(1 , 2 , Decimal("50.00"))

    with pytest.raises(ValueError):
        Order( 1 , 5 , (item1 , item2 , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc) )


def test_order_accepts_distinct_products():
    item1= OrderItem(1 , 2 , Decimal("50.00"))
    item2 = OrderItem(2 , 1 , Decimal("50.00"))
    order = Order( 1 , 5 , (item1 , item2 , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc) )

    assert order.items == (item1 , item2)