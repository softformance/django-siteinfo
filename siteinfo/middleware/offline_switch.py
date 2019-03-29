import re

import django
from django.conf import settings
from django.shortcuts import render_to_response


from siteinfo.models import SiteSettings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class OfflineSwitchMiddleware(MiddlewareMixin):
    """
    OfflineSwitchMiddleware will return a special view if SiteSettings.active
    is set to False.
    By default the 'siteinfo/offline_page.html' template will be used. But
    if a template matching the current site exists, it will be used.
    e.g 'siteinfo/offline_page-example.com.html'
    """

    def __init__(self, *args, **kwargs):
        super(OfflineSwitchMiddleware, self).__init__(*args, **kwargs)
        # same as in RequireLoginMiddleware
        self.login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')
        public_urls = []
        if hasattr(settings, 'PUBLIC_URLS'):
            public_urls = [re.compile(url) for url in settings.PUBLIC_URLS]
        public_urls += [(re.compile("^%s$" % self.login_url[1:]))]
        self.public_urls = tuple(public_urls)

    def process_request(self, request):
        try:
            current = SiteSettings.objects.get_current()
            # print u"current: %s" % current
            if current:
                # print u"current: %s" % current
                is_active = current.is_active_now()
                if is_active or getattr(getattr(request, 'user', False), 'is_staff', False):
                    return None
                for url in self.public_urls:
                    if url.match(request.path[1:]):
                        return None
                # the site must be offline
                templates = ['siteinfo/offline_page-%s.html' % current.site.domain, 'siteinfo/offline_page.html']
                context = {
                    'text': current.inactive_text,
                    'image': current.inactive_image,
                    'domain': current.site.domain
                }
                if django.VERSION < (1, 10):
                    from django.template.context import RequestContext
                    return render_to_response(templates, context, context_instance=RequestContext(request))
                else:
                    from django.shortcuts import render
                    return render(request, templates, context)
        except AttributeError:
            return None
        return None
