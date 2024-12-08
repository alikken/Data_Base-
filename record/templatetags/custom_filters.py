from django import template

register = template.Library()

@register.filter
def attr(obj, field_name):
    return getattr(obj, field_name, '')



@register.filter
def getitem(dictionary, key):
    return dictionary.get(key)
