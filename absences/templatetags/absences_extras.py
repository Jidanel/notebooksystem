# absences/templatetags/absences_extras.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def default(value, default_value):
    return value if value is not None else default_value