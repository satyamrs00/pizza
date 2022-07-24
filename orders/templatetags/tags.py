from django import template

register = template.Library()

@register.filter
def classname(obj):
    return obj.__class__.__name__

@register.simple_tag()
def multiply(unit_price, quantity):
    return unit_price * quantity