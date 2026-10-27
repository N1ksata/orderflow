from domain.order import Order
from domain.order_item import OrderItem
from domain.order_status import OrderStatus
from datetime import datetime, timezone
from decimal import Decimal
import pytest

def test_order_confirm_changes_pending_to_confirmed():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    order = Order(1 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))

    order.confirm()

    assert order.status == OrderStatus.CONFIRMED
    assert order.rejection_reason is None


def test_order_confirm_is_idempotent():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    order = Order(1 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))
    
    order.confirm()
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED
    assert order.rejection_reason is None


def test_order_reject_changes_pending_to_rejected():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    order = Order(1 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))


    order.reject("out of stock")

    assert order.status == OrderStatus.REJECTED
    assert order.rejection_reason == "out of stock"


def test_order_cannot_confirm_rejected_order():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    order = Order(1 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))

    order.reject("out of stock")

    with pytest.raises(ValueError):
        order.confirm()

    assert order.status == OrderStatus.REJECTED
    assert order.rejection_reason == "out of stock"


def test_order_cannot_reject_confirmed_order():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    order = Order(1 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))

    order.confirm()

    with pytest.raises(ValueError):
        order.reject("out of stock")

    assert order.status == OrderStatus.CONFIRMED
    assert order.rejection_reason is None


def test_order_reject_rejects_blank_reason():
    item = OrderItem(1,2 ,Decimal("50.00"))
    order = Order(1 , 5 , (item , ) , datetime(2026 , 10 , 24 , 15 , 30 , tzinfo = timezone.utc))

    
    with pytest.raises(ValueError):
        order.reject(" ")

    assert order.status == OrderStatus.PENDING
    assert order.rejection_reason is None


def test_order_reject_rejects_empty_reason():
    item = OrderItem(1,2 ,Decimal("50.00"))
    order = Order(1 , 5 , (item , ) , datetime(2026 , 10 , 24 , 15 , 30 , tzinfo = timezone.utc))
    
        
    with pytest.raises(ValueError):
        order.reject("")
    
    assert order.status == OrderStatus.PENDING
    assert order.rejection_reason is None

def test_order_reject_rejects_non_string_reason():
    item = OrderItem(1,2 ,Decimal("50.00"))
    order = Order(1 , 5 , (item , ) , datetime(2026 , 10 , 24 , 15 , 30 , tzinfo = timezone.utc))
    
        
    with pytest.raises(ValueError):
        order.reject(123)
    
    assert order.status == OrderStatus.PENDING
    assert order.rejection_reason is None


def test_order_reject_is_idempotent():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    order = Order(1 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))

    order.reject("out of stock")
    order.reject("out of stock")


    assert order.status == OrderStatus.REJECTED
    assert order.rejection_reason == "out of stock"


def test_order_reject_cannot_change_existing_reason():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    order = Order(1 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))
    
    order.reject("out of stock")
    with pytest.raises(ValueError):
        order.reject("don't have money")

    assert order.status == OrderStatus.REJECTED
    assert order.rejection_reason == "out of stock"


def test_order_blocks_direct_status_assignment():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    order = Order(1 , 5 , (item , ), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))
    with pytest.raises(AttributeError):
        order.status = OrderStatus.CONFIRMED

    assert order.status == OrderStatus.PENDING

def test_order_blocks_direct_rejection_reason_assignment():
    item = OrderItem(1 , 2 , Decimal("50.00"))
    order = Order(1,5 , (item ,  ) , datetime(2026 , 10 , 27 , 12 , 30 , tzinfo = timezone.utc ))

    with pytest.raises(AttributeError):
        order.rejection_reason = "out of stock"

    assert order.rejection_reason is None
    assert order.status == OrderStatus.PENDING

def test_order_total_uses_quantities_and_unit_prices():
    item1 = OrderItem(1 , 2 , Decimal("50.00"))
    item2 = OrderItem(2 , 3  , Decimal("20.00"))
    order = Order(1,5 , (item1, item2,   ) , datetime(2026 , 10 , 27 , 12 , 30 , tzinfo = timezone.utc ))

    assert order.total == Decimal("160.00")

def test_order_total_preserves_decimal_precision():
    item1 = OrderItem(1 , 3 , Decimal("00.10"))
    item2 = OrderItem(2 , 1  , Decimal("00.20"))
    order = Order(1,5 , (item1, item2,   ) , datetime(2026 , 10 , 27 , 12 , 30 , tzinfo = timezone.utc ))

    assert order.total == Decimal("0.50")