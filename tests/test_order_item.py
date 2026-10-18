from domain.order_item import OrderItem
import decimal
import pytest


def test_order_item_creation():
    item = OrderItem(1 , 2 , decimal.Decimal("50.00"))

    assert item.product_id == 1
    assert item.quantity == 2
    assert item.unit_price == decimal.Decimal("50.00")


# tests for quantity
def test_order_item_rejects_zero_quantity():
    with pytest.raises(ValueError):
        OrderItem(2 , 0 , decimal.Decimal("50.01"))

def test_order_item_rejects_fractional_quantity():
    with pytest.raises(ValueError):
            OrderItem(3 , 2.5 , decimal.Decimal("50.01"))

def test_order_item_rejects_negative_quantity():
    with pytest.raises(ValueError):
            OrderItem(4 , -1 , decimal.Decimal("50.01"))

def test_order_item_rejects_string_quantity():
    with pytest.raises(ValueError):
            OrderItem(5 , "2" , decimal.Decimal("50.01"))

def test_order_item_rejects_boolean_quantity():
    with pytest.raises(ValueError):
            OrderItem(5 , True , decimal.Decimal("50.01"))

def test_order_item_rejects_None_quantity():
    with pytest.raises(ValueError):
            OrderItem(5 , None , decimal.Decimal("50.01"))

# tests for product_id

def test_order_item_rejects_zero_product_id():
    with pytest.raises(ValueError):
        OrderItem(0, 2, decimal.Decimal("50.00"))


def test_order_item_rejects_negative_product_id():
    with pytest.raises(ValueError):
        OrderItem(-1, 2, decimal.Decimal("50.00"))


def test_order_item_rejects_fractional_product_id():
    with pytest.raises(ValueError):
        OrderItem(2.5, 2, decimal.Decimal("50.00"))


def test_order_item_rejects_string_product_id():
    with pytest.raises(ValueError):
        OrderItem("2", 2, decimal.Decimal("50.00"))


def test_order_item_rejects_boolean_product_id():
    with pytest.raises(ValueError):
        OrderItem(True, 2, decimal.Decimal("50.00"))


def test_order_item_rejects_none_product_id():
    with pytest.raises(ValueError):
        OrderItem(None, 2, decimal.Decimal("50.00"))

# tests for unit_price

def test_order_item_rejects_zero_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, decimal.Decimal("0"))


def test_order_item_rejects_negative_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, decimal.Decimal("-1.00"))


def test_order_item_rejects_float_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, 50.00)


def test_order_item_rejects_integer_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, 50)


def test_order_item_rejects_string_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, "50.00")


def test_order_item_rejects_boolean_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, True)


def test_order_item_rejects_none_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, None)


def test_order_item_rejects_nan_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, decimal.Decimal("NaN"))


def test_order_item_rejects_positive_infinity_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, decimal.Decimal("Infinity"))


def test_order_item_rejects_negative_infinity_price():
    with pytest.raises(ValueError):
        OrderItem(1, 2, decimal.Decimal("-Infinity"))