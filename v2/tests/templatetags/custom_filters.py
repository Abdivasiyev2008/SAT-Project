# myapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(list, index):
    try:
        return list[int(index) - 1]  # Adjust index to be zero-based
    except (IndexError, ValueError):
        return None
