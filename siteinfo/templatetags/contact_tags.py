from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def render_email(email):
    if not email:
        return ''
    le, ri = (email + "#").split('@')
    bits = reversed((ri + le).split("."))
    html = """<span><script type="text/javascript">nospam(%s);</script></span>"""
    return mark_safe(html % ', '.join(map(lambda b: "'%s'" % b, bits)))
