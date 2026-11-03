def process_order(order , products):
    for item in order.items:
        product = products[item.product_id]
        if item.quantity > product.available_stock:
            return order.reject("Not enough availability")

    for item in order.items:
        product = products[item.product_id]
        product.reserve(item.quantity)

            
    order.confirm()