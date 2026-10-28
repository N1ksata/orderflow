from decimal import Decimal


class Product():
    _product_id : int
    _name : str
    _price : Decimal
    _available_stock : int
    
    def __init__(self , product_id , name , price , available_stock ):
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