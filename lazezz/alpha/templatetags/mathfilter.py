from django import template

register = template.Library()

@register.filter(name='mul')
def mul(a, b):
    return a*b