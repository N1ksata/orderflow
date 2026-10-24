from domain.order import Order
from domain.order_item import OrderItem
from domain.order_status import OrderStatus
from datetime import datetime, timezone
from decimal import Decimal

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
