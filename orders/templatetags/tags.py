from django import template

register = template.Library()

@register.filter
def classname(obj):
    return obj.__class__.__name__

@register.simple_tag()
def multiply(unit_price, quantity):
    return unit_price * quantity

# @register.simple_tag()
# def countitemsbyquantity(items):
#     sum = 0
#     for item, quantity in items:
#         sum += quantity
#     return sum