from domain.product import Product
from decimal import Decimal
import pytest


def test_product_creation_accepts_zero_stock():
    product = Product(1 ,"keyboard" ,Decimal("120.00") , 0)

    assert product.product_id == 1
    assert product.name == "keyboard"
    assert product.price == Decimal("120.00")
    assert product.available_stock == 0


def test_product_rejects_negative_stock():
    with pytest.raises(ValueError):
        Product(1 ,"keyboard" ,Decimal("120.00") , -1)

def test_product_rejects_boolean_stock():
    with pytest.raises(ValueError):
        Product(1 ,"keyboard" ,Decimal("120.00") , True)

def test_product_rejects_fractional_stock():
    with pytest.raises(ValueError):
        Product(1 ,"keyboard" ,Decimal("120.00") , 2.5)

def test_product_rejects_string_stock():
    with pytest.raises(ValueError):
        Product(1 ,"keyboard" ,Decimal("120.00") , "5")

def test_product_rejects_none_stock():
    with pytest.raises(ValueError):
        Product(1 ,"keyboard" ,Decimal("120.00") , None)

def test_product_rejects_empty_name():
    with pytest.raises(ValueError):
        Product(1 ,"" ,Decimal("120.00") , 0)

def test_product_rejects_blank_name():
    with pytest.raises(ValueError):
        Product(1 ," " ,Decimal("120.00") , 0)


def test_product_rejects_non_string_name():
    with pytest.raises(ValueError):
        Product(1 ,123 ,Decimal("120.00") , 0)

def test_product_rejects_zero_product_id():
    with pytest.raises(ValueError):
        Product(0 ,"keyboard" ,Decimal("120.00") , 0)



def test_product_rejects_negative_product_id():
    with pytest.raises(ValueError):
        Product(-1 ,"keyboard" ,Decimal("120.00") , 0)

def test_product_rejects_fractional_product_id():
    with pytest.raises(ValueError):
        Product(2.5 ,"keyboard" ,Decimal("120.00") , 0)

def test_product_rejects_str_product_id():
    with pytest.raises(ValueError):
        Product("1" ,"keyboard" ,Decimal("120.00") , 0)

def test_product_rejects_boolean_product_id():
    with pytest.raises(ValueError):
        Product(True ,"keyboard" ,Decimal("120.00") , 0)

def test_product_rejects_none_product_id():
    with pytest.raises(ValueError):
        Product(None ,"keyboard" ,Decimal("120.00") , 0)

def test_product_rejects_zero_price(): #price 0
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , Decimal("0") , 0)


def test_product_rejects_negative_price():
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , Decimal("-1") , 0)


def test_product_rejects_float_price():
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , 120.00 , 0)


def test_product_rejects_int_price():
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , 120 , 0)

def test_product_rejects_str_price():
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , "120.00" , 0)

def test_product_rejects_boolean_price():
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , True , 0)

def test_product_rejects_none_price():
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , None , 0)

def test_product_rejects_nan_decimal_price():
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , Decimal("NaN") , 0)

def test_product_rejects_positive_infinity_price():
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , Decimal("Infinity") , 0)

def test_product_rejects_negative_infinity_price():
    with pytest.raises(ValueError):
        Product(1 , "keyboard" , Decimal("-Infinity") , 0)

def test_product_reserve_decreases_available_stock():
    product = Product(1 , "keyboard" , Decimal("120.00") , 5)
    product.reserve(2)
    assert product.available_stock == 3
    