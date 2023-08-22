from django import template

register = template.Library()


@register.filter(name="is_in_cart")
def is_in_cart(product,cart):
    # cart is a dictionary
    keys=cart.keys()
    for fid in keys:
        if int(fid) == product.fid:
            return True
    print(keys)
    return False

@register.filter(name="cart_quantity")
def cart_quantity(product,cart):
    # cart is a dictionary
    keys=cart.keys()
    for fid in keys:
        if int(fid) == product.fid:
            return cart.get(fid)
    # print(keys)
    return 0

@register.filter(name="price_total")
def price_total(product,cart):
    return product.price * cart_quantity(product , cart)

@register.filter(name="total_price")
def total_price(products,cart):
    sum=0;
    for p in products:
        sum += price_total(p , cart)

    return sum
    


