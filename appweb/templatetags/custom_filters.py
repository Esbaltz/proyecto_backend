from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter
def total_compra(items):
    return sum(item.libro.precio * item.cantidad for item in items)

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)