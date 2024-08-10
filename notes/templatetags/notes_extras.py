# notes/templatetags/notes_extras.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key)
    if isinstance(value, float):
        return "{:.2f}".format(value).replace(',', '.')
    return value
