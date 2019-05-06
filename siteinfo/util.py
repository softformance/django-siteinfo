from django.template.defaultfilters import force_escape
from django.utils.safestring import mark_safe


class MetaTag:
    """Simple class to output XHTML conform <meta> tags."""
    def __init__(self, content='', name=None, http_equiv=None, scheme=None, lang=None):
        self.content = content
        self.name = name
        self.http_equiv = http_equiv
        self.scheme = scheme
        self.lang = lang and lang.lower()[:5]

    def __str__(self, request=None):
        attrs = ''
        if self.name:
            attrs += 'name="%s" ' % force_escape(self.name)
        attrs += 'content="%s" ' % force_escape(self.content)
        if self.http_equiv:
            attrs += 'http-equiv="%s" ' % force_escape(self.http_equiv)
        if self.scheme:
            attrs += 'scheme="%s" ' % force_escape(self.scheme)
        return mark_safe('<meta %s/>' % attrs)
