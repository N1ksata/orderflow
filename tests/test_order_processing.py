from domain.product import Product
from domain.order import Order
from decimal import Decimal
from domain.order_item import OrderItem
from domain.order_status import OrderStatus
from datetime import datetime,timezone
from application.order_process import process_order


def test_order_processing_rejects_insufficient_stock_without_partial_reservation():
    product1 = Product(1 , "keyboard" , Decimal("120.00") , 0)
    product2 = Product(2 , "mouse" , Decimal("100.00") , 5)

    order_mouse = OrderItem(2 , 2  , Decimal("100.00"))
    order_keyboard = OrderItem(1 , 1 , Decimal("120.00"))

    order = Order(1 , 1  , (order_mouse , order_keyboard), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))

    products = {product1.product_id: product1 , product2.product_id : product2}
    process_order(order , products)


    assert order.status == OrderStatus.REJECTED
    assert order.rejection_reason is not None and order.rejection_reason != ""
    assert product1.available_stock == 0 
    assert product2.available_stock == 5

def test_order_processing_confirms_order_and_reserves_all_items():
    product1 = Product(1 , "keyboard" , Decimal("120.00") , 1)
    product2 = Product(2 , "mouse" , Decimal("100.00") , 5)

    order_mouse = OrderItem(2 , 2  , Decimal("100.00"))
    order_keyboard = OrderItem(1 , 1 , Decimal("120.00"))

    order = Order(1 , 1  , (order_mouse , order_keyboard), datetime(2026, 10, 24, 15, 30 , tzinfo=timezone.utc))

    products = {product1.product_id: product1 , product2.product_id : product2}
    process_order(order , products)

    assert order.status == OrderStatus.CONFIRMED
    assert order.rejection_reason is None 
    assert product1.available_stock == 0
    assert product2.available_stock == 3