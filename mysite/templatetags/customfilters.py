from cart.cart import Cart
from django import template

register = template.Library()

@register.filter(name='number_of_items')
def number_of_items(cart):
    if isinstance(cart, Cart):
        return sum(cart.cart.values())
    return 0

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), 1)

@register.filter
def mul(value, arg):
    return float(value) * int(arg)

@register.filter
def percent_status(value):
    status_percent = {
        'pending': 0,
        'preparing': 25,
        'on_the_way': 50,
        'delivered': 100,
        'canceled': 0
    }
    return status_percent.get(value, 0)

@register.filter
def to(value, end):
    try:
        return range(int(value), int(end) + 1)
    except ValueError:
        return []

def number_of_items_detail(value):
    try:
        return range(1, int(value) + 1)
    except ValueError:
        return []