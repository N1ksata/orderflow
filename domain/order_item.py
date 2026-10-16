class OrderItem:
    def __init__( self , product_id , quantity , unit_price):

        if type(quantity) is not int or quantity <= 0:  #we need quantity -> int  and positive number
            raise ValueError("Quantity must be a positive integer.")
        
        if type(unit_price) is not decimal.Decimal or not unit_price.is_finite() or unit_price <= 0:
            raise ValueError("Unit price must be greater than zero.")
        
        if type(product_id) is not int or product_id <= 0:
            raise ValueError("Product ID must be a positive integer.")

        
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price