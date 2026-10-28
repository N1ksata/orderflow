from decimal import Decimal
from domain.exceptions import InsufficientStockError


class Product():
    _product_id : int
    _name : str
    _price : Decimal
    _available_stock : int
    
    def __init__(self , product_id , name , price , available_stock ):

        if type(product_id) is not int or product_id <= 0:
            raise ValueError("Product ID must be a positive integer.")
        if type(name) is not str or name.strip() == "":
            raise ValueError("Name must be a non-empty string ")
        if type(price) is not Decimal or not price.is_finite() or price <= 0:
            raise ValueError("Price must be a finite, positive Decimal.")
        if type(available_stock) is not int or available_stock < 0:
            raise ValueError("Available stock must be a whole positive number or it can be 0.")


        self._product_id = product_id
        self._name = name
        self._price = price
        self._available_stock = available_stock


    @property 
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def available_stock(self):
        return self._available_stock


    def reserve(self , quantity):
        if type(quantity) is not int or quantity <= 0 :
            raise ValueError("Quantity must be whole positive number")
        if quantity > self._available_stock:
            raise InsufficientStockError("Not available stock")

        self._available_stock -= quantity