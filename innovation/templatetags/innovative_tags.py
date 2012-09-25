import re
from django import template

register = template.Library()


@register.filter
def lookup(d, key):
    return d[key]

@register.simple_tag
def active(request, pattern):
    if not hasattr(request, 'path'):
        return ''
    if pattern == "":
        return "active" if request.path == "/" else ""
    return 'active' if re.match(pattern, request.path) else ''
